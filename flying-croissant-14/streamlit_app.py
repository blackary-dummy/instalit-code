from pathlib import Path
from platform import python_version

import streamlit as st
from git import Repo
from streamlit_tags import st_tags

from push import add_files

st.title("Deploy your app")

name = st.text_input("App Name", value="flying-croissant-14")

if not name:
    st.stop()

dependencies = st.radio(
    "Dependencies",
    ["Only Streamlit", "Manually add dependencies", "Upload requirements.txt"],
)

if dependencies == "Only Streamlit":
    dependency_list = ["streamlit"]

elif dependencies == "Manually add dependencies":
    dependency_list = st_tags(
        label="Dependencies (including version numbers if desired)"
    )

elif dependencies == "Upload requirements.txt":
    f = st.file_uploader("requirements.txt")

    if f is not None:
        dependency_list = f.getvalue().decode("utf-8").splitlines()
    else:
        st.stop()

files_to_include = st.radio(
    "Files to include",
    [
        # "Only streamlit_app.py",
        # "Entire repository",
        # "Entire folder (including subfolders)",
        "Manually add files",
    ],
)

if files_to_include == "Only streamlit_app.py":
    file_list = ["streamlit_app.py"]
elif files_to_include == "Entire repository":
    file_list = Repo(".").git.ls_files().splitlines()
elif files_to_include == "Entire folder (including subfolders)":
    file_list = [str(p) for p in Path(".").rglob("*")]
elif files_to_include == "Manually add files":
    to_include = st.file_uploader("Files to include", accept_multiple_files=True)
    if to_include is not None:
        file_list = [str(Path(file.name).absolute()) for file in to_include]

python_version_ = st.radio(
    "Python version",
    [
        "3.10",
        "3.9",
        "3.8",
        "3.7",
    ],
)

python_version = python_version_.replace(".", "")

secrets_file = st.file_uploader("Secrets file", type="toml")

if secrets_file is not None:
    secrets = secrets_file.getvalue().decode("utf-8")
else:
    secrets = ""

if st.button("Deploy"):
    add_files(
        name,
        file_list,
        dependency_list,
    )
