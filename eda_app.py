import pandas as pd
import streamlit as st

navigation_pages = [
    st.Page("toppage.py", title="Home"),
    st.Page("profile.py", title="Profile Data"),
    st.Page("explore_data.py", title="Explore Data"),
    st.Page("outliers.py", title="Explore Outliers"),
    st.Page("hypothesis.py", title="Test Hypothesis"),
]


def run():
    global navigation_pages

    st.set_page_config(layout="wide")
    st.logo(
        "images/logo banner.002.png",
        icon_image="images/logo banner.002.png",
        size="large",
    )

    # Sidebar of app.
    pages = st.navigation(navigation_pages)
    pages.run()
    uploaded_file = st.sidebar.file_uploader("Upload file", accept_multiple_files=False)
    st.sidebar.text("Warning! Don't upload any confidential data on this app.")

    if uploaded_file is not None and "df" not in st.session_state:
        df = pd.read_csv(uploaded_file)
        st.session_state.df_name = uploaded_file.name
        st.session_state.df = df
        st.rerun()


if __name__ == "__main__":
    run()
