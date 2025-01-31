"""Command-line interface."""

__version__ = "0.0.2"

import time

import click
import pandas as pd
import os
import requests
import pyranges

from liquidsig.deconvolution import HeirarchicalDeconvolution
from importlib.metadata import version


# Some data preprocessing. Should move this elsewhere.
def flatten_series(series):
    """
    Flattens a Pandas Series containing nested dictionaries and lists, designed
    to flatten the output of the CZI CellGuide API.

    Args:
        series: The Pandas Series to flatten.

    Returns:
        A Pandas DataFrame with the flattened data.
    """
    data = []
    for tissue, cell_types in series.items():
        for cell_type_id, markers in cell_types.items():
            for marker in markers:
                row = {"tissue": tissue, "cell_type_id": cell_type_id}
                row.update(marker)
                data.append(row)
    return pd.DataFrame(data)


@click.command(help="LiquidSig: Predict tissue of origin from cfRNA transcript data.")
@click.version_option()
@click.option(
    "--transcript-quants",
    help="Transcript-level quant.sf file (e.g., from Salmon).",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    # TODO: expand to multiple with default=[]
)
# Select one of human or mouse organism via this click flag
@click.option(
    "--organism",
    help="Organism to analyze, currently limited to mouse and human (via CZI CellGuide).",
    type=click.Choice(["Homo sapiens", "Mus musculus"]),
    default="Homo sapiens",
    show_default=True,
)
# Optional flags
@click.option("--verbose", help="Verbose output.", is_flag=True)
@click.option("--debug", help="Debug output.", is_flag=True)
@click.option("--overwrite", help="Overwrite output file if it exists.", is_flag=True)
def main(
    transcript_quants: str,
    organism: str,
    verbose: bool,
    debug: bool,
    overwrite: bool,
) -> None:
    """LiquidSig"""
    time_start = time.time()

    # Print run information
    click.echo(f"LiquidSig: cfRNA ML-Guided Analysis (version {version('liquidsig')})")
    if version("liquidsig") != __version__:
        click.echo(
            "** Warning: Runtime and installed versions differ! Your environment may be corrupt."
        )

    click.echo(f"\nTranscript quants: {transcript_quants}")
    # click.echo(f"ENST to gene mapping: … TODO")

    # Load transcript quants, expecting a .sf file (TSV) with predefined columns
    click.echo("Loading transcript quants …")
    transcript_quants_df = pd.read_csv(transcript_quants, sep="\t")

    # Assert that the transcript quants file has the expected columns
    if verbose:
        click.echo("Checking transcript quants columns …\n")
        expected_columns = ["Name", "Length", "EffectiveLength", "TPM", "NumReads"]
        assert all(
            column in transcript_quants_df.columns for column in expected_columns
        ), f"Expected columns: {expected_columns}"
        click.echo(transcript_quants_df.head())

    # Let's download the marker data from CZBioHub's CellGuide
    # Per discussion with Max Lombardo on Slack, this is a snapshot from Q2/Q3 2024
    # We can also scrape the individual json files, but it's tedious -- hopefully their API allows a clearer access later.

    # Download this URL and save it into a references/ directory, only if it doesn't already exist:
    marker_data_url = "https://cellguide.cellxgene.cziscience.com/1716401368/computational_marker_genes/marker_gene_data.json.gz"
    ref_dir = "references"
    marker_file = os.path.join(ref_dir, "marker_gene_data.json.gz")

    if not os.path.exists(ref_dir):
        os.makedirs(ref_dir)

    if not os.path.exists(marker_file):
        click.echo(f"Downloading marker data from {marker_data_url}")
        response = requests.get(marker_data_url, timeout=30)
        response.raise_for_status()
        with open(marker_file, "wb") as f:
            f.write(response.content)
    else:
        click.echo(f"\nMarker data cache exists at: {marker_file}")

    # Also download the Gencode .GTF for annotations / transcript data
    # Note this is the *FULL* GENCODE GTF that includes scaffolds like "ENSG00000275405"
    # We probably also need to download the lncRNA variant version?
    gencode_gtf_url = "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/gencode.v47.chr_patch_hapl_scaff.annotation.gtf.gz"
    gencode_gtf_file = os.path.join(
        ref_dir, "gencode.v47.chr_patch_hapl_scaff.annotation.gtf.gz"
    )

    if not os.path.exists(gencode_gtf_file):
        click.echo(f"Downloading GENCODE GTF data from {gencode_gtf_url}")
        response = requests.get(gencode_gtf_url, timeout=30)
        response.raise_for_status()
        with open(gencode_gtf_file, "wb") as f:
            f.write(response.content)
    else:
        click.echo(f"GENCODE GTF cache exists at {gencode_gtf_file}\n")

    # Open and load the .json.gz
    marker_data = pd.read_json(marker_file, compression="gzip")

    if verbose:
        click.echo("\nMarker data:")
        click.echo(marker_data.head())
        click.echo(f"\nNumber of organisms: {len(marker_data.columns)}")
        click.echo("Organisms: " + ",".join(marker_data.columns.to_list()))

    # organism_marker_data is a dataframe of tissues & cell types w/ corresponding markers
    #  Explained a bit in: https://cellxgene.cziscience.com/docs/04__Analyze%20Public%20Data/4_2__Gene%20Expression%20Documentation/4_2_5__Find%20Marker%20Genes ?
    # e.g. organism_marker_data['heart']['CL:4033054']
    #    [{'marker_score': 1.6855389931276041,   # AKA effect size. Indicates how much higher the average gene expression is in this cell type relative to other cell types in the same tissue.
    #     'me': 3.168754253595605, # Mean expression average(ln(cppt+1))-normalized gene expression among cells in the cell type
    #     'pc': 0.821720388599369,  # Percentage of cells expressing a gene in the cell type (?)
    #     'gene': 'PLA2G5'}

    # Note some have tissue entries but nan data (e.g., "urethra" and "urinary bladder")
    # TODO: Sort out ontology to better manage these? e.g. there's a "bladder organ" which has markers, but not "urinary bladder"
    organism_marker_data = marker_data[organism].dropna()
    assert (
        len(organism_marker_data.index) > 0
    ), f"No tissues with marker genes found for {organism}."

    assert organism == "Homo sapiens"  # not yet implemented for mouse

    if verbose:
        click.echo(
            f"{len(organism_marker_data.index)-1} tissues found for {organism}."
        )  # -1 to exclude the "All Tissues" first row
        click.echo("Tissues: " + ",".join(organism_marker_data.index.to_list()))

    cellgene_markers = []
    malformed_entries = 0
    # Let's get the list of all marker genes from this nested dict
    for tissue, cell_types in organism_marker_data.items():
        for cell_type, markers in cell_types.items():
            for marker_dict in markers:
                try:
                    cellgene_markers.append(marker_dict["gene"])
                except KeyError:
                    malformed_entries += 1  # Some entries lack genes? I suspect the CZI snapshot has some errors, or it's an ontology issue.

    if verbose:
        click.echo(
            f"\nMalformed entries (no gene) in CellGene markers: {malformed_entries}"
        )

    # cellgene_markers is a list of genes like ["ABCG1"]
    cellgene_markers = list(set(cellgene_markers))  # Remove duplicates

    if verbose:
        click.echo(
            f"\n{len(cellgene_markers)} distinct marker genes found in {organism}."
        )

    click.echo("Loading Gencode GTF data …")
    ## Ensure the marker gene names are actual gene names, or convert ENSG->gene_name
    # Load the GTF file to convert ENSG to gene names
    gencode_df = pyranges.read_gtf(gencode_gtf_file, as_df=True)

    # Filter the GTF to only include gene entries
    # TODO: explore lncRNAs - lots of data there
    gencode_genes_df = gencode_df[gencode_df.Feature == "gene"]

    # See if our quant has ENSG or gene names
    first_quant_entry = transcript_quants_df["Name"].iloc[0]
    print(
        f"Validating gene names in quant file using first entry: {first_quant_entry} (from {transcript_quants})"
    )

    if first_quant_entry.startswith("ENST"):
        click.echo(
            "\tENST prefix detected in quants: pure transcript not yet supported."
        )
        return
    else:
        click.echo(f"Number of genes in your quant: {len(transcript_quants_df)}")
        click.echo(
            f"Number of *distinct* genes in your quant: {len(set(transcript_quants_df['Name'].values))}"
        )

        if first_quant_entry.startswith("ENSG"):
            click.echo(
                "\tENSG prefix detected in quants, converting to common gene name."
            )
            # We want to convert the column transcript_quants_df['Name'] to gene names, using the gencode_genes dataframe.
            # Specifically, we want to use gencode_genes["gene_name"] where gencode_genes["gene_id"] == transcript_quants_df["Name"]
            # However, the gencode gene_id is suffixed by the ensembl version (e.g. ENSG00000237491.11) -- so we drop the period and any characters after it
            gencode_genes_df.loc[:, "gene_id"] = (
                gencode_genes_df["gene_id"].str.split(".").str[0]
            )

            polished_quants_df = transcript_quants_df.merge(
                gencode_genes_df, left_on="Name", right_on="gene_id", how="inner"
            )
            click.echo(
                f"*Distinct* genes by GENCODE name: {len(set(polished_quants_df['gene_name'].values))}"
            )
            # Also calculate the number of genes that are not in the GTF
            missing_genes = set(transcript_quants_df["Name"].values) - set(
                gencode_genes_df["gene_id"].values
            )
            click.echo(f"Number of genes *not* found in GTF: {len(missing_genes)}")

            if len(missing_genes) > 0:
                orphans = transcript_quants_df[
                    transcript_quants_df["Name"].isin(missing_genes)
                ]
                orphan_file = "unannotated-quants.tsv"
                orphans.to_csv(orphan_file, sep="\t", index=False)
                click.echo(
                    f"Unannotated quants (not found in GTF) saved to {orphan_file}"
                )

        else:
            click.echo(
                "No ENST or ENSG prefix, assuming gene names are already present and match ENSEMBL/GENCODE."
            )
            click.echo(
                "If this is incorrect, please file a bug at github.com/semenko/liquidsig"
            )
            polished_quants_df = transcript_quants_df

    # Next, let's see what marker genes are in the transcript quants
    marker_polished_quants_df = polished_quants_df[
        polished_quants_df["gene_name"].isin(cellgene_markers)
    ]

    click.echo(
        f"Number of CellGene markers in your dataset: {len(marker_polished_quants_df)}"
    )
    click.echo(
        f"Percent of CellGene markers represented in your data: {len(marker_polished_quants_df) / len(cellgene_markers) * 100:.2f}%"
    )

    if debug:
        # Save markers to a file for debugging
        marker_file = "marker_genes_in_quant.tsv"
        marker_polished_quants_df.to_csv(marker_file, sep="\t", index=False)
        click.echo(f"Marker genes saved to {marker_file}")

        # Save missed markers to a file for debugging
        missed_markers = set(cellgene_markers) - set(
            marker_polished_quants_df["gene_name"].values
        )
        missed_marker_file = "missed_marker_genes.tsv"
        missed_marker_df = pd.DataFrame(missed_markers, columns=["gene_name"])
        missed_marker_df.to_csv(missed_marker_file, sep="\t", index=False)
        click.echo(f"Missed marker genes saved to {missed_marker_file}")

    if len(marker_polished_quants_df) < 100:
        click.echo("Not enough marker genes are represented in your cfRNA quants.")
        return

    ## Time to deconvolute

    # Rename gene_name to GeneName in polished_quants_df
    polished_quants_df.rename(columns={"gene_name": "GeneName"}, inplace=True)

    organism_marker_data_df = flatten_series(organism_marker_data)

    # Drop the tissue named "All Tissues"
    organism_marker_data_df = organism_marker_data_df[
        organism_marker_data_df["tissue"] != "All Tissues"
    ]

    # Hackish -- must fix this later
    renamed_organism_marker_data = organism_marker_data_df.rename(
        columns={
            "tissue": "Tissue",
            "cell_type_id": "Cell",
            "marker_score": "GeneMarkerScore",
            "me": "GeneMeanExpression",
            "pc": "GenePercentExpressing",
            "gene": "GeneName",
        }
    )

    # Now we have the polished quants and the marker data in a format that can be used for deconvolution
    # Let's run the deconvolution
    deconvolution = HeirarchicalDeconvolution(
        polished_quants_df, renamed_organism_marker_data
    )

    (
        tissue_proportion_df,
        tissue_stats,
        tissue_figures,
        cell_proportion_df,
        cell_stats,
        cell_proportion_figures_dict,
        cell_scatter_figures_dict,
        cell_marker_heatmap_figures_dict,
        cell_residual_figures_dict,
    ) = deconvolution.run()

    print("Tissue Proportions:")
    print(tissue_proportion_df)
    print("\nCell Proportions within Tissues:")
    print(cell_proportion_df)

    run_results_path = "run_results/"
    os.makedirs(run_results_path, exist_ok=True)

    tissue_proportion_df.to_csv(
        os.path.join(run_results_path, "tissue_deconvolution.csv"), index=False
    )

    cell_proportion_df.to_csv(
        os.path.join(run_results_path, "cell_deconvolution.csv"), index=False
    )

    # Also save the stats
    tissue_stats_df = pd.DataFrame.from_dict(tissue_stats, orient="index").transpose()
    tissue_stats_df.to_csv(
        os.path.join(run_results_path, "tissue_deconvolution_stats.csv"), index=False
    )

    cell_stats_df = pd.DataFrame.from_dict(cell_stats, orient="index").transpose()
    cell_stats_df.to_csv(
        os.path.join(run_results_path, "cell_deconvolution_stats.csv"), index=False
    )

    # To display figures:
    # plt.show() # This will display all generated figures

    # # To save figures (optional):
    tissue_figures["proportion"].savefig(
        os.path.join(run_results_path, "tissue_proportions.png")
    )
    tissue_figures["scatter"].savefig(
        os.path.join(run_results_path, "tissue_scatter.png")
    )
    tissue_figures["marker_heatmap"].savefig(
        os.path.join(run_results_path, "tissue_marker_heatmap.png")
    )
    tissue_figures["residual"].savefig(
        os.path.join(run_results_path, "tissue_residual_plot.png")
    )

    for tissue, fig in cell_proportion_figures_dict.items():
        if fig:
            fig.savefig(
                os.path.join(run_results_path, f"cell_proportions_{tissue}.png")
            )
    for tissue, fig in cell_scatter_figures_dict.items():
        if fig:
            fig.savefig(os.path.join(run_results_path, f"cell_scatter_{tissue}.png"))

    for tissue, fig in cell_marker_heatmap_figures_dict.items():
        if fig:
            fig.savefig(
                os.path.join(run_results_path, f"cell_marker_heatmap_{tissue}.png")
            )
    for tissue, fig in cell_residual_figures_dict.items():
        if fig:
            fig.savefig(
                os.path.join(run_results_path, f"cell_residual_plot_{tissue}.png")
            )

    click.echo(f"Figures and stats saved to: {run_results_path}")
    click.echo("WARNING: This is an *Alpha* implementation!", color="yellow")

    # Export the renamed quants to a file
    # polished_quants_file = "polished_quants.tsv"
    # polished_quants_df.to_csv(polished_quants_file, sep="\t", index=False)
    # click.echo(f"Polished quants saved to {polished_quants_file}")

    # import IPython; IPython.embed()

    # Drop to an ipython shell for debugging
    # Sort marker genes from the marker_data nested dict

    # Index(['Chromosome', 'Source', 'Feature', 'Start', 'End', 'Score', 'Strand',
    #   'Frame', 'gene_id', 'gene_type', 'gene_name', 'level', 'tag',
    #   'transcript_id', 'transcript_type', 'transcript_name', 'exon_number',
    #   'exon_id', 'transcript_support_level', 'havana_transcript', 'hgnc_id',
    #   'havana_gene', 'ont', 'protein_id', 'ccdsid', 'artif_dupl'],

    # Map the gene names from transcript_quants_df to the z dataframe, converting the transcript_quants_df name to the gene_name based on the gene_id
    # marker_transcript_quants_df = marker_transcript_quants_df.merge(z, left_on="Name", right_on="gene_id", how="left")

    # Identify the number of genes overlapping our marker data

    # Next, let's convert the ENST to gene symbols
    # Load ENST to Gene mapping
    # enst_to_gene = pd.read_csv(enst_to_gene_mapping, sep="\t")
    # transcript_quants_df = transcript_quants_df.merge(enst_to_gene, on="Name", how="left")
    # if verbose:
    #    click.echo("\tENST to gene mapping.")
    #    click.echo(transcript_quants_df.head())

    # Next, let's filter out the lowly expressed transcripts

    # Next, let's normalize the transcript quants

    # Next, let's predict the tissue of origin

    # Next, let's save the results

    click.echo(f"\nTime elapsed: {time.time() - time_start:.2f} seconds")


if __name__ == "__main__":
    main.main(
        standalone_mode=False,
        args=[
            "--transcript-quants",
            "../quants-trial/quant.genes.sf",
            "--organism",
            "Homo sapiens",
            "--verbose",
            "--debug",
        ],
    )  # pragma: no cover
