import streamlit as st
import os

# Load credentials securely from Streamlit secrets
USERS = st.secrets["users"]

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None

# Sidebar login form
st.sidebar.title("🔑 User Login")

if not st.session_state["authenticated"]:
    username = st.sidebar.text_input("Username", key="username_input")
    password = st.sidebar.text_input("Password", type="password", key="password_input", type="password")

    if username in USERS and USERS[username] == password:
        st.sidebar.success(f"✅ Welcome, {username}!")
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        st.rerun()  # Refresh the page to update the session state
    else:
        st.sidebar.error("❌ Invalid credentials")
        st.stop()

# Sidebar Navigation
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
    st.write("Please have your Cq file, gene map file, sample map file, and group information files in CSV format.")
    
    st.subheader("📥 Download Template Files")
    st.write("Use these template files to structure your qPCR data correctly:")

    # List of template files
    template_files = {
        "Cq_template.csv": "./templates/Cq_template.csv",
        "Genes_template.csv": "./templates/genes_template.csv",
        "Samples_template.csv": "./templates/samples_template.csv",
        "Groups_template.csv": "./templates/groups_template.csv"
    }

    for filename, filepath in template_files.items():
        if os.path.exists(filepath):
            with open(filepath, "rb") as file:
                st.download_button(label=f"📥 Download {filename}", data=file, file_name=filename, mime="text/csv")
        else:
            st.warning(f"⚠️ {filename} is missing. Please check the templates folder.")

    st.write("-----------------------------")
    st.write("For any questions, please contact: huqj@pitt.edu")

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
