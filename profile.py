import streamlit as st
import pandas as pd


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

    st.subheader("Statistical values of the data")
    st.text("Numerical data")
    profiled_df_num = df.describe(include="number").loc[["count", "mean", "std", "min", "max"]]
    profiled_df_num.loc["null (%)"] = df.isnull().sum()/len(df)*100
    profiled_df_num.loc["Datatype"] = df.dtypes
    st.write(profiled_df_num)
    st.text("Categorical data")
    profiled_df_cat = df.describe(include=["object", "category"]).loc[["count", "unique", "top", "freq"]]
    profiled_df_cat.loc["null (%)"] = df.isnull().sum()/len(df)*100
    profiled_df_cat.loc["Datatype"] = df.dtypes
    st.write(profiled_df_cat)
    
    st.subheader("Missing values")
    st.write(df[df.isnull().any(axis=1)])

    st.subheader("Duplicated values")
    st.write(df[df.duplicated(keep=False)])    

else:
    st.text("Upload a file on the side bar")

