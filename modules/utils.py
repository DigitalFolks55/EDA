import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib.ticker import MaxNLocator
from scipy.stats import iqr, median_abs_deviation, ttest_ind, zscore
from statsmodels.stats.weightstats import ztest


def dfprofiler(df) -> None:
    with st.expander("DataFrame Description"):
        profiled_df = df.describe(include="all").loc[
            ["count", "unique", "top", "freq", "mean", "std", "min", "max"]
        ]
        profiled_df.loc["null (%)"] = df.isnull().sum() / len(df) * 100
        profiled_df.loc["Datatype"] = df.dtypes
        st.write(profiled_df)


def dist_plot(df, column) -> None:
    if column == "All":
        for col in [x for x in df.select_dtypes(include="number").columns]:
            f, ax = plt.subplots(1, 3, figsize=(12, 4))
            sns.histplot(df, x=col, ax=ax[0], kde=True, bins=20, stat="percent")
            sns.boxplot(df, x=col, ax=ax[1])
            sns.violinplot(df, x=col, ax=ax[2], alpha=0.3, label=col)
            plt.legend()
            plt.tight_layout()
            st.pyplot(f)
    elif df[column].dtype in ["object", "category"]:
        st.error(
            "Selected column is a categorical column, please select a numerical column"
        )
    else:
        f, ax = plt.subplots(1, 3, figsize=(12, 4))
        sns.histplot(df, x=column, ax=ax[0], kde=True, bins=20, stat="percent")
        sns.boxplot(df, x=column, ax=ax[1])
        sns.violinplot(df, x=column, ax=ax[2], alpha=0.3)
        plt.tight_layout()
        st.pyplot(f)


def count_plot(df, column, hue) -> None:
    if column == "All":
        for col in [
            x for x in df.select_dtypes(include=["object", "category"]).columns
        ]:
            f, ax = plt.subplots(1, 2, figsize=(12, 4))
            sns.countplot(data=df, x=col, ax=ax[0], hue=hue)
            x_labels_1 = [label.get_text() for label in ax[0].get_xticklabels()]
            ax[0].set_xticklabels(x_labels_1, rotation=90)
            tgt_counts = df[col].value_counts()
            ax[1].pie(
                tgt_counts,
                labels=tgt_counts.index,
                autopct="%1.1f%%",
                colors=sns.color_palette("Set2"),
            )
            plt.tight_layout()
            st.pyplot(f)
    else:
        if df[column].dtype not in ["object", "category"]:
            st.error(
                "Selected column is a numerical column. Chart would be messy in case"
            )
        f, ax = plt.subplots(1, 2, figsize=(12, 4))
        sns.countplot(data=df, x=column, ax=ax[0], hue=hue)
        x_labels_1 = [label.get_text() for label in ax[0].get_xticklabels()]
        ax[0].set_xticklabels(x_labels_1, rotation=90)
        tgt_counts = df[column].value_counts()
        ax[1].pie(
            tgt_counts,
            labels=tgt_counts.index,
            autopct="%1.1f%%",
            colors=sns.color_palette("Set2"),
        )
        plt.tight_layout()
        st.pyplot(f)


def scatter_plot(df, x, y, hue) -> None:
    """Scatter plot"""
    if (
        df[x].dtype in ["datetime64[ns]"]
        or isinstance(df[x].dtype, datetime.date)
        or df[y].dtype in ["datetime64[ns]"]
        or isinstance(df[y].dtype, datetime.date)
    ):
        st.error("Chosen datetime or date column. Please select other columns.")
    else:
        col1, col2 = st.columns([1, 1], vertical_alignment="center")
        with col1:
            f1 = plt.figure()
            f1 = sns.lmplot(data=df, x=x, y=y, hue=hue, fit_reg=True)
            plt.tight_layout()
            st.pyplot(f1)
        with col2:
            f2 = plt.figure()
            f2 = sns.jointplot(data=df, x=x, y=y, hue=hue)
            plt.tight_layout()
            st.pyplot(f2)


