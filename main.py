import streamlit as st

# Load credentials securely from Streamlit secrets
USERS = st.secrets["users"]

# Sidebar login form
st.sidebar.title("🔑 User Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Check credentials
if username in USERS and USERS[username] == password:
    st.sidebar.success(f"✅ Welcome, {username}!")
else:
    st.sidebar.error("❌ Invalid credentials")
    st.stop()  # Stop execution if login fails

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", 
    ["Main", "Upload Data", "Review Replicates", "Mean Cq Computation", "Delta Cq Normalization", 
     "Fold Change Analysis", "ΔCt Visualization", "Fold Change Visualization"]
)

# Load different pages
if page == "Main":
    st.title("Welcome to MK Lab qPCR Analysis App")
    st.write("Use the sidebar to navigate through different steps of the qPCR analysis.")
    st.write("Please have your Cq file, gene map file, sample map, and group information files in **CSV format**.")
    
    # 📥 **Download Template Files**
    st.subheader("📂 Download Example Template Files")
    st.markdown("To ensure correct data formatting, please use the following template files:")

    template_files = {
        "Cq_template.csv": "templates/Cq_template.csv",
        "genes_template.csv": "templates/genes_template.csv",
        "samples_template.csv": "templates/samples_template.csv",
        "groups_template.csv": "templates/groups_template.csv"
    }

    for file_name, file_path in template_files.items():
        try:
            with open(file_path, "rb") as file:
                st.download_button(
                    label=f"📥 Download {file_name}",
                    data=file,
                    file_name=file_name,
                    mime="text/csv"
                )
        except FileNotFoundError:
            st.warning(f"⚠️ {file_name} is missing. Please upload it to the `templates/` folder.")

    st.write("-----------------------------")
    st.write("For any questions, please contact: **huqj@pitt.edu**")

elif page == "Upload Data":
    import upload_data
    upload_data.app()
elif page == "Review Replicates":
    import review_replicates
    review_replicates.app()
elif page == "Mean Cq Computation":
    import mean_cq_computation
    mean_cq_computation.app()
elif page == "Delta Cq Normalization":
    import deltact_normalization
    deltact_normalization.app()
elif page == "Fold Change Analysis":
    import fold_change_analysis
    fold_change_analysis.app()
elif page == "ΔCt Visualization":
    import visualization_delta_ct
    visualization_delta_ct.app()
elif page == "Fold Change Visualization":
    import visualization_fold_change
    visualization_fold_change.app()
import streamlit as st

# Load credentials securely from Streamlit secrets
USERS = st.secrets["users"]

# Sidebar login form
st.sidebar.title("🔑 User Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Check credentials
if username in USERS and USERS[username] == password:
    st.sidebar.success(f"✅ Welcome, {username}!")
else:
    st.sidebar.error("❌ Invalid credentials")
    st.stop()  # Stop execution if login fails

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", 
    ["Main", "Upload Data", "Review Replicates", "Mean Cq Computation", "Delta Cq Normalization", 
     "Fold Change Analysis", "ΔCt Visualization", "Fold Change Visualization"]
)

# Load different pages
if page == "Main":
    st.title("Welcome to MK Lab qPCR Analysis App")
    st.write("Use the sidebar to navigate through different steps of the qPCR analysis.")
    st.write("Please have your Cq file, gene map file, sample map, and group information files in **CSV format**.")
    
    # 📥 **Download Template Files**
    st.subheader("📂 Download Example Template Files")
    st.markdown("To ensure correct data formatting, please use the following template files:")

    template_files = {
        "Cq_template.csv": "templates/Cq_template.csv",
        "genes_template.csv": "templates/genes_template.csv",
        "samples_template.csv": "templates/samples_template.csv",
        "groups_template.csv": "templates/groups_template.csv"
    }

    for file_name, file_path in template_files.items():
        try:
            with open(file_path, "rb") as file:
                st.download_button(
                    label=f"📥 Download {file_name}",
                    data=file,
                    file_name=file_name,
                    mime="text/csv"
                )
        except FileNotFoundError:
            st.warning(f"⚠️ {file_name} is missing. Please upload it to the `templates/` folder.")

    st.write("-----------------------------")
    st.write("For any questions, please contact: **huqj@pitt.edu**")

elif page == "Upload Data":
    import upload_data
    upload_data.app()
elif page == "Review Replicates":
    import review_replicates
    review_replicates.app()
elif page == "Mean Cq Computation":
    import mean_cq_computation
    mean_cq_computation.app()
elif page == "Delta Cq Normalization":
    import deltact_normalization
    deltact_normalization.app()
elif page == "Fold Change Analysis":
    import fold_change_analysis
    fold_change_analysis.app()
elif page == "ΔCt Visualization":
    import visualization_delta_ct
    visualization_delta_ct.app()
elif page == "Fold Change Visualization":
    import visualization_fold_change
    visualization_fold_change.app()
