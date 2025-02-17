import streamlit as st
import pandas as pd

from pages.utils import dfprofiler


# Description of app.
st.title("Profile Dataset")

if "df" in st.session_state:
    df = st.session_state.df
    st.subheader("Samples of dataset")
    st.dataframe(df.head())

    st.subheader("Stastical values")
    profiled_df = df.describe(include="all").loc[["count", "unique", "top", "freq", "mean", "std", "min", "max"]]
    profiled_df.loc["null (%)"] = df.isnull().sum()/len(df)*100
    st.dataframe(profiled_df)
    
    st.subheader("Missing values (Null or Nan)")
    st.dataframe(df[df.isnull().any(axis=1)])

    st.subheader("Duplicated values")
    st.dataframe(df[df.duplicated()])
    

else:
    st.text("Please upload the file first")