def pair_plot(df, hue) -> None:
    """Pair plot"""
    f = sns.pairplot(df, hue=hue)
    plt.tight_layout()
    st.pyplot(f)


def corr_plot(df, threshold) -> None:
    """Calculate Pearson correlation among numerical columns and plot it."""
    df_corr = df.corr(numeric_only=True)
    mask = np.tril(np.ones(df_corr.shape), k=-1).astype(bool)
    df_corr_fil = df_corr.where(mask)

    f, ax = plt.subplots(1, 2, figsize=(12, 6))
    sns.heatmap(
        df_corr_fil, annot=True, cmap="crest", fmt=".2f", linewidths=0.01, ax=ax[0]
    )
    mask = df_corr_fil.where(abs(df_corr_fil) > threshold).isna()
    sns.heatmap(
        df_corr_fil,
        annot=True,
        cmap="crest",
        fmt=".2f",
        linewidths=0.01,
        mask=mask,
        ax=ax[1],
    )
    plt.tight_layout()
    st.pyplot(f)


def line_plot(df, x, y, hue) -> None:
    """Line plot"""
    x_nunique = df[x].nunique()
    col1, col2 = st.columns([1, 1], vertical_alignment="center")
    with col1:
        f1, ax1 = plt.subplots()
        sns.lineplot(data=df, x=x, y=y, ax=ax1)
        ax1.set_xlim(xmin=df[x].min(), xmax=df[x].max())
        if x_nunique > 100:
            ax1.xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(f1)
    with col2:
        f2, ax2 = plt.subplots()
        sns.lineplot(data=df, x=x, y=y, hue=hue, ax=ax2)
        ax2.set_xlim(xmin=df[x].min(), xmax=df[x].max())
        if x_nunique > 100:
            ax2.xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(f2)


def outlier_zscore(df, column, threshold) -> None:
    """Z score method for outlier detection."""
    input_cols = df.columns
    df["zscore"] = abs(zscore(df[column]))
    df["outlier"] = df["zscore"].apply(
        lambda x: "outlier" if x > threshold else "nonoutlier"
    )

    f, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(data=df, x=column, hue="outlier", ax=ax[0])
    sns.stripplot(data=df, x=column, y="outlier", ax=ax[1])
    plt.tight_layout()
    st.pyplot(f)

    st.text("Outliers")
    st.write(df[df["outlier"] == "outlier"])
    st.session_state.df = df[input_cols]


def outlier_iqr(df, column, threshold) -> None:
    """Interquartile range method for outlier detection."""
    input_cols = df.columns
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr_df = iqr(df[column])
    lower_bound = q1 - (threshold * iqr_df)
    upper_bound = q3 + (threshold * iqr_df)

    df["outlier"] = df[column].apply(
        lambda x: "outlier" if x < lower_bound or x > upper_bound else "nonoutlier"
    )

    f, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(data=df, x=column, hue="outlier", ax=ax[0])
    sns.stripplot(data=df, x=column, y="outlier", ax=ax[1])
    plt.tight_layout()
    st.pyplot(f)

    st.text("Outliers")
    st.write(df[df["outlier"] == "outlier"])
    st.session_state.df = df[input_cols]


def outlier_hampel(df, column, threshold) -> None:
    """Hempler filter method for outlier detection."""
    input_cols = df.columns
    median = df[column].median()
    mad = median_abs_deviation(df[column])
    lower_bound = median - (threshold * mad)
    upper_bound = median + (threshold * mad)

    df["outlier"] = df[column].apply(
        lambda x: "outlier" if x < lower_bound or x > upper_bound else "nonoutlier"
    )

    f, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(data=df, x=column, hue="outlier", ax=ax[0])
    sns.stripplot(data=df, x=column, y="outlier", ax=ax[1])
    plt.tight_layout()
    st.pyplot(f)

    st.text("Outliers")
    st.write(df[df["outlier"] == "outlier"])
    st.session_state.df = df[input_cols]


