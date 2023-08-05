import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, chi2_contingency
import streamlit as st

st.set_page_config(page_title="Streamlit Project", page_icon=":chart_with_upwards_trend:", layout="wide")
st.markdown("""
<style>
body {
    color: #444;
    background-color: #000;
}
h1, h2, h3 {
    color: #444;
}
</style>
""", unsafe_allow_html=True)

file = st.file_uploader("Загрузите датасет (CSV)", type="csv")
if file is not None:
    df = pd.read_csv(file)

    columns = df.columns.tolist()
    first = st.selectbox("Выберите первую колонку", columns)
    second = st.selectbox("Выберите вторую колонку", columns)

    mean = df[first].mean()
    df[first] = df[first].fillna(mean)
    mean = df[second].mean()
    df[second] = df[second].fillna(mean)

    fig, axs = plt.subplots(1, 2)
    axs[0].hist(df[first])
    axs[0].set_title(first)
    axs[1].hist(df[second])
    axs[1].set_title(second)
    st.pyplot(fig)

    tests = ["Т-критерий Стьюдента", "Критерий Хи-квадрат"]
    test = st.selectbox("Выберите алгоритм теста гипотезы", tests)

    if test == "Т-критерий Стьюдента":
        _, pvalue = ttest_ind(df[first], df[second])
        st.write(f"Результат Т-теста: {pvalue:.3f}")
    elif test == "Критерий Хи-квадрат":
        contingency_table = pd.crosstab(df[first], df[second])
        _, pvalue, _, _ = chi2_contingency(contingency_table)
        st.write(f"Результат Хи-квадрат теста: {pvalue:.3f}")
else:
    st.write("Загрузите датасет (CSV)")