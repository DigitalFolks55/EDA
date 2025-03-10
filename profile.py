import pandas as pd
import streamlit as st

# Description of app.
st.title("Profile Data")

with st.expander("Concepts"):
    st.text(
        """
        The main purpose of data profiling is that to understand what your dataset looks like.
        This tool helps you to understand the basics of your dataset.
            - Data types (numbers and text) and key statistics (averages, count, max and min etc).
        It highlights potential problems, such as missing values or duplicate entries, which could cause issues in further data analysis.
        The tool even shows you exactly where these problems are in your data.
        This can help you to fix the issues quickly.

        Data profiling on this tool.
        1) Dataset samples
            - You can check what kind of columns/data are in your dataset
        2) Datatype and Statistical values of the data
        3) Missing values
        4) Duplicated values
        """
    )

if "df" in st.session_state:
    df = st.session_state.df
    st.subheader("Dataset samples")
    st.write(df.head())

    st.subheader("Datatype")
    data_types_df = df.dtypes.to_frame().reset_index()
    data_types_df.columns = ["Column", "Data Type"]
    data_types_df["New Data Type"] = data_types_df["Data Type"].apply(lambda x: str(x))
    data_types_df = st.data_editor(
        data_types_df,
        column_config={
            "New Data Type": st.column_config.SelectboxColumn(
                help="Choose data type which you want to conver",
                options=[
                    "int64",
                    "float64",
                    "object",
                    "category",
                    "bool",
                    "string",
                    "datetime",
                    "date",
                ],
                required=True,
            )
        },
        disabled=["Column", "Data Type"],
        hide_index=True,
    )

    for i, row in data_types_df.iterrows():
        if row["Data Type"] != row["New Data Type"]:
            if row["New Data Type"] == "datetime":
                df[row["Column"]] = pd.to_datetime(df[row["Column"]], errors="coerce")
            elif row["New Data Type"] == "date":
                df[row["Column"]] = pd.to_datetime(
                    df[row["Column"]], errors="coerce"
                ).dt.date
            else:
                df[row["Column"]] = df[row["Column"]].astype(row["New Data Type"])
    st.text("After changing data type")
    st.write(df.head())

    st.subheader("Statistical values of the data")
    st.text("Numerical data")
    profiled_df_num = df.describe(include="number").loc[
        ["count", "mean", "std", "min", "max"]
    ]
    profiled_df_num.loc["null (%)"] = df.isnull().sum() / len(df) * 100
    profiled_df_num.loc["Datatype"] = df.dtypes
    st.write(profiled_df_num)
    st.text("Categorical data")
    profiled_df_cat = df.describe(include=["object", "category"]).loc[
        ["count", "unique", "top", "freq"]
    ]
    profiled_df_cat.loc["null (%)"] = df.isnull().sum() / len(df) * 100
    profiled_df_cat.loc["Datatype"] = df.dtypes
    st.write(profiled_df_cat)
    with st.expander("Intention & How to fix"):
        st.text(
            """
            1) Intention
             - Understand datatype of the data
             - Check statistical values of the data in line with your expectation
             - Know how many missing values are in the data
            2) How to fix
             - Data cleaning: Correct or Remove values which are not in your expectation
             - Data cleaning: Remove missing or duplicated lines.
             - Data imputation: Fill missing values with mean, median or mode
            """
        )

    st.subheader("Missing values")
    st.write(df[df.isnull().any(axis=1)])
    with st.expander("Intention & How to fix"):
        st.text(
            """
            1) Intention
             - Check lines which have missing values
            2) How to fix
             - Data cleaning: Remove missing or duplicated lines.
             - Data imputation: Fill missing values with mean, median or mode
            """
        )

    st.subheader("Duplicated values")
    st.write(df[df.duplicated(keep=False)])
    with st.expander("Intention & How to fix"):
        st.text(
            """
            1) Intention
             - Check duplicated lines
            2) How to fix
             - Data cleaning: Remove duplicated lines or aggregate lines.
            """
        )

else:
    st.error("Upload a file on the side bar")