def data_split(df, col1, col2=None, hue=None) -> pd.DataFrame:
    """Split data by column."""
    if hue is not None:
        return (
            df[df[hue] == df[hue].unique()[0]][col1],
            df[df[hue] == df[hue].unique()[1]][col1],
        )
    elif col2 is not None:
        return df[col1], df[col2]


def hypo_kde_plot(df, col1, col2=None, hue=None) -> None:
    """KDE plot for hypothesis testing."""
    f, ax = plt.subplots(1, 2, figsize=(12, 4))
    if hue is not None:
        sns.kdeplot(
            df[df[hue] == df[hue].unique()[0]], x=col1, hue=hue, fill=True, ax=ax[0]
        )
        sns.kdeplot(
            df[df[hue] == df[hue].unique()[1]], x=col1, hue=hue, fill=True, ax=ax[1]
        )
    elif col2 is not None:
        sns.kdeplot(df, x=col1, fill=True, ax=ax[0])
        sns.kdeplot(df, x=col2, fill=True, ax=ax[1])
    plt.tight_layout()
    st.pyplot(f)


def hypo_ztest(df, col1, col2=None, hue=None, conf=95, tail="one-tailed") -> None:
    """Z test for hypothesis testing."""
    if df[col1].dtype in ["object", "category", "datetime64[ns]"] or isinstance(
        df[col1].dtype, datetime.datetime
    ):
        st.error(f"Please select a numerical column for the 1st column; {col1}.")
    elif col2 is not None and (
        df[col2].dtype in ["object", "category", "datetime64[ns]"]
        or isinstance(df[col2].dtype, datetime.datetime)
    ):
        st.error(f"Please select a numerical column for the 2nd column; {col2}.")
    elif hue is not None and len(df[hue].unique()) > 2:
        st.error(
            "Grouping column has groups more than 2 which we cannot proceed hypothesis test; Please select another column."
        )
    else:
        df1, df2 = data_split(df=df, col1=col1, col2=col2, hue=hue)
        z_stat, p_val = ztest(df1, df2)
        if hue is not None:
            st.text(
                f"Null hypothesis: two groups by {hue} of {col1} have same means (averages)"
            )
        elif col2 is not None:
            st.text(
                f"Null hypothesis: two groups by {col2} of {col1} have same means (averages)"
            )

        st.text(f"Z score: {z_stat}")
        st.text(f"P value: {p_val}")

        threshold = 1 - (conf / 100)
        if tail == "two-tailed":
            threshold = threshold / 2

        if p_val < threshold:
            st.text("Reject null hypothesis")
        else:
            st.text("Accept null hypothesis")

        hypo_kde_plot(df=df, col1=col1, col2=col2, hue=hue)


def hypo_ttest(df, col1, col2=None, hue=None, conf=95, tail="one-tailed") -> None:
    """T test for hypothesis testing."""
    if df[col1].dtype in ["object", "category"]:
        st.error(f"Please select a numerical column for the 1st column; {col1}.")
    elif col2 is not None and df[col2].dtype in ["object", "category"]:
        st.error(f"Please select a numerical column for the 2nd column; {col2}.")
    elif hue is not None and len(df[hue].unique()) > 2:
        st.error(
            "Grouping column has groups more than 2 which we cannot proceed hypothesis test; Please select another column."
        )
    else:
        df1, df2 = data_split(df=df, col1=col1, col2=col2, hue=hue)
        t_stat, p_val = ttest_ind(df1, df2)
        if hue is not None:
            st.text(
                f"Null hypothesis: two groups by {hue} of {col1} have same means (averages)"
            )
        elif col2 is not None:
            st.text(
                f"Null hypothesis: two groups by {col2} of {col1} have same means (averages)"
            )

        st.text(f"T score: {t_stat}")
        st.text(f"P value: {p_val}")

        threshold = 1 - (conf / 100)
        if tail == "two-tailed":
            threshold = threshold / 2

        if p_val < threshold:
            st.text("Reject null hypothesis")
        else:
            st.text("Accept null hypothesis")

        hypo_kde_plot(df=df, col1=col1, col2=col2, hue=hue)
