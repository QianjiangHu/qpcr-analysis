import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure plots directory exists
os.makedirs("./plots/foldchange", exist_ok=True)

def app():
    """Fold Change Visualization"""
    st.title("📊 Fold Change Visualization")

    # Ensure fold change data exists
    if "fold_change_qPCR_df" not in st.session_state:
        st.error("❌ No fold change data available. Please compute ΔΔCt & Fold Change first.")
        st.stop()

    df_filtered = st.session_state["fold_change_qPCR_df"].copy()

    # Compute mean and standard deviation for Fold Change
    fold_change_summary = (
        df_filtered.groupby(["Group", "Gene"])
        .agg(Fold_Change_Mean=("Fold_Change", "mean"),
             Fold_Change_SD=("Fold_Change", "std"))
        .reset_index()
    )

    # Remove invalid values
    df_filtered.replace([float("inf"), -float("inf")], pd.NA, inplace=True)
    df_filtered.dropna(subset=["Group", "Fold_Change"], inplace=True)

    unique_genes = df_filtered["Gene"].unique()
    group_colors = sns.color_palette("husl", n_colors=len(df_filtered["Group"].unique()))

    for gene in unique_genes:
        plt.figure(figsize=(1.3 * len(df_filtered["Group"].unique()), 5))
        group_order = df_filtered["Group"].unique()

        sns.barplot(
            x="Group",
            y="Fold_Change_Mean",
            data=fold_change_summary[fold_change_summary["Gene"] == gene],
            palette=group_colors,
            edgecolor="black",
            linewidth=1.5,
            order=group_order,
            errorbar=None
        )

        sns.stripplot(
            x="Group",
            y="Fold_Change",
            data=df_filtered[df_filtered["Gene"] == gene],
            color="black",
            alpha=0.9,
            size=9,
            jitter=True,
            order=group_order
        )

        for index, row in fold_change_summary[fold_change_summary["Gene"] == gene].iterrows():
            plt.errorbar(
                x=group_order.tolist().index(row["Group"]),
                y=row["Fold_Change_Mean"],
                yerr=row["Fold_Change_SD"],
                fmt='none',
                ecolor='red', capsize=5, elinewidth=1.5
            )

        plt.xticks(rotation=45, fontsize=14, color="black")
        plt.yticks(fontsize=14, color="black")
        plt.axhline(y=1, color="gray", linestyle="--")
        plt.xlabel("")
        plt.ylabel(f"Fold Change of $\\it{{{gene}}}$", fontsize=16, color="black")
        plt.title(gene, fontsize=18, fontweight="bold", fontstyle="italic", color="black")

        plt.grid(False)
        sns.despine(top=True, right=True)

        ax = plt.gca()
        ax.spines["bottom"].set_linewidth(2)
        ax.spines["left"].set_linewidth(2)

        plot_path = f"./plots/foldchange/{gene}_FoldChange_plot.png"
        plt.savefig(plot_path, dpi=300, bbox_inches="tight")
        st.pyplot(plt)

        with open(plot_path, "rb") as file:
            st.download_button(
                label=f"📥 Download {gene} Fold Change Plot",
                data=file,
                file_name=f"{gene}_FoldChange_plot.png",
                mime="image/png"
            )
