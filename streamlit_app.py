import streamlit as st

st.title("Automation for Data Preparation")

# change color to red
st.write("This app offers a simple way to automate data preparation for machine learning.")

# create 2 columns
col1, col2 = st.columns(2)

# column 1
with col1:
    st.subheader("**Default Format**")
    st.write("Usually, online image datasets are in this kind of format:")
    st.write("- root\n"
             "  - class1\n"
             "    - image1.jpg\n"
             "    - image2.jpg\n"
             "    - image3.jpg\n"
             "    - ...\n"
             "  - class2\n"
                "    - image1.jpg\n"
                "    - image2.jpg\n"
                "    - ...\n"
             "  - class3\n"
                "    - image1.jpg\n"
                "    - image2.jpg\n"
                "    - ...\n")




# column 2
with col2:
    # make the text bold
    st.subheader("**New Format**")
    st.write("**This app will create a new folder following structure:**")
    st.write("- root\n"
                "  - train\n"
                "    - class1\n"
                "      - image1.jpg\n"
                "      - image2.jpg\n"
                "      - ...\n"
                "    - class2\n"

                "  - test\n"
                "    - class1\n"
                "      - image1.jpg\n"
                "      - image2.jpg\n"
                "      - ...\n"
                "    - class2\n"
                "       - image1.jpg\n")

# input folder
st.write("### Input Folder")
st.write("Please update a zip file containing images in the default format.")
input_zip_file = st.file_uploader("Upload a zip file", type=["zip"])

# unzip the zip file
import zipfile
import os
import shutil

if st.button("Transform"):
    if input_zip_file is not None:
        with zipfile.ZipFile(input_zip_file, 'r') as zip_ref:
            zip_ref.extractall('input_folder')
        st.write("Unzip the zip file successfully.")

# store the default folder 
default_folder = 'input_folder'

