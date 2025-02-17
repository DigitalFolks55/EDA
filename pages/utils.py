import pandas as pd
import streamlit as st


def dfprofiler(df):
    with st.expander("DataFrame Description"):
        st.write(df.describe())