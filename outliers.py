import streamlit as st

from modules.utils import (dfprofiler, outlier_hampel, outlier_iqr,
                           outlier_zscore)

methods = ["Z score", "Interquartile range (IQR)", "Hampel filter"]


# Description of app.
st.title("Explore Outliers")

with st.expander("Concepts"):
    st.text(
        """
        The main purpose of exploring outliter of given data.
        Outliers negatively impact the statistical analysis and machine learning algorithms.
        Several mothologies are available to detect outliers as below.

        Outlier detection on this tool.
        * Statitical mothods
        1) Z-score
        2) Interquartile range (IQR)
        3) Hampel filter (MAD)

        * To be updated:
        Other mothods, such as Clustering and ML techniques
        """
    )

if "df" in st.session_state:
    df = st.session_state.df
    cols = list(df.columns)
    cols.insert(0, None)

    method = st.selectbox("Select a methonology", methods)
    column = st.selectbox("Select a column", cols)

    if column is None:
        st.text(
            """
            Choose one of columns from dataset.
            """
        )
    elif df[column].dtype in ["object", "category"]:
        st.text(
            "Selected column is a categorical column, please select a numerical column"
        )
    else:
        if method == "Z score":
            threshold = st.slider("Select a threshold", 0.0, 5.0, 3.0, 0.1)
            if column is not None:
                outlier_zscore(df, column, threshold)
            with st.expander("Intention & How to fix"):
                st.text(
                    """
                    1) Intention
                    - Define outliers based on the z-score.
                    2) How to fix
                    - Outliers: Remove or impute outliers (Please review it with experts).
                    """
                )
                st.text("*Reference")
                st.link_button("Z score", "https://en.wikipedia.org/wiki/Standard_score")
        elif method == "Interquartile range (IQR)":
            threshold = st.slider("Select a threshold", 0.0, 5.0, 1.5, 0.1)
            if column is not None:
                outlier_iqr(df, column, threshold)
            with st.expander("Intention & How to fix"):
                st.text(
                    """
                    1) Intention
                    - Define outliers based on the interquartile range.
                    2) How to fix
                    - Outliers: Remove or impute outliers (Please review it with experts).
                    """
                )
                st.text("*Reference")
                st.link_button("Interquartile range", "https://en.wikipedia.org/wiki/Interquartile_range")
        elif method == "Hampel filter":
            threshold = st.slider("Select a threshold", 0.0, 5.0, 3.0, 0.1)
            if column is not None:
                outlier_hampel(df, column, threshold)
            with st.expander("Intention & How to fix"):
                st.text(
                    """
                    1) Intention
                    - Define outliers based on the Hampel filter.
                    2) How to fix
                    - Outliers: Remove or impute outliers (Please review it with experts).
                    """
                )
                st.text("*Reference")
                st.link_button("Hampel filter", "https://real-statistics.com/time-series-analysis/stochastic-processes/hampel-filter-outliers/")
        else:
            st.text("Not implemented yet")

    dfprofiler(df)

else:
    st.text("Upload a file on the side bar")
