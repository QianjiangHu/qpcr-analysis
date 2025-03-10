import streamlit as st
import pandas as pd
import os

# ✅ Ensure required directories exist
os.makedirs("./results", exist_ok=True)

def app():
    """Upload and Merge qPCR Data"""
    st.title("📂 Upload & Merge qPCR Data")

    # Reset downstream data when merging new data
    if st.button("🔄 Reset Data"):
        for key in ["merged_data", "summary", "filtered_merged_data", "user_decisions", 
                    "mean_cq_df", "normalized_qPCR_df", "fold_change_qPCR_df"]:
            st.session_state[key] = None
        st.success("✅ All previous data cleared. You can start fresh.")

    # Step 1: Enter number of plates
    num_plates = st.number_input("🔢 Enter the number of plates:", min_value=1, max_value=20, step=1, value=1)

    # Store uploaded files
    plate_data = {}

    for i in range(1, num_plates + 1):
        st.subheader(f"📂 Upload Files for Plate {i}")

        cq_file = st.file_uploader(f"📥 Plate {i}: Upload Cq.csv", type=["csv"], key=f"cq_{i}")
        genes_file = st.file_uploader(f"📥 Plate {i}: Upload Genes.csv", type=["csv"], key=f"genes_{i}")
        samples_file = st.file_uploader(f"📥 Plate {i}: Upload Samples.csv", type=["csv"], key=f"samples_{i}")

        if cq_file and genes_file and samples_file:
            plate_name = f"plate{i}"
            plate_data[plate_name] = {
                "Cq": pd.read_csv(cq_file),
                "genes": pd.read_csv(genes_file, index_col=0),
                "samples": pd.read_csv(samples_file, index_col=0)
            }
            st.success(f"✅ All files for Plate {i} uploaded successfully!")

    # Step 2: Upload the `groups.csv` file
    st.subheader("📂 Upload the **Groups File (`groups.csv`)**")
    groups_file = st.file_uploader("📥 Upload groups.csv", type=["csv"], key="groups")

    # 🔘 "Merge Data" Button
    if st.button("🚀 Merge Data"):
        if plate_data and groups_file:
            groups_df = pd.read_csv(groups_file)
            st.success("✅ Groups file uploaded successfully!")

            all_data = []
            plate_summaries = {}

            for plate, files in plate_data.items():
                cq_df = files["Cq"]
                genes_df = files["genes"]
                samples_df = files["samples"]

                # ✅ Standardize Well ID format (A01 → A1)
                cq_df["Row"] = cq_df["Well"].str.extract(r"([A-P])")  
                cq_df["Column"] = cq_df["Well"].str.extract(r"(\d{2})").astype(int)  
                cq_df["Well"] = cq_df["Row"] + cq_df["Column"].astype(str)  

                # ✅ Reshape genes and samples into long format
                genes_melted = genes_df.melt(ignore_index=False).reset_index()
                genes_melted.columns = ["Row", "Column", "Gene"]
                genes_melted["Well"] = genes_melted["Row"] + genes_melted["Column"].astype(str)

                samples_melted = samples_df.melt(ignore_index=False).reset_index()
                samples_melted.columns = ["Row", "Column", "Sample"]
                samples_melted["Well"] = samples_melted["Row"] + samples_melted["Column"].astype(str)

                # ✅ Merge gene and sample information
                merged_df = genes_melted.merge(samples_melted, on="Well", how="left")
                merged_df = merged_df.merge(cq_df[["Well", "Cq"]], on="Well", how="left")

                # ✅ Merge with **group information**
                merged_df = merged_df.merge(groups_df, on="Sample", how="left")

                # ✅ Add plate identifier
                merged_df["Plate"] = plate

                # ✅ Remove empty wells
                empty_wells = merged_df["Sample"].isna().sum() + merged_df["Gene"].isna().sum()
                filtered_df = merged_df.dropna(subset=["Sample", "Gene"]).reset_index(drop=True)

                # ✅ Save per-plate summary
                plate_summaries[plate] = {
                    "Total Wells": len(merged_df),
                    "Empty Wells": empty_wells,
                    "Unique Samples": filtered_df["Sample"].nunique(),
                    "Unique Genes": filtered_df["Gene"].nunique()
                }

                # ✅ Append to all_data list
                all_data.append(filtered_df)

            # ✅ Combine all plates into a single DataFrame
            final_data = pd.concat(all_data, ignore_index=True)

            # ✅ Save merged data & store in session state
            final_data.to_csv("./results/Merged_qPCR_Data.csv", index=False)
            st.session_state["merged_data"] = final_data
            st.session_state["summary"] = plate_summaries

            st.success("✅ All plates successfully merged and saved with group information!")
            st.write("📋 **Preview of Merged Data (First 5 Rows):**")
            st.dataframe(final_data.head())

    # ✅ If data exists in session state, display search & download options
    if st.session_state["merged_data"] is not None:
        final_data = st.session_state["merged_data"]
        plate_summaries = st.session_state["summary"]

        # 📊 **Display Summary**
        st.subheader("📊 Summary of Merged Data")
        total_wells = sum([p["Total Wells"] for p in plate_summaries.values()])
        total_empty_wells = sum([p["Empty Wells"] for p in plate_summaries.values()])
        total_samples = final_data["Sample"].nunique()
        total_genes = final_data["Gene"].nunique()

        st.write(f"📌 **Total Plates:** {len(plate_summaries)}")
        st.write(f"📌 **Total Wells:** {total_wells}")
        st.write(f"📌 **Empty Wells:** {total_empty_wells}")
        st.write(f"📌 **Total Unique Samples:** {total_samples}")
        st.write(f"📌 **Total Unique Genes:** {total_genes}")

        # 📌 Per-Plate Summary
        st.subheader("📋 Per-Plate Breakdown")
        summary_df = pd.DataFrame.from_dict(plate_summaries, orient="index")
        st.dataframe(summary_df)

        # 🔍 **Enable Full Data Search**
        st.subheader("🔎 Search Data (Full Dataset)")
        search_term = st.text_input("Type to search:")
        filtered_data = final_data if not search_term else final_data[
            final_data.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        ]
        st.dataframe(filtered_data)

        # 📥 **Download Full Dataset**
        st.subheader("📥 Download Full Data")
        st.download_button(
            label="Download Full Merged Data as CSV",
            data=final_data.to_csv(index=False),
            file_name="Merged_qPCR_Data.csv",
            mime="text/csv"
        )
