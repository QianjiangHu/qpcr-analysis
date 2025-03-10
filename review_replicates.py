import streamlit as st
import pandas as pd

def app():
    """Review and Filter Technical Replicates"""
    st.title("🔍 Review Technical Replicates")

    # Ensure merged data exists
    if "merged_data" not in st.session_state or st.session_state["merged_data"] is None:
        st.error("❌ Merged qPCR data not found. Please upload and merge data first.")
        st.stop()

    # Initialize session state if not present
    if "filtered_merged_data" not in st.session_state:
        st.session_state["filtered_merged_data"] = st.session_state["merged_data"].copy()

    if "user_decisions" not in st.session_state:
        st.session_state["user_decisions"] = {}

    filtered_merged_df = st.session_state["filtered_merged_data"]
    user_decisions = st.session_state["user_decisions"]

    # **Step 1: Define Cq Difference Threshold**
    st.subheader("⚖ Define Cq Variation Threshold")
    threshold = st.number_input(
        "Enter the Cq value difference threshold:",
        min_value=0.1, max_value=5.0, value=1.5, step=0.1,
        key="cq_threshold"
    )

    # **Step 2: Identify High-Variation Technical Replicates**
    replicate_variation = (
        filtered_merged_df.groupby(["Sample", "Gene"])
        .agg(min_Cq=("Cq", "min"), max_Cq=("Cq", "max"))
        .reset_index()
    )
    replicate_variation["Cq_diff"] = replicate_variation["max_Cq"] - replicate_variation["min_Cq"]
    high_variation_replicates = replicate_variation[replicate_variation["Cq_diff"] > threshold]

    # Remove already reviewed pairs
    high_variation_replicates = high_variation_replicates[
        ~high_variation_replicates.apply(lambda row: f"{row['Sample']}__{row['Gene']}" in user_decisions, axis=1)
    ]

    st.write(f"📌 Found **{len(high_variation_replicates)}** high-variation replicates for review.")
    st.dataframe(high_variation_replicates)

    # **Step 3: Review & Select Replicates for Removal**
    st.subheader("📌 Review & Remove Technical Replicates")

    for index, row in high_variation_replicates.iterrows():
        sample, gene = row["Sample"], row["Gene"]
        key_id = f"{sample}__{gene}"

        replicates = filtered_merged_df[
            (filtered_merged_df["Sample"] == sample) & (filtered_merged_df["Gene"] == gene)
        ]

        if replicates.empty:
            continue

        st.write(f"### Reviewing Sample: `{sample}`, Gene: `{gene}`")
        st.dataframe(replicates)

        default_action = user_decisions.get(key_id, {}).get("action", "Keep All")

        action = st.radio(
            f"Action for `{sample} - {gene}`:",
            options=["Keep All", "Remove Specific", "Remove All"],
            index=["Keep All", "Remove Specific", "Remove All"].index(default_action),
            key=f"action_{key_id}"
        )

        remove_well = None
        if action == "Remove Specific":
            remove_well = st.selectbox(
                "Select Well ID to Remove:",
                replicates["Well"].unique(),
                key=f"well_{key_id}"
            )

        if st.button(f"Save Decision for `{sample} - {gene}`", key=f"save_{key_id}"):
            user_decisions[key_id] = {"action": action, "well": remove_well}
            st.session_state["user_decisions"] = user_decisions
            st.success(f"✅ Decision saved for `{sample} - {gene}`!")

        if key_id in user_decisions and st.button(f"Undo Decision for `{sample} - {gene}`", key=f"undo_{key_id}"):
            del user_decisions[key_id]
            st.session_state["user_decisions"] = user_decisions
            st.warning(f"⚠️ Decision undone for `{sample} - {gene}`!")

    # **Step 4: Apply All Changes at Once**
    if st.button("🚀 Apply All Selected Removals"):
        updated_filtered_df = st.session_state["filtered_merged_data"].copy()

        for key, decision in user_decisions.items():
            try:
                sample, gene = key.split("__")
            except ValueError:
                st.error(f"⚠️ Error parsing key: `{key}`")
                continue

            action = decision["action"]
            well_to_remove = decision.get("well", None)

            if action == "Remove Specific" and well_to_remove:
                updated_filtered_df = updated_filtered_df[
                    ~((updated_filtered_df["Sample"] == sample) & 
                      (updated_filtered_df["Gene"] == gene) & 
                      (updated_filtered_df["Well"] == well_to_remove))
                ]
            elif action == "Remove All":
                updated_filtered_df = updated_filtered_df[
                    ~((updated_filtered_df["Sample"] == sample) & (updated_filtered_df["Gene"] == gene))
                ]

        st.session_state["filtered_merged_data"] = updated_filtered_df

        reviewed_keys = [f"{row['Sample']}__{row['Gene']}" for index, row in high_variation_replicates.iterrows()]
        st.session_state["user_decisions"] = {key: val for key, val in user_decisions.items() if key not in reviewed_keys}

        st.success("🎯 All selected replicates have been removed!")

    # **Step 5: Display Decision Log**
    st.subheader("📝 Decision Log")

    if user_decisions:
        decision_log_df = pd.DataFrame(
            [{"Sample": key.split("__")[0], "Gene": key.split("__")[1], "Action": value["action"], "Removed Well": value.get("well")} 
             for key, value in user_decisions.items()]
        )
        st.dataframe(decision_log_df)
    else:
        st.write("No decisions have been made yet.")

    # **Step 6: Download Cleaned Data**
    if st.button("📥 Get Cleaned Data"):
        final_filtered_df = st.session_state["filtered_merged_data"]
        st.download_button(
            label="📥 Download Cleaned Data",
            data=final_filtered_df.to_csv(index=False),
            file_name="Filtered_qPCR_Data.csv",
            mime="text/csv"
        )
