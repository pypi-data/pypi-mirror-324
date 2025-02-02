# Copyright (c) Facebook, Inc. and its affiliates.
# Copyright (c) 2021 Dhruv Agarwal and authors of arboEL.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import argparse
import json
import ujson
import logging
import os
import torch
import pickle
from tqdm import tqdm

from torch.utils.data import DataLoader, SequentialSampler

from transformers import AutoTokenizer

from bioel.models.arboel.model.biencoder import BiEncoderRanker
import bioel.models.arboel.data.data_process as data_process
from bioel.models.arboel.crossencoder.original.train_cross import (
    read_dataset,
)
from bioel.models.arboel.model.common.params import BlinkParser

from IPython import embed

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_topk_predictions(
    input_crossencoder,
    reranker,
    train_dataloader,
    candidate_pool,
    cand_encode_list,
    silent,
    logger,
    top_k=10,
    save_predictions=False,
):
    """
    Retrieves the top-k predictions for a set of inputs using a reranking model.

    ------
    Params:
    - reranker : model
    biencoder
    - train_dataloader : DataLoader
    Provides batches of input data for evaluation.
    - candidate_pool : list of list (dim : )
    Contains the IDs of the candidate description.
    - cand_encode_list : list
    A list of precomputed candidate encodings that the reranker uses to score the inputs.
    - silent (bool): If True, the function operates silently without outputting progress; if False, progress
      is displayed using tqdm.
    - logger : logger object
    - top_k : int
    The number of top predictions to retrieve for each input, default is 10.
    - save_predictions : bool
    If True, saves the context, candidate indices, and label information for each prediction.

    Returns:
    - dict: A dictionary containing tensors for the contexts, candidate vectors, and labels of the top-k predictions.
      This includes:
        - "context_vecs": Tensor of input contexts.
        - "candidate_vecs": Tensor of candidate data corresponding to the top predictions.
        - "labels": Tensor of label indices indicating the position of the correct candidate within the top-k.
    """
    reranker.model.eval()
    logger.info("Getting top %d predictions." % top_k)
    if silent:
        iter_ = train_dataloader
    else:
        iter_ = tqdm(train_dataloader)

    count = 0
    n_samples = 0

    nn_context = []
    nn_candidates = []
    nn_labels = []
    nn_labels_bis = []

    indicies = input_crossencoder
    print("len(indicies) :", len(indicies))
    assert len(indicies) != 0, "list of top k candidates idx is empty"
    assert (
        len(indicies[0]) >= top_k
    ), f"{len(indicies[0])} <= {top_k} : Dimension mismatch between number of candidates (top_k) and the length of the list of top candidates idx"

    for step, batch in enumerate(iter_):
        length = len(batch)
        batch = tuple(t.cuda() for t in batch)  # Multiple tensors
        if len(batch) == 4:
            context_input, _, srcs, label_ids = batch

        elif len(batch) == 3:
            context_input, _, label_ids = batch

        for i in range(context_input.size(0)):

            inds = indicies[n_samples]
            n_samples += 1

            pointer = -1
            for j in range(top_k):
                if inds[j] == label_ids[i].item():
                    pointer = j  #  position of the gold cui in the candidate list
                    break

            if pointer == -1:
                count += 1
                continue

            if not save_predictions:
                continue

            # add examples in new_data
            cur_candidates = candidate_pool[inds]
            nn_context.append(context_input[i].cpu().tolist())
            nn_candidates.append(cur_candidates[:top_k].cpu().tolist())
            nn_labels.append(pointer)
            nn_labels_bis.append(label_ids[i].item())

    print("total_correct_samples:", n_samples - count)
    print("total_samples:", n_samples)
    nn_context = torch.LongTensor(nn_context)
    nn_candidates = torch.LongTensor(nn_candidates)
    nn_labels = torch.LongTensor(nn_labels)
    nn_labels_bis = torch.LongTensor(nn_labels_bis)
    nn_data = {
        "context_vecs": nn_context,
        "candidate_vecs": nn_candidates,
        "labels": nn_labels,
        "labels_bis": nn_labels_bis,
    }

    return nn_data


