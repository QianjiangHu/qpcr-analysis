import streamlit as st
import pandas as pd

def app():
    """Normalize ΔCt Values Using Housekeeping Genes"""
    st.title("📊 Normalize ΔCt Using Housekeeping Genes")

    # Ensure Mean Cq data exists
    if "mean_cq_df" not in st.session_state:
        st.error("❌ No Mean Cq data available. Please compute Mean Cq first.")
        st.stop()

    mean_cq_df = st.session_state["mean_cq_df"]  # ✅ Load stored Mean Cq data

    # Step 1: Let the user enter housekeeping genes
    housekeeping_genes_input = st.text_input("Enter housekeeping genes (comma-separated):")

    # ✅ Button to Check Housekeeping Genes
    if st.button("🔍 Check Housekeeping Genes"):
        housekeeping_genes = [gene.strip() for gene in housekeeping_genes_input.split(",")]

        # ✅ Identify missing & found housekeeping genes
        missing_genes = [gene for gene in housekeeping_genes if gene not in mean_cq_df["Gene"].unique()]
        found_genes = list(set(housekeeping_genes) - set(missing_genes))

        # ✅ Store housekeeping genes in session state for later use
        st.session_state["found_genes"] = found_genes

        # ✅ Display housekeeping gene status
        if found_genes:
            st.success(f"✅ Found: {', '.join(found_genes)}")
        else:
            st.error("❌ No valid housekeeping genes found!")

        if missing_genes:
            st.warning(f"⚠️ Missing: {', '.join(missing_genes)}")

    # Step 2: Compute Sample-Specific Housekeeping Mean Cq
    if st.button("🧬 Compute ΔCt"):
        if "found_genes" in st.session_state and st.session_state["found_genes"]:
            found_genes = st.session_state["found_genes"]  # ✅ Retrieve stored housekeeping genes

            # ✅ Calculate the Mean Cq of housekeeping genes per sample
            hk_mean_per_sample = (
                mean_cq_df[mean_cq_df["Gene"].isin(found_genes)]
                .groupby("Sample")["Mean_Cq"]
                .mean()
                .reset_index()
                .rename(columns={"Mean_Cq": "Housekeeping_Mean_Cq"})
            )

            # ✅ Merge housekeeping Mean Cq with main dataset
            normalized_df = mean_cq_df.merge(hk_mean_per_sample, on="Sample", how="left")

            # ✅ Compute Normalized ΔCt values
            normalized_df["Normalized_Cq"] = normalized_df["Mean_Cq"] - normalized_df["Housekeeping_Mean_Cq"]

            # ✅ Store in session state persistently
            st.session_state["normalized_qPCR_df"] = normalized_df

            # ✅ Display Summary
            st.write(f"📌 Normalized ΔCt computed for **{normalized_df.shape[0]}** Sample-Gene pairs.")

    # ✅ **Always Display the Computed Table if Available**
    if "normalized_qPCR_df" in st.session_state:
        normalized_df = st.session_state["normalized_qPCR_df"]

        # ✅ **Preview Table**
        st.data_editor(normalized_df.head(20), height=400, use_container_width=True)

        # ✅ **Download Button**
        st.download_button(
            label="📥 Download Full Normalized qPCR Data",
            data=normalized_df.to_csv(index=False),
            file_name="Normalized_qPCR_Data.csv",
            mime="text/csv"
        )
