import plotly.io as pio
import plotly.express as px
import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import pingouin as pg

from scipy.stats import spearmanr
from emma.ema import EmbeddingHandler

from emma.knn_analysis import (
    get_knn_alignment_scores,
    plot_knn_alignment_across_embedding_spaces,
    plot_knn_alignment_across_features,
    plot_class_mixing_heatmap,
)

# parameter for this script
figures_to_be_plotted = [  # 'Fig_A',
    # 'Fig_B',
    # 'Fig_C',
    "Fig_D"
]
output_dir = "figures/"
distance_metric = "cosine"


def paired_wilcoxon_test_penguin(all_results_df, embedding_1, embedding_2):
    """
    Performs a paired Wilcoxon test on the KNN fraction data for two embeddings.

    Parameters:
    - all_results_df: DataFrame containing KNN fraction results for each embedding.
    - embedding_1: The first embedding model to compare.
    - embedding_2: The second embedding model to compare.

    Returns:
    - Test statistic and p-value of the Wilcoxon signed-rank test.
    """
    # Filter the DataFrame for the two embeddings
    embedding_1_data = all_results_df[
        all_results_df["Embedding"] == embedding_1
    ]["Fraction"]
    embedding_2_data = all_results_df[
        all_results_df["Embedding"] == embedding_2
    ]["Fraction"]

    # Check if both embeddings have the same length (for paired test)
    if len(embedding_1_data) != len(embedding_2_data):
        raise ValueError(
            "The two embeddings must have the same number of data points for a paired test."
        )

    # Perform the paired Wilcoxon test
    results = pg.wilcoxon(
        embedding_1_data, embedding_2_data, alternative="greater"
    )

    return results["W-val"][0], results["p-val"][0], results["RBC"][0]


# Figure C
if "Fig_C" in figures_to_be_plotted:
    # values for k = 100
    classes = {
        "Cell.membrane": {
            "la": 0.81,
            "emma_cosine": 0.54,
            "emma_euclidean": 0.58,
        },
        "Cytoplasm": {"la": 0.81, "emma_cosine": 0.38, "emma_euclidean": 0.39},
        "Endoplasmic.reticulum": {
            "la": 0.70,
            "emma_cosine": 0.26,
            "emma_euclidean": 0.25,
        },
        "Golgi.apparatus": {
            "la": 0.33,
            "emma_cosine": 0.19,
            "emma_euclidean": 0.18,
        },
        "Lysosome/Vacuole": {
            "la": 0.12,
            "emma_cosine": 0.11,
            "emma_euclidean": 0.11,
        },
        "Mitochondrion": {
            "la": 0.88,
            "emma_cosine": 0.46,
            "emma_euclidean": 0.41,
        },
        "Nucleus": {"la": 0.90, "emma_cosine": 0.66, "emma_euclidean": 0.62},
        "Peroxisome": {
            "la": 0.17,
            "emma_cosine": 0.09,
            "emma_euclidean": 0.09,
        },
        "Plastid": {"la": 0.92, "emma_cosine": 0.70, "emma_euclidean": 0.66},
        "Extracellular": {
            "la": 0.95,
            "emma_cosine": 0.77,
            "emma_euclidean": 0.71,
        },
    }

    df = pd.DataFrame(classes).T.reset_index()
    df.columns = ["subcellular_localisation", "la", "cosine", "euclidean"]

    # correlation analysis
    corr, p_value = spearmanr(df["la"], df[distance_metric])

    # plot
    fig_C = px.scatter(
        df,
        x="la",
        y=distance_metric,
        # text="subcellular_localisation",
        color_discrete_sequence=["#303496"],
    )

    fig_C.update_traces(line_width=3, marker=dict(size=12))

    fig_C.update_layout(
        template="plotly_white",
        xaxis=dict(showline=True, linecolor="black", linewidth=3),
        yaxis=dict(showline=True, linecolor="black", linewidth=3),
        title=None,  # "Subcellular Localization",
        title_font=dict(size=26),
        xaxis_title="Accuracy reported by Stärk et al.",
        xaxis_title_font=dict(size=26),
        yaxis_title="Mean KNN feature alignment score",
        yaxis_title_font=dict(size=26),
        xaxis_tickfont=dict(size=26),
        yaxis_tickfont=dict(size=26),
        font={"family": "Arial", "color": "black"},
        margin=dict(l=10, r=10, t=10, b=10),
    )

    fig_C.write_image(
        output_dir + "fig_3_C.pdf", format="pdf", width=600, height=600
    )


fp_metadata = "examples/deeploc/data/deeploc_train_features.csv"
metadata = pd.read_csv(fp_metadata)
# rename subcellular localization column
sub_loc_abbreviation_mapping = {
    "Cell.membrane": "Mem",
    "Cytoplasm": "Cyt",
    "Endoplasmic.reticulum": "End",
    "Golgi.apparatus": "Gol",
    "Lysosome/Vacuole": "Lys",
    "Mitochondrion": "Mit",
    "Nucleus": "Nuc",
    "Peroxisome": "Per",
    "Plastid": "Pla",
    "Extracellular": "Ext",
}
metadata["Subcellular Localization"] = metadata["subcellular_location"].map(
    sub_loc_abbreviation_mapping
)


