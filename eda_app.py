import numpy as np
import pandas as pd
import streamlit as st


navigation_pages = [
    st.Page("pages/toppage.py", title="Home"),
    st.Page("pages/profile.py", title="Profile Data"),
    # st.Page("pages/distribution.py", title="Check Distribution")
]

def run():
    global navigation_pages

    st.set_page_config(layout="wide")
    st.logo("images/logo banner.002.png", icon_image="images/logo banner.002.png", size="large")

    # Sidebar of app.
    pages = st.navigation(navigation_pages)
    pages.run()
    uploaded_file = st.sidebar.file_uploader("Upload file", accept_multiple_files=False)

    if uploaded_file is not None and "df" not in st.session_state:
        df = pd.read_csv(uploaded_file)
        st.session_state.df_name = uploaded_file.name
        st.session_state.df = df

if __name__ == "__main__":
    run()