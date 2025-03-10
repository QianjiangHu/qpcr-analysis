import streamlit as st
import pandas as pd

def app():
    """Compute Mean Cq for Each Sample-Gene Pair"""
    st.title("📊 Compute Mean Cq Values")

    # Ensure cleaned data exists
    if "filtered_merged_data" not in st.session_state:
        st.error("❌ No cleaned data available. Please review & clean technical replicates first.")
        st.stop()

    filtered_merged_df = st.session_state["filtered_merged_data"]

    if st.button("🔄 Compute Mean Cq Values"):
        # ✅ Compute Mean Cq per Sample-Gene pair (ignoring Plate)
        mean_cq_df = (
            filtered_merged_df.groupby(["Sample", "Gene"], as_index=False)
            .agg(Mean_Cq=("Cq", "mean"))  # Calculate mean Cq for each Sample-Gene pair
        )

        # ✅ Merge with Group metadata
        mean_cq_df = mean_cq_df.merge(
            filtered_merged_df[["Sample", "Gene", "Group"]].drop_duplicates(),
            on=["Sample", "Gene"],
            how="left"
        )

        # ✅ Store in session state persistently
        st.session_state["mean_cq_df"] = mean_cq_df

    # ✅ Check if mean Cq data exists and display
    if "mean_cq_df" in st.session_state:
        st.write(f"📌 Computed Mean Cq for **{st.session_state['mean_cq_df'].shape[0]}** Sample-Gene pairs.")
        st.dataframe(st.session_state["mean_cq_df"].head(10))  # Show preview

        # ✅ Provide a download button for Mean Cq Data
        st.download_button(
            label="📥 Download Mean Cq Data",
            data=st.session_state["mean_cq_df"].to_csv(index=False),
            file_name="Mean_Cq_Data.csv",
            mime="text/csv"
        )
