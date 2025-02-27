import streamlit as st

from modules.utils import dfprofiler, hypo_ttest, hypo_ztest

tests = ["Z-test", "T-test"]


# Description of app.
st.title("Test Hypothesis")

with st.expander("Concepts"):
    st.text(
        """
        The main purpose is to conduct null hypothesis testing with given dataset.
        Hypothesis testing is a statistical method that is used in making statistical decisions using experimental data.
        Test could be done with 2 data samples.
        Hypothesis testing is important for
        1) Avoid misleading conclusions from misreading data
        2) Make evidence-based decisions led by data

        Null hypothesis testing on this tool.
        1) Z-test
        2) T-test

        * To be updated:
        Chi-Square test, ANOVA, Other tests
        """
    )

# target, cat/num
if "df" in st.session_state:
    df = st.session_state.df
    cols = list(df.columns)
    cols.insert(0, None)

    column1 = st.selectbox("1st column: Select a column1", cols)
    column2 = st.selectbox(
        "2nd column: Select a column if you want to use samples from another column",
        cols,
    )
    hue = st.selectbox(
        f"Grouping column: Select a column if you want to use another column for grouping from samples with {column1}",
        cols,
    )
    tail = st.selectbox("Directional test", ["one-tailed", "two-tailed"])
    conf = st.slider("Confidence interval (%)", 0, 100, 95)

    test = st.selectbox("Select a visulazation", tests)

    if test == "Z-test":
        if column2 is not None and hue is not None:
            st.text("Please either of 2nd column or Grouping column")
        elif column1 is not None and hue is not None:
            hypo_ztest(df, col1=column1, col2=None, hue=hue, conf=conf, tail=tail)
        elif column1 is not None and column2 is not None:
            hypo_ztest(df, col1=column1, col2=column2, hue=None, conf=conf, tail=tail)
        else:
            st.text("Please select columns")

        with st.expander("Reference"):
            st.link_button("Z-test", "https://en.wikipedia.org/wiki/Z-test")
    if test == "T-test":
        if column2 is not None and hue is not None:
            st.text("Please either of 2nd column or Grouping column")
        elif column1 is not None and hue is not None:
            hypo_ttest(df, col1=column1, col2=None, hue=hue, conf=conf, tail=tail)
        elif column1 is not None and column2 is not None:
            hypo_ttest(df, col1=column1, col2=column2, hue=None, conf=conf, tail=tail)
        else:
            st.text("Please select columns")

        with st.expander("Reference"):
            st.link_button("T-test", "https://en.wikipedia.org/wiki/Student%27s_t-test")
    else:
        st.text("Not implemented yet")

    dfprofiler(df)

else:
    st.text("Upload a file on the side bar")
