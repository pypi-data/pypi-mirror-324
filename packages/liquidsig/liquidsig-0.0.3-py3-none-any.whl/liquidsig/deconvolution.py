"""
Perform hierarchical deconvolution of cfRNA data to estimate tissue and cell type proportions.
"""

# Third party modules
import pandas as pd
import numpy as np
from scipy.optimize import nnls
from scipy.stats import pearsonr
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.rcParams["figure.max_open_warning"] = (
    0  # Suppress warning about too many open figures
)


class HeirarchicalDeconvolution:
    """Perform hierarchical deconvolution of cfRNA data."""

    def __init__(
        self,
        mixture_data: pd.DataFrame,
        training_data: pd.DataFrame,
        top_tissue_markers: int = 50,
        top_cell_markers: int = 30,
        generate_detailed_figures: bool = False,
        verbose: bool = False,
    ):
        """Initialize the HeirarchicalDeconvolution class.

        Args
        ----
            mixture_data (pd.DataFrame): DataFrame containing mixture RNA-seq data with columns 'GeneName' and 'TPM'.
            training_data (pd.DataFrame): DataFrame containing training data with columns
                                          'Tissue', 'Cell', 'GeneName', 'GeneMarkerScore',
                                          'GeneMeanExpression', 'GenePercentExpressing'.
            top_tissue_markers (int): Number of top marker genes to use for tissue deconvolution.
            top_cell_markers (int): Number of top marker genes to use for cell deconvolution within each tissue.
            generate_detailed_figures (bool): Whether to generate detailed figures for cell deconvolution.
            verbose (bool): Whether to print verbose output.

        Raises
        ------
            ValueError: If required columns are missing in the input data.

        Returns
        -------
            None
        """

        self.mixture_data = mixture_data
        self.training_data = training_data
        self.top_tissue_markers = top_tissue_markers
        self.top_cell_markers = top_cell_markers
        self.generate_detailed_figures = generate_detailed_figures
        self.verbose = verbose

        # Validate input data
        assert isinstance(self.mixture_data, pd.DataFrame)
        assert isinstance(self.training_data, pd.DataFrame)
        assert self.top_cell_markers > 0
        assert self.top_tissue_markers > 0

        self.validate_deconvolution_input()

        self.tissue_list = self.training_data["Tissue"].unique()

        # Store results
        self.tissue_proportion_df = None

        self.tissue_internals = {
            "tissue_marker_expression_df": None,
            "mixture_tissue_expression_vector": None,
            "reconstructed_tissue_expression": None,
        }

        self.tissue_stats = {}

        self.tissue_figures = {
            "proportion": None,
            "scatter": None,
            "marker_heatmap": None,
            "residual": None,
        }

        # Store the results of cell deconvolution in a single df
        self.cell_proportion_df = None

        # TODO: Change this dict to have tissue be the key?
        self.cell_stats = {"r2": {}, "rmse": {}, "pearson_r": {}}

        # This is a dict of each cell type, each of which contains a dict of internals
        self.cell_internals = {}

        self.cell_proportion_figures_dict = {}
        self.cell_scatter_figures_dict = {}
        self.cell_marker_heatmap_figures_dict = {}
        self.cell_residual_figures_dict = {}

    def validate_deconvolution_input(self):
        """
        Validate the input data for deconvolution.

        Raises:
            ValueError: If required columns are missing in the input data.
        """

        required_columns_mixture = ["GeneName", "TPM"]
        if not set(required_columns_mixture).issubset(self.mixture_data.columns):
            raise ValueError(
                f"Mixture data must contain columns: {required_columns_mixture}"
            )

        required_columns_training = [
            "Tissue",
            "Cell",
            "GeneName",
            "GeneMarkerScore",
            "GeneMeanExpression",
            "GenePercentExpressing",
        ]
        if not set(required_columns_training).issubset(self.training_data.columns):
            raise ValueError(
                f"Training data must contain columns: {required_columns_training}"
            )

    def tissue_level_deconvolution(self):
        """
        Perform tissue-level deconvolution using marker genes from the training data.

        This method:
        1. Identifies top marker genes for each tissue
        2. Creates reference expression matrices
        3. Performs non-negative least squares optimization
        4. Calculates tissue proportions and quality metrics

        The results are stored in class attributes:
        - tissue_proportion_df: DataFrame with tissue proportions
        - tissue_stats: Dictionary containing r2, rmse, and pearson_r statistics
        - tissue_internals: Dictionary containing intermediate calculation results

        Raises:
            ValueError: If no overlapping marker genes are found between training and mixture data
        """
        print("Starting tissue-level deconvolution...")

        print(f"\tNumber of Tissues: {len(self.tissue_list)}")
        tissue_marker_expression_profiles = {}
        tissue_markers = {}

        # Subset to the top marker genes for each tissue (based on top_tissue_markers)
        for tissue in self.tissue_list:
            tissue_specific_markers = (
                self.training_data[self.training_data["Tissue"] == tissue]
                .sort_values("GeneMarkerScore", ascending=False)
                .drop_duplicates(subset=["GeneName"])
            )

            top_markers = tissue_specific_markers.head(self.top_tissue_markers)
            tissue_markers[tissue] = top_markers["GeneName"].tolist()
            tissue_marker_expression_profiles[tissue] = top_markers.set_index(
                "GeneName"
            )["GeneMeanExpression"].to_dict()

        # Ensure we have overlap of the top marker genes between training and mixture data
        tissue_marker_genes = list(
            set(gene for markers in tissue_markers.values() for gene in markers)
        )
        tissue_marker_genes_intersection = list(
            set(tissue_marker_genes) & set(self.mixture_data["GeneName"])
        )
        if not tissue_marker_genes_intersection:
            raise ValueError(
                "No overlapping marker genes found between training and mixture data for tissue deconvolution."
            )

        # Prepare the reference tissue expression matrix
        reference_tissue_expression = []
        tissue_names_for_matrix = []
        for tissue in self.tissue_list:
            profile = tissue_marker_expression_profiles[tissue]
            expression_vector = [
                profile.get(gene, 0) for gene in tissue_marker_genes_intersection
            ]
            reference_tissue_expression.append(expression_vector)
            tissue_names_for_matrix.append(tissue)

        # Prepare the matrices for constrained least squares
        reference_tissue_expression_matrix = np.array(reference_tissue_expression).T
        # Extract the mixture expression vector for the marker genes, filling with 0 if gene not present
        self.tissue_internals["mixture_tissue_expression_vector"] = np.array(
            [
                (
                    self.mixture_data[self.mixture_data["GeneName"] == gene][
                        "TPM"
                    ].iloc[0]
                    if gene in self.mixture_data["GeneName"].values
                    else 0
                )
                for gene in tissue_marker_genes_intersection
            ]
        )

        self.tissue_internals["tissue_marker_expression_df"] = pd.DataFrame(
            reference_tissue_expression_matrix,
            index=tissue_marker_genes_intersection,
            columns=tissue_names_for_matrix,
        )

        # Constrained Least Squares for Tissue Deconvolution
        # NNLS seems to outperform L-BFGS-B and SLSQP for our use case
        tissue_proportions, residuals = nnls(
            reference_tissue_expression_matrix,
            self.tissue_internals["mixture_tissue_expression_vector"],
        )
        tissue_proportions_normalized = (
            tissue_proportions / tissue_proportions.sum()
            if tissue_proportions.sum() > 0
            else tissue_proportions
        )

        # Use the NNLS residuals to calculate the proportion of unexplained variance -- this is not the same as R-squared, but a useful metric for NNLS
        # Note we are not comparing the same values -- specifically we have TPM data from our mixture, but mean expression data from our training data
        # TODO: Consider normalizing the data before calculating residuals or fitting the model?
        total_variance = np.sum(
            (
                self.tissue_internals["mixture_tissue_expression_vector"]
                - np.mean(self.tissue_internals["mixture_tissue_expression_vector"])
            )
            ** 2
        )
        unexplained_variance = np.sum(residuals**2)
        proportion_unexplained_variance = unexplained_variance / total_variance
        print(
            f"\tProportion of Unexplained Variance: {proportion_unexplained_variance:.3f}"
        )

        tissue_proportion_df = pd.DataFrame(
            {
                "Tissue": tissue_names_for_matrix,
                "Proportion": tissue_proportions_normalized,
            }
        )

        # Calculate Statistics for tissue deconvolution
        self.tissue_internals["reconstructed_tissue_expression"] = (
            reference_tissue_expression_matrix @ tissue_proportions
        )
        tissue_r2 = r2_score(
            self.tissue_internals["mixture_tissue_expression_vector"],
            self.tissue_internals["reconstructed_tissue_expression"],
        )
        tissue_rmse = np.sqrt(
            mean_squared_error(
                self.tissue_internals["mixture_tissue_expression_vector"],
                self.tissue_internals["reconstructed_tissue_expression"],
            )
        )
        tissue_pearson_r, _ = pearsonr(
            self.tissue_internals["mixture_tissue_expression_vector"],
            self.tissue_internals["reconstructed_tissue_expression"],
        )

        # Store results
        self.tissue_proportion_df = tissue_proportion_df
        self.tissue_stats["r2"] = tissue_r2
        self.tissue_stats["rmse"] = tissue_rmse
        self.tissue_stats["pearson_r"] = tissue_pearson_r

        for metric, value in self.tissue_stats.items():
            print(f"\t{metric.upper()}: {value:.3f}")
        print()

        print("Completed tissue deconvolution.\n")

    def cell_level_deconvolution(self):
        """
        Perform cell-level deconvolution within each tissue using marker genes.

        This method performs deconvolution for each tissue separately to estimate
        the proportions of different cell types within that tissue. Results are stored
        in class attributes:
        - cell_proportion_df: DataFrame with columns 'Tissue', 'Cell', and 'Proportion'
        - cell_stats: Dictionary containing r2, rmse, and pearson_r statistics per tissue
        - cell_internals: Dictionary containing intermediate calculation results per tissue

        The method handles cases where marker genes may not be present in the mixture data
        and skips tissues where deconvolution cannot be performed.

        Note:
            Cell proportions are normalized within each tissue independently.
        """

        for tissue in self.tissue_list:
            print(f"Cell-level deconvoluting: {tissue}")

            # We store the internals of each cell-level deconvolution, but since the same cell type
            # can exist in multiple different tissues (with different internals), we need a nested dict.
            self.cell_internals[tissue] = {}

            self.cell_internals[tissue]["cells_in_tissue"] = self.training_data[
                self.training_data["Tissue"] == tissue
            ]["Cell"].unique()

            # Let's get the top marker genes & their expression profiles for each cell type in this tissue
            cell_marker_expression_profiles = {}
            cell_markers = {}

            for cell in self.cell_internals[tissue]["cells_in_tissue"]:
                # Add the internals for this cell to the nested dict

                cell_specific_markers = (
                    self.training_data[
                        (self.training_data["Tissue"] == tissue)
                        & (self.training_data["Cell"] == cell)
                    ]
                    .sort_values("GeneMarkerScore", ascending=False)
                    .drop_duplicates(subset=["GeneName"])
                )

                top_markers = cell_specific_markers.head(self.top_cell_markers)
                cell_markers[cell] = top_markers["GeneName"].tolist()
                cell_marker_expression_profiles[cell] = top_markers.set_index(
                    "GeneName"
                )["GeneMeanExpression"].to_dict()

            cell_marker_genes = list(
                set(gene for markers in cell_markers.values() for gene in markers)
            )

            cell_marker_genes_intersection = list(
                set(cell_marker_genes) & set(self.mixture_data["GeneName"])
            )

            # TODO: Think if it's even possible to have no overlapping marker genes
            if not cell_marker_genes_intersection:
                print(
                    f"Warning: No overlapping marker genes found for cell deconvolution in Tissue: {tissue}. Skipping this tissue."
                )
                self.cell_internals[tissue]["cell_proportions_dict"] = pd.DataFrame(
                    {
                        "Cell": self.cell_internals[tissue]["cells_in_tissue"],
                        "Proportion": np.nan,
                    }
                )
                self.cell_stats[tissue] = {
                    "r2": np.nan,
                    "rmse": np.nan,
                    "pearson_r": np.nan,
                }
                continue

            reference_cell_expression = []
            for cell in self.cell_internals[tissue]["cells_in_tissue"]:
                profile = cell_marker_expression_profiles[cell]
                expression_vector = [
                    profile.get(gene, 0) for gene in cell_marker_genes_intersection
                ]
                reference_cell_expression.append(expression_vector)

            reference_cell_expression_matrix = np.array(reference_cell_expression).T
            self.cell_internals[tissue][
                "reference_cell_expression_matrix"
            ] = reference_cell_expression_matrix

            # Store this as a DataFrame for visualization later on
            self.cell_internals[tissue]["cell_marker_expression_df"] = pd.DataFrame(
                reference_cell_expression_matrix,
                index=cell_marker_genes_intersection,
                columns=self.cell_internals[tissue]["cells_in_tissue"],
            )

            mixture_cell_expression_vector = np.array(
                [
                    (
                        self.mixture_data[self.mixture_data["GeneName"] == gene][
                            "TPM"
                        ].iloc[0]
                        if gene in self.mixture_data["GeneName"].values
                        else 0
                    )
                    for gene in cell_marker_genes_intersection
                ]
            )
            self.cell_internals[tissue][
                "mixture_cell_expression_vector"
            ] = mixture_cell_expression_vector

            # Constrained Least Squares for Cell Deconvolution
            cell_proportions, _ = nnls(
                reference_cell_expression_matrix, mixture_cell_expression_vector
            )
            cell_proportions_normalized = (
                cell_proportions / cell_proportions.sum()
                if cell_proportions.sum() > 0
                else cell_proportions
            )

            self.cell_internals[tissue]["cell_proportions_dict"] = pd.DataFrame(
                {
                    "Tissue": [tissue]
                    * len(self.cell_internals[tissue]["cells_in_tissue"]),
                    "Cell": self.cell_internals[tissue]["cells_in_tissue"],
                    "Proportion": cell_proportions_normalized,
                }
            )

            # Calculate Statistics for cell-level deconvolution
            reconstructed_cell_expression = (
                reference_cell_expression_matrix @ cell_proportions
            )
            self.cell_internals[tissue][
                "reconstructed_cell_expression"
            ] = reconstructed_cell_expression
            self.cell_stats[tissue] = {}

            self.cell_stats[tissue]["r2"] = r2_score(
                mixture_cell_expression_vector, reconstructed_cell_expression
            )
            self.cell_stats[tissue]["rmse"] = np.sqrt(
                mean_squared_error(
                    mixture_cell_expression_vector, reconstructed_cell_expression
                )
            )
            self.cell_stats[tissue]["pearson_r"], _ = pearsonr(
                mixture_cell_expression_vector, reconstructed_cell_expression
            )

            if self.verbose:
                # Print our stats
                print("\t", end="")
                print(
                    ", ".join(
                        [
                            f"{metric.upper()}: {value:.3f}"
                            for metric, value in self.cell_stats[tissue].items()
                        ]
                    )
                )
                print()

        # Aggregate all of the different tissues in self.cell_internals[tissue]['cell_proportions_dict'] into a single DataFrame
        self.cell_proportion_df = pd.concat(
            [
                self.cell_internals[tissue]["cell_proportions_dict"]
                for tissue in self.tissue_list
            ]
        )

        print("Cell deconvolutions complete.")

    def generate_tissue_figures(self):
        """
        Generate visualization figures for tissue-level deconvolution results.

        Creates and stores the following figures in the tissue_figures dictionary:
        - proportion: Bar plot of estimated tissue proportions
        - scatter: Scatter plot of reconstructed vs original expression
        - marker_heatmap: Heatmap of marker gene expression across tissues
        - residual: Residual plot for quality assessment

        Each figure is stored as a matplotlib Figure object in the tissue_figures
        dictionary using the corresponding key.
        """
        # Tissue Proportion Bar Plot (same as before)
        tissue_fig_prop, ax_tissue_prop = plt.subplots(figsize=(10, 12))
        sns.barplot(
            x="Proportion",
            y="Tissue",
            data=self.tissue_proportion_df.sort_values("Proportion", ascending=False),
            hue="Tissue",
            dodge=False,
            legend=False,
            palette="viridis",
            ax=ax_tissue_prop,
        )
        ax_tissue_prop.set_title("Estimated Tissue Proportions")
        ax_tissue_prop.set_xlabel("Proportion")
        ax_tissue_prop.set_ylabel("Tissue")
        tissue_fig_prop.tight_layout()
        self.tissue_figures["proportion"] = tissue_fig_prop

        # Tissue Scatter Plot (Reconstructed vs. Original)
        tissue_fig_scatter, ax_tissue_scatter = plt.subplots(figsize=(8, 8))
        sns.scatterplot(
            x=self.tissue_internals["mixture_tissue_expression_vector"],
            y=self.tissue_internals["reconstructed_tissue_expression"],
            ax=ax_tissue_scatter,
        )
        ax_tissue_scatter.set_xlabel("Original Mixture Expression (Marker Genes)")
        ax_tissue_scatter.set_ylabel("Reconstructed Tissue Expression (Marker Genes)")
        ax_tissue_scatter.set_title("Tissue Deconvolution: Reconstructed vs. Original")
        ax_tissue_scatter.plot(
            [
                min(self.tissue_internals["mixture_tissue_expression_vector"]),
                max(self.tissue_internals["mixture_tissue_expression_vector"]),
            ],
            [
                min(self.tissue_internals["mixture_tissue_expression_vector"]),
                max(self.tissue_internals["mixture_tissue_expression_vector"]),
            ],
            color="red",
            linestyle="--",
        )  # Diagonal line
        tissue_fig_scatter.tight_layout()
        self.tissue_figures["scatter"] = tissue_fig_scatter

        # Tissue Marker Heatmap
        tissue_marker_heatmap_fig, ax_tissue_heatmap = plt.subplots(figsize=(10, 10))
        sns.heatmap(
            self.tissue_internals["tissue_marker_expression_df"],
            cmap="viridis",
            ax=ax_tissue_heatmap,
            cbar_kws={"label": "Mean Expression"},
        )
        ax_tissue_heatmap.set_title("Tissue Marker Gene Expression Heatmap")
        ax_tissue_heatmap.set_xlabel("Tissues")
        ax_tissue_heatmap.set_ylabel("Marker Genes")
        tissue_marker_heatmap_fig.tight_layout()
        self.tissue_figures["marker_heatmap"] = tissue_marker_heatmap_fig

        # Tissue Residual Plot
        tissue_fig_residual, ax_tissue_residual = plt.subplots(figsize=(8, 8))
        residuals_tissue = (
            self.tissue_internals["reconstructed_tissue_expression"]
            - self.tissue_internals["mixture_tissue_expression_vector"]
        )
        sns.scatterplot(
            x=self.tissue_internals["mixture_tissue_expression_vector"],
            y=residuals_tissue,
            ax=ax_tissue_residual,
        )
        ax_tissue_residual.axhline(0, color="red", linestyle="--")  # Zero line
        ax_tissue_residual.set_xlabel("Original Mixture Expression (Marker Genes)")
        ax_tissue_residual.set_ylabel("Residuals (Reconstructed - Original)")
        ax_tissue_residual.set_title("Tissue Deconvolution: Residual Plot")
        tissue_fig_residual.tight_layout()
        self.tissue_figures["residual"] = tissue_fig_residual

        print("Tissue figures generated.")

    def generate_cell_figures(self):
        """
        Generate visualization figures for cell-level deconvolution results.

        Creates separate figures for each tissue, storing them in dictionaries:
        - cell_proportion_figures_dict: Bar plots of cell proportions per tissue
        - cell_scatter_figures_dict: Scatter plots of reconstructed vs original expression
        - cell_marker_heatmap_figures_dict: Heatmaps of marker gene expression
        - cell_residual_figures_dict: Residual plots for quality assessment

        Note:
            This method is experimental and only generates figures when
            generate_detailed_figures is True and valid results exist for a tissue.
        """
        generate_detailed_figures = False

        cell_proportion_figures_dict = {}
        cell_scatter_figures_dict = {}
        cell_marker_heatmap_figures_dict = {}
        cell_residual_figures_dict = {}

        for tissue in self.tissue_list:
            cell_props_tissue = self.cell_internals[tissue]["cell_proportions_dict"]
            if (
                cell_props_tissue is not None
                and not cell_props_tissue["Proportion"].isnull().all()
                and generate_detailed_figures
            ):
                cell_props_tissue_valid = cell_props_tissue.dropna(
                    subset=["Proportion"]
                ).sort_values("Proportion", ascending=False)

                # Cell Proportion Bar Plot
                cell_fig_prop, ax_cell_prop = plt.subplots(figsize=(8, 8))
                sns.barplot(
                    x="Proportion",
                    y="Cell",
                    data=cell_props_tissue_valid,
                    hue="Cell",
                    dodge=False,
                    legend=False,
                    palette="viridis",
                    ax=ax_cell_prop,
                )
                ax_cell_prop.set_title(f"Cell Proportions within {tissue} Tissue")
                ax_cell_prop.set_xlabel("Proportion")
                ax_cell_prop.set_ylabel("Cell Type")
                cell_fig_prop.tight_layout()
                cell_proportion_figures_dict[tissue] = cell_fig_prop

                # Cell Scatter Plot (Reconstructed vs. Original)
                cell_fig_scatter, ax_cell_scatter = plt.subplots(figsize=(8, 8))

                sns.scatterplot(
                    x=self.cell_internals[tissue]["mixture_cell_expression_vector"],
                    y=self.cell_internals[tissue]["reconstructed_cell_expression"],
                    ax=ax_cell_scatter,
                )
                ax_cell_scatter.set_xlabel("Original Mixture Expression (Marker Genes)")
                ax_cell_scatter.set_ylabel(
                    "Reconstructed Cell Expression (Marker Genes)"
                )
                ax_cell_scatter.set_title(
                    f"Cell Deconvolution in {tissue}: Reconstructed vs. Original"
                )
                ax_cell_scatter.plot(
                    [
                        min(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                        max(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                    ],
                    [
                        min(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                        max(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                    ],
                    color="red",
                    linestyle="--",
                )  # Diagonal line
                cell_fig_scatter.tight_layout()
                cell_scatter_figures_dict[tissue] = cell_fig_scatter

                # Cell Marker Heatmap
                cell_marker_heatmap_fig, ax_cell_heatmap = plt.subplots(figsize=(8, 8))
                sns.heatmap(
                    self.cell_internals[tissue]["cell_marker_expression_df"],
                    cmap="viridis",
                    ax=ax_cell_heatmap,
                    cbar_kws={"label": "Mean Expression"},
                )
                ax_cell_heatmap.set_title(
                    f"Cell Marker Gene Expression Heatmap in {tissue}"
                )
                ax_cell_heatmap.set_xlabel("Cell Types")
                ax_cell_heatmap.set_ylabel("Marker Genes")
                cell_marker_heatmap_fig.tight_layout()
                cell_marker_heatmap_figures_dict[tissue] = cell_marker_heatmap_fig

                # Cell Residual Plot
                cell_fig_residual, ax_cell_residual = plt.subplots(figsize=(8, 8))
                residuals_cell = (
                    self.cell_internals[tissue]["reconstructed_cell_expression"]
                    - self.cell_internals[tissue]["mixture_cell_expression_vector"]
                )
                sns.scatterplot(
                    x=self.cell_internals[tissue]["mixture_cell_expression_vector"],
                    y=residuals_cell,
                    ax=ax_cell_residual,
                )
                ax_cell_residual.axhline(0, color="red", linestyle="--")  # Zero line
                ax_cell_residual.set_xlabel(
                    "Original Mixture Expression (Marker Genes)"
                )
                ax_cell_residual.set_ylabel("Residuals (Reconstructed - Original)")
                ax_cell_residual.set_title(
                    f"Cell Deconvolution in {tissue}: Residual Plot"
                )
                cell_fig_residual.tight_layout()
                cell_residual_figures_dict[tissue] = cell_fig_residual

            else:
                cell_proportion_figures_dict[tissue] = None
                cell_scatter_figures_dict[tissue] = None
                cell_marker_heatmap_figures_dict[tissue] = None
                cell_residual_figures_dict[tissue] = None

        self.cell_proportion_figures_dict = cell_proportion_figures_dict
        self.cell_scatter_figures_dict = cell_scatter_figures_dict
        self.cell_marker_heatmap_figures_dict = cell_marker_heatmap_figures_dict
        self.cell_residual_figures_dict = cell_residual_figures_dict

        print("Cell figures generated.")

    def run(self):
        """
        Execute the complete hierarchical deconvolution pipeline.

        This method runs the full analysis pipeline in sequence:
        1. Validates input data
        2. Performs tissue-level deconvolution
        3. Performs cell-level deconvolution
        4. Generates visualization figures

        Returns:
            tuple: Contains:
                - pd.DataFrame: Tissue proportion results
                - dict: Tissue deconvolution statistics (r2, rmse, pearson_r)
                - dict: Tissue visualization figures
        """

        self.validate_deconvolution_input()

        self.tissue_level_deconvolution()

        self.cell_level_deconvolution()

        self.generate_tissue_figures()

        # Not fully implemented yet
        self.generate_cell_figures()

        return (
            self.tissue_proportion_df,
            self.tissue_stats,
            self.tissue_figures,
            self.cell_proportion_df,
            self.cell_stats,
            self.cell_proportion_figures_dict,
            self.cell_scatter_figures_dict,
            self.cell_marker_heatmap_figures_dict,
            self.cell_residual_figures_dict,
        )
