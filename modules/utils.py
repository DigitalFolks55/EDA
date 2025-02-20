import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st


def dfprofiler(df) -> None:
    with st.expander("DataFrame Description"):
        profiled_df = df.describe(include="all").loc[["count", "unique", "top", "freq", "mean", "std", "min", "max"]]
        profiled_df.loc["null (%)"] = df.isnull().sum()/len(df)*100
        profiled_df.loc["Datatype"] = df.dtypes  
        st.write(profiled_df)


def dist_plot(df, column) -> None:
    if column == "All":
        for col in [x for x in df.select_dtypes(include="number").columns]:
            f, ax = plt.subplots(1,3,figsize=(12,4))
            sns.histplot(df, x=col, ax=ax[0], kde=True, bins=20, stat="percent")
            sns.boxplot(df, x=col, ax=ax[1])
            sns.violinplot(df, x=col, ax=ax[2], alpha=0.3, label=col)
            plt.legend()
            plt.tight_layout()
            st.pyplot(f)
    elif df[column].dtype in ["object", "category"]:
        st.text("Selected column is a categorical column, please select a numerical column")
    else:
        f, ax = plt.subplots(1,3,figsize=(12,4))
        sns.histplot(df, x=column, ax=ax[0], kde=True, bins=20, stat="percent")
        sns.boxplot(df, x=column, ax=ax[1])
        sns.violinplot(df, x=column, ax=ax[2], alpha=0.3)
        plt.tight_layout()
        st.pyplot(f)


def count_plot(df, column, hue) -> None:
    if column == "All":
        for col in [x for x in df.select_dtypes(include=["object", "category"]).columns]:
            f, ax = plt.subplots(1,2,figsize=(12,4))
            sns.countplot(data=df, x=col, ax=ax[0], hue=hue)
            x_labels_1 = [label.get_text() for label in ax[0].get_xticklabels()]
            ax[0].set_xticklabels(x_labels_1, rotation=90)
            tgt_counts = df[col].value_counts()
            ax[1].pie(tgt_counts, labels=tgt_counts.index, autopct='%1.1f%%', colors=sns.color_palette('Set2'))
            plt.tight_layout()
            st.pyplot(f)
    else:
        if df[column].dtype not in ["object", "category"]:
            st.text("Selected column is a numerical column. Chart would be messy in case")
        f, ax = plt.subplots(1,2,figsize=(12,4))
        sns.countplot(data=df, x=column, ax=ax[0], hue=hue)
        x_labels_1 = [label.get_text() for label in ax[0].get_xticklabels()]
        ax[0].set_xticklabels(x_labels_1, rotation=90)
        tgt_counts = df[column].value_counts()
        ax[1].pie(tgt_counts, labels=tgt_counts.index, autopct='%1.1f%%', colors=sns.color_palette('Set2'))
        plt.tight_layout()
        st.pyplot(f)


def scatter_plot(df, x, y, hue) -> None:
    """Scatter plot"""
    col1, col2 = st.columns([1,1], vertical_alignment="center")
    if x == "All" or y == "All":
        st.text("All is not accepted for x and y")
    with col1:
        f1 = sns.lmplot(data=df, x=x, y=y, hue=hue, fit_reg=True)
        plt.tight_layout()
        st.pyplot(f1)
    with col2:
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
    mask = np.tril(np.ones(df_corr.shape),k = -1).astype(bool)
    df_corr_fil = df_corr.where(mask)

    f, ax = plt.subplots(1,2,figsize=(12,6))
    sns.heatmap(df_corr_fil, annot=True, cmap="crest", fmt=".2f", linewidths=0.01, ax=ax[0])
    mask = df_corr_fil.where(abs(df_corr_fil) > threshold).isna()
    sns.heatmap(df_corr_fil, annot=True, cmap="crest", fmt=".2f", linewidths=0.01, mask=mask, ax=ax[1])
    plt.tight_layout()
    st.pyplot(f)
    