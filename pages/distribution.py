import streamlit as st


if "df" in st.session_state:
    st.write(st.session_state.df_name)
    st.write(st.session_state.df)
