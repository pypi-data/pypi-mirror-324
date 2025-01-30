import os

import pandas as pd
import torch

# from RNABERT import RNABERT
from torch.nn import AdaptiveAvgPool1d

from scprint import utils

from . import ESM2


def protein_embeddings_generator(
    genedf: pd.DataFrame,
    organism: str = "homo_sapiens",  # mus_musculus,
    cache: bool = True,
    fasta_path: str = "/tmp/data/fasta/",
    embedding_size: int = 512,
    embedder: str = "esm2",  # or glm2
):
    """
    protein_embeddings_generator embed a set of genes using fasta file and LLMs

    Args:
        genedf (pd.DataFrame): A DataFrame containing gene information.
        organism (str, optional): The organism to which the genes belong. Defaults to "homo_sapiens".
        cache (bool, optional): If True, the function will use cached data if available. Defaults to True.
        fasta_path (str, optional): The path to the directory where the fasta files are stored. Defaults to "/tmp/data/fasta/".
        embedding_size (int, optional): The size of the embeddings to be generated. Defaults to 512.

    Returns:
        pd.DataFrame: Returns a DataFrame containing the protein embeddings, and the RNA embeddings.
    """
    # given a gene file and organism
    # load the organism fasta if not already done
    utils.load_fasta_species(species=organism, output_path=fasta_path, cache=cache)
    # subset the fasta
    fasta_file = next(
        file for file in os.listdir(fasta_path) if file.endswith(".all.fa.gz")
    )
    if embedder == "esm2":
        protgenedf = genedf[genedf["biotype"] == "protein_coding"]
        utils.utils.run_command(["gunzip", fasta_path + fasta_file])
        utils.subset_fasta(
            protgenedf.index.tolist(),
            subfasta_path=fasta_path + "subset.fa",
            fasta_path=fasta_path + fasta_file[:-3],
            drop_unknown_seq=True,
        )
        prot_embedder = ESM2()
        prot_embeddings = prot_embedder(
            fasta_path + "subset.fa", output_folder=fasta_path + "esm_out/", cache=cache
        )
    else:
        raise ValueError(f"Embedder {embedder} not supported")
    # load the data and erase / zip the rest
    utils.utils.run_command(["gzip", fasta_path + fasta_file[:-3]])
    # return the embedding and gene file
    # TODO: to redebug
    # do the same for RNA
    # rnagenedf = genedf[genedf["biotype"] != "protein_coding"]
    # fasta_file = next(
    #    file for file in os.listdir(fasta_path) if file.endswith(".ncrna.fa.gz")
    # )
    # utils.utils.run_command(["gunzip", fasta_path + fasta_file])
    # utils.subset_fasta(
    #    rnagenedf["ensembl_gene_id"].tolist(),
    #    subfasta_path=fasta_path + "subset.ncrna.fa",
    #    fasta_path=fasta_path + fasta_file[:-3],
    #    drop_unknown_seq=True,
    # )
    # rna_embedder = RNABERT()
    # rna_embeddings = rna_embedder(fasta_path + "subset.ncrna.fa")
    ## Check if the sizes of the cembeddings are not the same
    # utils.utils.run_command(["gzip", fasta_path + fasta_file[:-3]])
    #
    m = AdaptiveAvgPool1d(embedding_size)
    prot_embeddings = pd.DataFrame(
        data=m(torch.tensor(prot_embeddings.values)), index=prot_embeddings.index
    )
    # rna_embeddings = pd.DataFrame(
    #    data=m(torch.tensor(rna_embeddings.values)), index=rna_embeddings.index
    # )
    # Concatenate the embeddings
    return prot_embeddings  # pd.concat([prot_embeddings, rna_embeddings])
