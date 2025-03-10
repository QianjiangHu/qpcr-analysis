import streamlit as st
import pandas as pd
import numpy as np
import re  # To sanitize filenames

def app():
    """Compute ΔΔCt and Fold Change"""
    st.title("📊 Fold Change Analysis")

    # Ensure Normalized Data Exists
    if "normalized_qPCR_df" not in st.session_state:
        st.error("❌ No normalized qPCR data available. Please compute ΔCt first.")
        st.stop()

    df = st.session_state["normalized_qPCR_df"].copy()

    # ✅ Step 1: User Selects Control Group
    st.subheader("📌 Select Control Group & Groups for Analysis")
    
    # Get available groups
    unique_groups = df["Group"].dropna().unique()

    # Dropdown for control group selection
    control_group = st.selectbox("🔹 Select the control group:", unique_groups)

    # Ensure Control Group is Safe for Filenames
    safe_control_group = re.sub(r"[^\w\-_]", "_", control_group)

    # Multi-select for which groups to analyze
    selected_groups = st.multiselect(
        "🔹 Select groups for analysis (include control group):",
        unique_groups,
        default=[control_group]  # Preselect control group
    )

    # Ensure control group is always included
    if control_group not in selected_groups:
        selected_groups.append(control_group)

    # ✅ Step 2: Compute ΔΔCt and Fold Change
    if st.button("🚀 Compute ΔΔCt & Fold Change"):
        # Filter data to only include selected groups
        df_filtered = df[df["Group"].isin(selected_groups)].copy()

        # ✅ Handle Infinite Values
        df_filtered.replace([np.inf, -np.inf], pd.NA, inplace=True)

        # ✅ Compute Mean ΔCt for the Control Group
        reference_ct = (
            df_filtered[df_filtered["Group"] == control_group]
            .groupby("Gene")["Normalized_Cq"]
            .mean()
            .reset_index()
            .rename(columns={"Normalized_Cq": "Reference_Ct"})
        )

        # ✅ Merge Reference ΔCt Values
        df_filtered = df_filtered.merge(reference_ct, on="Gene", how="left")

        # ✅ Compute ΔΔCt for Each Sample
        df_filtered["Delta_Delta_Ct"] = df_filtered["Normalized_Cq"] - df_filtered["Reference_Ct"]

        # ✅ Compute Fold Change
        df_filtered["Fold_Change"] = 2 ** (-df_filtered["Delta_Delta_Ct"])

        # ✅ Store Data in Session State
        st.session_state["fold_change_qPCR_df"] = df_filtered

        # ✅ Save File Path
        output_file = f"./results/DeltaDeltaCt_qPCR_relative_to_{safe_control_group}.csv"
        st.session_state["fold_change_output_file"] = output_file

        # ✅ Save to CSV
        df_filtered.to_csv(output_file, index=False)

        st.success(f"✅ ΔΔCt and Fold Change calculations completed using '{control_group}' as control!")

    # ✅ Step 3: Ensure Preview Always Stays Visible
    if "fold_change_qPCR_df" in st.session_state:
        df_filtered = st.session_state["fold_change_qPCR_df"]

        st.subheader("📂 Preview of Results:")
        st.dataframe(df_filtered.head(10))  # ✅ This will now persist after clicking "Download CSV"

        st.subheader("📥 Download ΔΔCt & Fold Change Data")
        st.download_button(
            label="📥 Download CSV",
            data=df_filtered.to_csv(index=False),
            file_name=f"DeltaDeltaCt_qPCR_{safe_control_group}.csv",
            mime="text/csv"
        )
