import streamlit as st

from modules.utils import (corr_plot, count_plot, dfprofiler, dist_plot,
                           pair_plot, scatter_plot)

visuals = ["Distribution", "Count", "Scatter", "Pair", "corr_plot"]


# Description of app.
st.title("Explore Data")

with st.expander("Concepts"):
    st.text(
        """
        The main purpose of exploring data is that to understand what your dataset in details.
        This tool helps beginners to efficiently visualize and analyze data, such as:
        1) Identify patterns & trends: i.e. recurring behaviors seasonal spike.
        2) Relationships between variables: i.e. correlation.
        3) Hidden insight: i.e. leading to new opportunities and strategic improvements.
        4) Anomalies & Outlier detection: i.e. incorrect inputs
        5) Visualization

        Data profiling on this tool.
        1) Distribution plot (Categorical, Numerical data)
        2) Pie/Count plot (Categorical data)
        3) Scatter plot (Numerical data)
        4) Pair plot (Numerical data)
        5) Correlation plot (Numerical)

        * To be updated:
        More visularization & Time Series, Geospatial data
        """
    )

if "df" in st.session_state:
    df = st.session_state.df
    cols = list(df.columns)
    cols.insert(0, None)
    cols.append("All")

    visual = st.selectbox("Select a visulazation", visuals)

    if visual == "Distribution":
        column = st.selectbox("Select a column", cols)
        if column is not None:
            dist_plot(df, column)
            with st.expander("Intention & How to fix"):
                st.text(
                    """
                    1) Intention
                    - Understand the distribution of the data whether it is normal or skewed.
                    - Check outliers from the box plot.
                    2) How to fix
                    - Skewed data: Apply log or Box-Cox transformation or nomarilization, such as z_score.
                    - Outliers: Remove or impute outliers (Please review it with experts).
                    """
                )
    elif visual == "Count":
        column = st.selectbox("Select a column", cols)
        hue = st.selectbox("Select a grouping column", cols)
        if column is not None:
            count_plot(df, column, hue)
            with st.expander("Intention & How to fix"):
                st.text(
                    """
                    1) Intention
                    - Check bias of the data.
                    - Check outliers from the labels.
                    2) How to fix
                    - Bias data: Take more data or resampling (over/undersampling).
                    - Outliers: Remove or impute outliers (Please review it with experts).
                    """
                )
    elif visual == "Scatter":
        x_col = st.selectbox("Select a 1st column", cols)
        y_col = st.selectbox("Select a 2nd column", cols)
        hue = st.selectbox("Select grouping column", cols)
        if x_col == "All" or y_col == "All" or hue == "All":
            st.text(
                """
                All is not accepted for any column.
                Choose one of columns from dataset.
                """
            )
        elif x_col is not None and y_col is not None:
            scatter_plot(df, x_col, y_col, hue)
            with st.expander("Intention & How to fix"):
                st.text(
                    """
                    1) Intention
                    - This plot is for more insights on your data.
                    - Review the relationship between 2 columns; quantitative value can be confirmed by correlation heatmap.
                    - Check the relationship by another column.
                    2) How to fix
                    - Outliers: Remove or impute outliers (Please review it with experts).
                    """
                )
        else:
            st.text("We need 2 columns. Please select 1st and 2nd columns")
    elif visual == "Pair":
        hue = st.selectbox("Select a grouping column", cols)
        if hue == "All":
            st.text(
                """
                All is not accepted for a grouping column.
                Choose one of columns from dataset.
                """
            )
        else:
            pair_plot(df, hue)
            with st.expander("Intention & How to fix"):
                st.text(
                    """
                    1) Intention
                    - This plot is for more insights on your data for whole columns.
                    - Review the relationship between 2 columns; quantitative value can be confirmed by correlation heatmap.
                    - Check the relationship by another column.
                    2) How to fix
                    - Outliers: Remove or impute outliers (Please review it with experts).
                    """
                )
    elif visual == "corr_plot":
        threshold = st.slider("Select a threshold", 0.0, 1.0, 0.5, 0.1)
        corr_plot(df, threshold)
        with st.expander("Intention & How to fix"):
            st.text(
                """
                1) Intention
                - This plot is for more insights on your data for whole columns.
                - Review the relationship among columns with quantitative values.
                2) How to fix
                - Correlated columns: Drop one of them as per your needs.
                """
            )
    else:
        st.text("Not implemented yet")

    dfprofiler(df)

else:
    st.text("Upload a file on the side bar")
