import pandas as pd
import streamlit as st

# Description of app.
st.title("Exploratory Data Analysis (EDA)")
st.text(
    """
    This application is designed as an introductory tool to EDA, specifically for beginners.
    It guides users through the general steps of EDA, explaining the core concepts behind each stage.
    The application aims to demystify the EDA process, making it accessible and understandable to those new to data analysis.
    It provides a structured approach to exploring datasets, enabling users to gain initial insights and identify potential patterns, anomalies and relationships within their data before moving on to complex analysis.  # noqa
    If you have any further question/feedback or any bug, please feel free to reach out to the developer, digitalfolk55@gmai.com.
    """
)

# What is EDA
st.subheader("What is EDA?")
st.text(
    """
    EDA is a first step of and an approach for data analysis that includes a varietry of purporses, such as:
    1) Gain insights into the data
    2) Identify patterns, characteristics and relationships
    3) Detect anomalies and outliers
    4) Extract crucial features/variables
    5) Help test hypothesis with statistical methonologies
    6) Determine data manipulation, such as Extract-Tranform-Load (ETL) process, for further data analysis
    """
)

# Why EDA?
st.subheader("Why EDA?")
st.text(
    """
    EDA helps identify potential data quality issues and biases.
    Ultimately, EDA informs and improves the accuracy and effectiveness of subsequent data analysis and modelling.
    Remember, garbage in garbage out.
    """
)

# Why EDA?
st.subheader("General EDA step provided in this app")
st.image("images/EDA_steps.001.png", width=800)

st.subheader("Warning! Don't upload any confidential data on this app.")

# Version logs
st.subheader("Version")
hist = {
    "Date": ["2025-02-16", "2025-02-20"],
    "Description": [
        "Crated an application; Added a page of Profile Data",
        "Added a page of Explore Data",
    ],
}

st.table(pd.DataFrame(hist))
