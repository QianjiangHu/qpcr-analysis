import streamlit as st

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
    st.title("Welcome to MK lab qPCR Analysis App")
    st.write("Use the sidebar to navigate through different steps of the qPCR analysis.")
    st.write("Please have your Cq file, gene map file, sample map and group information files as .csv format")
    st.write("-----------------------------")
    st.write("for any questions, please contact: huqj@pitt.edu")
    
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
