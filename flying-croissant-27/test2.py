import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

fig, ax = plt.subplots()

iris = sns.load_dataset("iris")
sns.pairplot(iris, hue="species", palette="pastel", ax=ax)

st.pyplot(fig)