embedding_dir = "embeddings/"
models = {
    "Ankh": "ankh_base/layer_None/chopped_1022_overlap_300",
    "ESM2": "esm2_t36_3B_UR50D/layer_36/chopped_1022_overlap_300",
    "ProstT5": "Rostlab/ProstT5/layer_None/chopped_1022_overlap_300",
    "ProtT5": "Rostlab/prot_t5_xl_uniref50/layer_None/chopped_1022_overlap_300",
}


ema = EmbeddingHandler(sample_meta_data=metadata)
for model_alias, model_name in models.items():
    ema.add_emb_space(
        embeddings_source=embedding_dir + model_name,
        emb_space_name=model_alias,
    )

# Figure A
if ("Fig_A" in figures_to_be_plotted) or ("Fig_B" in figures_to_be_plotted):

    # correlation analysis

    knn_alignment_scores = get_knn_alignment_scores(
        ema,
        feature_column="Subcellular Localization",
        k_neighbors=100,
        distance_metric=distance_metric,
    )

    # Perform Wilcoxon tests for each pair and print the results
    w_stat, p_value, rbc = paired_wilcoxon_test_penguin(
        knn_alignment_scores, "ESM2", "ProstT5"
    )
    print(
        f"ESM2 vs ProstT5 - Test Statistic: {w_stat}, P-Value: {p_value}, Rank-biserial correlation: {rbc}"
    )

    w_stat, p_value, rbc = paired_wilcoxon_test_penguin(
        knn_alignment_scores, "Ankh", "ESM2"
    )
    print(
        f"Ankh vs ESM2 - Test Statistic: {w_stat}, P-Value: {p_value}, Rank-biserial correlation: {rbc}"
    )

    w_stat, p_value, rbc = paired_wilcoxon_test_penguin(
        knn_alignment_scores, "ProtT5", "Ankh"
    )
    print(
        f"ProtT5 vs Ankh - Test Statistic: {w_stat}, P-Value: {p_value}, Rank-biserial correlation: {rbc}"
    )

    if "Fig_A" in figures_to_be_plotted:
        fig_A = plot_knn_alignment_across_embedding_spaces(
            knn_alignment_scores,
            embedding_order=["ProstT5", "ESM2", "Ankh", "ProtT5"],
        )

        fig_A.update_layout(
            xaxis=dict(showline=True, linecolor="black", linewidth=3),
            yaxis=dict(showline=True, linecolor="black", linewidth=3),
            title=None,  # "Subcellular Localization",
            title_font=dict(size=26),
            # xaxis_title="X-Axis Label",
            xaxis_title_font=dict(size=26),
            yaxis_title="KNN feature <br> alignment scores",
            yaxis_title_font=dict(size=26),
            xaxis_tickfont=dict(size=26),
            yaxis_tickfont=dict(size=26),
            margin=dict(l=10, r=10, t=10, b=10),
        )

        fig_A.update_traces(line_width=3)

        fig_A.write_image(
            output_dir + "fig_3_A.pdf", format="pdf", width=600, height=400
        )

    if "Fig_B" in figures_to_be_plotted:

        fig_B = plot_knn_alignment_across_features(
            knn_alignment_scores,
            embedding_order=["ProstT5", "ESM2", "Ankh", "ProtT5"],
        )

        fig_B.update_layout(
            font={"color": "black"},
            title=None,  # "Subcellular Localization",
            title_font=dict(size=80),
            # xaxis_title="X-Axis Label",
            xaxis_title_font=dict(size=80),
            # yaxis_title="Y-Axis Label",
            yaxis_title_font=dict(size=80),
            xaxis=dict(
                ticklabelposition="outside",
                tickfont=dict(size=80),
                automargin=True,
            ),
            yaxis=dict(
                ticklabelposition="outside",
                ticklabelstandoff=20,
                tickfont=dict(size=80),
                automargin=True,
            ),
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            shapes=[
                dict(
                    type="rect",
                    x0=0,
                    y0=0,
                    x1=1,
                    y1=1,
                    xref="paper",
                    yref="paper",
                    line=dict(color="black", width=5),
                )
            ],
        )

        fig_B.update_traces(textfont=dict(size=80))

        # saved as png for now due to problems of blury pdfs
        fig_B.write_image(
            output_dir + "fig_3_B.png",
            format="png",
            width=2400,
            height=2800,
        )


# Figure D
if "Fig_D" in figures_to_be_plotted:

    fig_D = plot_class_mixing_heatmap(
        ema,
        embedding_space="ProtT5",
        feature="Subcellular Localization",
        k_neighbors=100,
        distance_metric=distance_metric,
    )

    fig_D.update_layout(
        title=None,  # "Subcellular Localization",
        title_font=dict(size=80),
        # xaxis_title="X-Axis Label",
        xaxis_title_font=dict(size=80),
        # yaxis_title="Y-Axis Label",
        yaxis_title_font=dict(size=80),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_colorbar=dict(tickformat=".0f"),
        xaxis=dict(
            ticklabelposition="outside",
            tickfont=dict(size=80),
            tickangle=0,
            automargin=True,
        ),
        yaxis=dict(
            ticklabelposition="outside",
            ticklabelstandoff=30,
            tickfont=dict(size=80),
            automargin=True,
        ),
        shapes=[
            dict(
                type="rect",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                xref="paper",
                yref="paper",
                line=dict(color="black", width=5),
            )
        ],
    )
    fig_D.update_traces(textfont=dict(size=70), texttemplate="%{z:.0f}")

    fig_D.write_image(
        output_dir + "fig_3_D.png", format="png", width=4000, height=2400
    )


print()
# check how to export in high quality
