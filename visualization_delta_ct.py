import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure plots directory exists
os.makedirs("./plots/deltaCT", exist_ok=True)

def app():
    """-ΔCt Visualization"""
    st.title("📊 -ΔCt Visualization")

    # Ensure normalized data exists
    if "normalized_qPCR_df" not in st.session_state:
        st.error("❌ No normalized qPCR data available. Please compute ΔCt first.")
        st.stop()

    df_filtered = st.session_state["normalized_qPCR_df"].copy()
    
    # Compute -ΔCt for visualization
    df_filtered["Neg_Delta_Ct"] = -df_filtered["Normalized_Cq"]
    
    # Remove invalid values
    df_filtered.replace([float("inf"), -float("inf")], pd.NA, inplace=True)
    df_filtered.dropna(subset=["Group", "Neg_Delta_Ct"], inplace=True)

    # Get unique genes
    unique_genes = df_filtered["Gene"].unique()
    group_colors = sns.color_palette("husl", n_colors=len(df_filtered["Group"].unique()))

    # Generate plots for each gene
    for gene in unique_genes:
        plt.figure(figsize=(1.3 * len(df_filtered["Group"].unique()), 5))
        group_order = df_filtered["Group"].unique()

        sns.boxplot(
            x="Group",
            y="Neg_Delta_Ct",
            data=df_filtered[df_filtered["Gene"] == gene],
            palette=group_colors,
            width=0.18 * len(df_filtered["Group"].unique()),
            showcaps=True,
            boxprops={'edgecolor': 'black', 'linewidth': 1.5},
            order=group_order
        )

        sns.stripplot(
            x="Group",
            y="Neg_Delta_Ct",
            data=df_filtered[df_filtered["Gene"] == gene],
            color="black",
            alpha=0.9,
            size=9,
            jitter=True,
            order=group_order
        )

        plt.xticks(rotation=45, fontsize=14, color="black")
        plt.yticks(fontsize=14, color="black")
        plt.xlabel("")
        plt.ylabel(f"Expression of $\\it{{{gene}}}$", fontsize=16, color="black")
        plt.title(gene, fontsize=18, fontweight="bold", fontstyle="italic", color="black")

        plt.grid(False)
        sns.despine(top=True, right=True)

        ax = plt.gca()
        ax.spines["bottom"].set_linewidth(2)
        ax.spines["left"].set_linewidth(2)

        # Save plot
        plot_path = f"./plots/deltaCT/{gene}_deltaCT_expression.png"
        plt.savefig(plot_path, dpi=300, bbox_inches="tight")
        st.pyplot(plt)

        with open(plot_path, "rb") as file:
            st.download_button(
                label=f"📥 Download {gene} -ΔCt Plot",
                data=file,
                file_name=f"{gene}_deltaCT_expression.png",
                mime="image/png"
            )
