import spacy
from bioel.ontology import BiomedicalOntology
from bioel.models.scispacy.candidate_generation import CandidateGenerator
from bioel.models.scispacy.scispacy_embeddings import KnowledgeBaseEmbeddings
from bioel.models.scispacy.entity_linking import EntityLinker
from bioel.utils.bigbio_utils import (
    load_bigbio_dataset,
    add_deabbreviations,
    dataset_to_documents,
    dataset_to_df,
    load_dataset_df,
    resolve_abbreviation,
    CUIS_TO_REMAP,
    CUIS_TO_EXCLUDE,
    DATASET_NAMES,
    VALIDATION_DOCUMENT_IDS,
)
from bioel.utils.dataset_consts import (
    dataset_to_pretty_name,
    model_to_pretty_name,
    model_to_color,
)
import ujson
import os


def evaluate_model(
    dataset,
    ontology,
    k,
    path_to_save,
    output_path,
    equivalant_cuis=None,
    path_to_abbrev=None,
):
    """
    Params :
    ---------
    dataset: str
        Name of the dataset to evaluate
    ontology: BiomedicalOntology
        Ontology to use for candidate generation
    k: int
        Number of candidates to generate
    path_to_save: str
        Path to save the serialized knowledge base
    output_path: str
        Path to save the output
    equivalent_cuis: bool
        Whether the ontology has equivalent cuis or not
    path_to_abbrev: str
        Path to the abbreviations file
    """
    myembed = KnowledgeBaseEmbeddings(ontology)
    myembed.create_tfidf_ann_index(path_to_save)
    kb = myembed.serialized_kb()
    cand_gen = CandidateGenerator(kb)
    df = load_dataset_df(name=dataset, path_to_abbrev=path_to_abbrev)
    df = df.query("split == 'test'")

    output = list()

    if equivalant_cuis:
        cui_synsets = {}
        for cui, entity in ontology.entities.items():
            cui_synsets[cui] = entity.equivalant_cuis

    path_to_abbrev = True
    for index, row in df.iterrows():
        list_dbid = list(row.db_ids)  # Accessing db_ids as a list
        if path_to_abbrev:
            mention = row.deabbreviated_text  # Accessing the text of the current row
        else:
            mention = row.text
        candidates = cand_gen([mention], 3 * k)  # Generating candidates
        predicted = []

        for cand in candidates[0]:
            score = max(cand.similarities)
            predicted.append((cand.concept_id, score))

        sorted_predicted = sorted(predicted, reverse=True, key=lambda x: x[1])
        sorted_predicted = sorted_predicted[:k]  # Taking top k predictions

        cui_result = [[cui[0]] for cui in sorted_predicted]
        score = [[cui[1]] for cui in sorted_predicted]

        if equivalant_cuis:
            cui_result = [cui_synsets[y[0]] for y in cui_result]

        if path_to_abbrev:
            output.append(
                {
                    "document_id": row.document_id,
                    "offsets": row.offsets,
                    "text": row.text,
                    "type": row.type,
                    "db_ids": list_dbid,
                    "split": row.split,
                    "deabbreviated_text": row.deabbreviated_text,
                    "mention_id": row.mention_id + ".abbr_resolved",
                    "candidates": cui_result,
                    "scores": score,
                }
            )
        else:
            output.append(
                {
                    "document_id": row.document_id,
                    "offsets": row.offsets,
                    "text": row.text,
                    "type": row.type,
                    "db_ids": list_dbid,
                    "split": row.split,
                    "mention_id": row.mention_id,
                    "candidates": cui_result,
                    "scores": score,
                }
            )

    with open(output_path, "w") as f:
        f.write(ujson.dumps(output, indent=2))


if __name__ == "__main__":
    ontology_dir = "/mitchell/entity-linking/kbs/medic.tsv"
    myonto = BiomedicalOntology.load_medic(filepath=ontology_dir, name="medic")
    dataset = "ncbi_disease"

    # mesh_dict = {"name": "mesh", "filepath": "/mitchell/entity-linking/2017AA/META/"}
    # myonto = BiomedicalOntology.load_mesh(**mesh_dict)
    # dataset = "nlmchem"

    # ontology_dict = {
    #     "name": "entrez",
    #     "filepath": "/mitchell/entity-linking/el-robustness-comparison/data/gene_info.tsv",
    #     "dataset": "nlm_gene",
    # }
    # myonto = BiomedicalOntology.load_entrez(**ontology_dict)
    # dataset = "nlm_gene"

    # ontology_dict = {
    #     "name": "entrez",
    #     "filepath": "/mitchell/entity-linking/el-robustness-comparison/data/gene_info.tsv",
    #     "dataset": "gnormplus",
    # }
    # myonto = BiomedicalOntology.load_entrez(**ontology_dict)
    # dataset = "gnormplus"

    # umls_dict = {"name": "umls", "filepath": "/mitchell/entity-linking/2017AA/META/"}
    # myonto = BiomedicalOntology.load_umls(**umls_dict)
    # dataset = "medmentions_st21pv"

    # umls_dict = {"name": "umls", "filepath": "/mitchell/entity-linking/2017AA/META/"}
    # myonto = BiomedicalOntology.load_umls(**umls_dict)
    # dataset = "medmentions_full"

    path_to_save = f"/home2/cye73/data_test2/scispacy/kb_paths_scispacy/{dataset}"
    output_path = f"/home2/cye73/results2/scispacy/{dataset}_output.json"
    evaluate_model(
        dataset=dataset,
        ontology=myonto,
        k=10,
        path_to_save=path_to_save,
        output_path=output_path,
        path_to_abbrev="/home2/cye73/data_test2/abbreviations.json",
    )