def load_entity_dict(logger, params):
    """
    Loads and processes a dictionary of entities from a specified file path.
    ------
    Params:
    - logger : logger object
    - params : dict
    A dictionary of parameters that control the function's behavior
    ------
    Returns:
    - list of tuples: Each tuple contains two elements, the 'title' and the 'text' (description) of an entity.
    """
    path = params.get("entity_dict_path", None)
    assert path is not None, "Error! entity_dict_path is empty."

    logger.info("Loading entity description from path: " + path)
    entity_list = []  # Initialize the list to store tuples of title and text
    with open(path, "rb") as f:  # Open file in binary read mode
        full_list = pickle.load(f)

        for item in full_list:
            title = item["title"]
            text = item.get("description", "").strip()
            entity_list.append((title, text))

            if params.get("debug", False) and len(entity_list) > 200:
                break

    return entity_list


def get_candidate_pool_tensor(
    entity_desc_list,
    tokenizer,
    max_seq_length,
    logger,
):
    """
    Processes a list of entity descriptions by converting them into token IDs.
    The resulting IDs are then collected into a tensor.
    ------
    Params:
    - entity_desc_list : list of str or tuple
    A list where each element is either a string representing an entity description or a tuple containing a title and an entity description.
    - tokenizer : PreTrainedTokenizer
    Used to convert text into a sequence of token IDs.
    - max_seq_length : int
    The maximum length of the token sequences.
    - logger : logger object

    Returns:
    - torch.LongTensor: Contains the token IDs of the entity descriptions.
    """
    # TODO: add multiple thread process
    logger.info("Convert candidate text to id")
    cand_pool = []
    for entity_desc in tqdm(entity_desc_list):
        if type(entity_desc) is tuple:
            title, entity_text = entity_desc
        else:
            title = None
            entity_text = entity_desc

        rep = data_process.get_candidate_representation(
            entity_text,
            tokenizer,
            max_seq_length,
            title,
        )
        cand_pool.append(rep["ids"])

    cand_pool = torch.LongTensor(cand_pool)
    return cand_pool


# def encode_candidate(
#     reranker,
#     candidate_pool,
#     encode_batch_size,
#     silent,
#     logger,
# ):
#     """
#     Encodes a pool of candidate entries using a reranker model.
#     ------
#     Params:
#     - reranker : model
#     biencoder
#     - candidate_pool : Dataset
#     A dataset containing candidate entries that need to be encoded.
#     - encode_batch_size : int
#     Size of the batches in which the candidate_pool will be processed.
#     - silent : bool
#     If True, the function operates without printing progress; if False, progress is displayed using tqdm.
#     - logger : logger object

#     Returns:
#     - torch.Tensor: Contains the encoded representations of all candidates in the candidate pool.
#     """
#     reranker.model.eval()
#     sampler = SequentialSampler(candidate_pool)
#     data_loader = DataLoader(
#         candidate_pool, sampler=sampler, batch_size=encode_batch_size
#     )
#     if silent:
#         iter_ = data_loader
#     else:
#         iter_ = tqdm(data_loader)

#     cand_encode_list = None
#     for step, batch in enumerate(iter_):
#         cand_encode = reranker.encode_candidate(batch.cuda())
#         if cand_encode_list is None:
#             cand_encode_list = cand_encode
#         else:
#             cand_encode_list = torch.cat((cand_encode_list, cand_encode))

#     return cand_encode_list


