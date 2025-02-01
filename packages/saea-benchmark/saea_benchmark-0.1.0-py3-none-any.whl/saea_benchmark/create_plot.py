from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scanpy import read_h5ad
from scipy.stats import entropy


def jensen_shannon_divergence(p, q):
    p = np.asarray(p)
    q = np.asarray(q)
    p = p / np.sum(p)
    q = q / np.sum(q)
    m = (p + q) / 2

    # JS divergence
    # JS = 0.5 * (KL(P||M) + KL(Q||M))
    divergence = 0.5 * (entropy(p, m) + entropy(q, m))

    return divergence


def prepare_data(
    full_adata_path: str, split_df_path: str, experiment_json_path: str | None = None
):
    full_adata = read_h5ad(full_adata_path)
    split_df = pd.read_csv(split_df_path, index_col=0)
    full_label_dist = full_adata.obs["y"].value_counts(normalize=True)
    label_index = full_adata.obs["y"].cat.categories
    folds = {}

    for fold_idx in split_df["cluster"].unique():
        fold = split_df[split_df["cluster"] == fold_idx]
        fold_accessions = set(fold["AC"].to_list())
        mask = full_adata.obs["accession"].isin(fold_accessions)
        fold_label_dist = full_adata.obs["y"].loc[mask].value_counts(normalize=True)
        folds[fold_idx] = {
            "size": mask.sum() / len(full_adata),
            "2d": full_adata.obsm["X_tsne"][mask],
            "label_dist": fold_label_dist,
            "js_div": jensen_shannon_divergence(full_label_dist, fold_label_dist),
        }

    if experiment_json_path is not None:
        with open(experiment_json_path, "r") as f:
            exp_results = json.load(f)
        threshold = exp_results.get("threshold", "N/A")
        metric = exp_results.get("metric", "N/A")
        seed = exp_results.get("seed", "N/A")

        under_threshold = [
            round(exp_results[str(idx)].get("under_threshold", "N/A"), 3)
            if exp_results[str(idx)].get("under_threshold", "N/A") != "N/A"
            else "N/A"
            for idx in folds
        ]

        best_validation_score = [
            round(exp_results[str(idx)].get("best_validation_score", "N/A"), 3)
            if exp_results[str(idx)].get("best_validation_score", "N/A") != "N/A"
            else "N/A"
            for idx in folds
        ]

        test_score = [
            round(exp_results[str(idx)].get("test_score", "N/A"), 3)
            if exp_results[str(idx)].get("test_score", "N/A") != "N/A"
            else "N/A"
            for idx in folds
        ]
    else:
        threshold = "N/A"
        metric = "N/A"
        seed = "N/A"
        under_threshold = ["N/A"] * len(folds)
        best_validation_score = ["N/A"] * len(folds)
        test_score = ["N/A"] * len(folds)

    sizes = [round(folds[idx]["size"], 3) for idx in folds]
    js_div = [round(folds[idx]["js_div"], 3) for idx in folds]
    table_list = [
        [
            "Fold",
            "Size",
            "% < thresh\n(↑)",
            "JS div\n(↓)",
            "Valid\nScore",
            "Test\nScore",
        ],
        *zip(
            range(len(folds)),
            sizes,
            under_threshold,
            js_div,
            best_validation_score,
            test_score,
        ),
    ]
    return folds, full_label_dist, table_list, label_index, threshold, metric, seed


def create_tsne_plot(ax, folds, dataset_name, alpha):
    """Create t-SNE visualization plot."""
    for key in folds.keys():
        ax.scatter(
            folds[key]["2d"][:, 0],
            folds[key]["2d"][:, 1],
            label=f"Fold {key}",
            alpha=alpha,
        )
    ax.legend()
    ax.set_title(
        "t-SNE visualizations of folds\nSplit by SAEA, " + f"Dataset: {dataset_name}"
    )
    ax.axis("off")


def create_metrics_table(
    ax, table_list, threshold, metric, seed, table_col_widths, font_size, scale
):
    """Create metrics table."""
    table = ax.table(cellText=table_list, loc="center", colWidths=table_col_widths)
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    table.scale(*scale)

    # Center align all cell text
    for cell in table._cells.values():
        cell.set_text_props(ha="center", va="center")

    ax.set_title(
        f"Size, similarity and label divergence metric\n\n"
        f"Threshold = {threshold}, Score = {metric}, Seed = {seed}"
    )
    ax.axis("off")

    return table


def create_distribution_plot(ax, full_label_dist, folds, label_index, bar_width, alpha):
    """Create distribution bar plot."""
    x = np.arange(len(full_label_dist))

    # Plot full dataset distribution
    ax.bar(x, full_label_dist.values, bar_width, alpha=alpha, label="Full Dataset")

    # Plot fold distributions
    for fold_idx in folds.keys():
        dist = folds[fold_idx]["label_dist"].values
        ax.bar(
            x + bar_width * (fold_idx + 1), dist, bar_width, label=f"Fold {fold_idx}"
        )

    # Set x-axis ticks and labels
    n_folds = len(folds.keys())
    tick_positions = x + bar_width * (n_folds / 2)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(label_index, rotation=45)

    # Set labels and title
    ax.set_title("Distribution of folds")
    ax.set_xlabel("Class")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize="x-small")


def visualize_fold_analysis(
    full_adata_path: str,
    split_df_path: str,
    dataset_name: str,
    experiment_json_path: str | None = None,
    figsize: tuple[int, int] = (14, 6),
    width_ratios: tuple[float] = (0.5, 0.5),
    scatter_alpha: float = 0.5,
    table_col_widths: tuple[float] = (0.15, 0.25, 0.3, 0.3, 0.3, 0.3),
    table_font_size: int = 12,
    table_scale: tuple[float] = (0.65, 6),
    bar_alpha: float = 0.7,
    bar_width: float = 0.25,
    dpi: int = 300,
    save_path: str | None = None,
):
    """Main function to create the complete visualization."""
    (
        folds,
        full_label_dist,
        table_list,
        label_index,
        threshold,
        metric,
        seed,
    ) = prepare_data(full_adata_path, split_df_path, experiment_json_path)

    # Create figure and grid
    plt.rcParams["figure.dpi"] = dpi
    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(1, 2, width_ratios=width_ratios)
    gs.update(wspace=0.1, hspace=0.1)

    # Create left plot (t-SNE)
    ax_left = plt.subplot(gs[0])
    create_tsne_plot(ax_left, folds, dataset_name, scatter_alpha)

    # Create right plots (table and distribution)
    ax_right = plt.subplot(gs[1])
    create_metrics_table(
        ax_right,
        table_list,
        threshold,
        metric,
        seed,
        table_col_widths,
        table_font_size,
        table_scale,
    )

    # Create bottom right plot (distribution)
    divider = make_axes_locatable(ax_right)
    ax_bottom_right = divider.append_axes(
        "bottom", size="100%", pad=0.1, sharex=ax_right
    )
    create_distribution_plot(
        ax_bottom_right, full_label_dist, folds, label_index, bar_width, bar_alpha
    )

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight", dpi=dpi)
    return fig