def load_or_generate_candidate_pool(
    tokenizer,
    params,
    logger,
    cand_pool_path,
):
    candidate_pool = None
    if cand_pool_path is not None:
        # try to load candidate pool from file
        try:
            logger.info("Loading pre-generated candidate pool from: ")
            logger.info(cand_pool_path)
            candidate_pool = torch.load(cand_pool_path)
        except:
            logger.info("Loading failed. Generating candidate pool")

    if candidate_pool is None:
        # compute candidate pool from entity list
        entity_desc_list = load_entity_dict(logger, params)
        candidate_pool = get_candidate_pool_tensor(
            entity_desc_list,
            tokenizer,
            params["max_cand_length"],
            logger,
        )

        if cand_pool_path is not None:
            logger.info("Saving candidate pool.")
            torch.save(candidate_pool, cand_pool_path)

    return candidate_pool


def eval_biencoder(params, reranker, tokenizer, input_crossencoder):
    output_path = params["output_path"]
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    model = reranker.model

    cand_encode_path = params.get("cand_encode_path", None)

    # candidate encoding is not pre-computed.
    # load/generate candidate pool to compute candidate encoding.
    cand_pool_path = params.get("cand_pool_path", None)
    candidate_pool = load_or_generate_candidate_pool(
        tokenizer,
        params,
        logger,
        cand_pool_path,
    )

    candidate_encoding = None
    if cand_encode_path is not None:
        # try to load candidate encoding from path
        # if success, avoid computing candidate encoding
        try:
            logger.info("Loading pre-generated candidate encode path.")
            candidate_encoding = torch.load(cand_encode_path)
        except:
            logger.info("Loading failed. Generating candidate encoding.")

    if candidate_encoding is None:
        candidate_encoding = data_process.embed_and_index(
            model=reranker,
            token_id_vecs=candidate_pool,
            encoder_type="candidate",
            batch_size=768,
            only_embed=True,
        )

        if cand_encode_path is not None:
            # Save candidate encoding to avoid re-compute
            logger.info("Saving candidate encoding to file " + cand_encode_path)
            torch.save(candidate_encoding, cand_encode_path)

    test_samples = read_dataset(params["mode"], params["data_path"])
    logger.info("Read %d test samples." % len(test_samples))

    entity_dictionary_pkl_path = os.path.join(
        params["data_path"], "entity_dictionary.pickle"
    )
    entity_dictionary_loaded = False
    if os.path.isfile(entity_dictionary_pkl_path):
        print("Loading stored processed entity dictionary...")
        with open(entity_dictionary_pkl_path, "rb") as read_handle:
            entity_dictionary = pickle.load(read_handle)
        entity_dictionary_loaded = True

    test_data, test_tensor_data = data_process.process_mention_with_candidate(
        samples=test_samples,
        entity_dictionary=entity_dictionary,
        tokenizer=tokenizer,
        max_context_length=params["max_context_length"],
        max_cand_length=params["max_cand_length"],
        context_key=params["context_key"],
        silent=params["silent"],
        dictionary_processed=entity_dictionary_loaded,
        logger=logger,
        debug=params["debug"],
    )

    test_sampler = SequentialSampler(test_tensor_data)
    test_dataloader = DataLoader(
        test_tensor_data, sampler=test_sampler, batch_size=params["encode_batch_size"]
    )

    save_results = params.get("save_topk_result")
    new_data = get_topk_predictions(
        input_crossencoder=input_crossencoder,
        reranker=reranker,
        train_dataloader=test_dataloader,
        candidate_pool=candidate_pool,
        cand_encode_list=candidate_encoding,
        silent=params["silent"],
        logger=logger,
        top_k=params["top_k"],
        save_predictions=save_results,
    )

    if save_results:
        save_data_path = os.path.join(
            params["output_path"],
            "candidates_%s_top%d.t7" % (params["mode"], params["top_k"]),
        )
        torch.save(new_data, save_data_path)

    return new_data


# if __name__ == "__main__":
#     parser = BlinkParser(add_model_args=True)
#     parser.add_eval_args()
#     args = parser.parse_args()
#     print(args)
#     main(args.__dict__)
