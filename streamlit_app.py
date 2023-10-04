import streamlit as st
import zipfile
import os
import shutil
import os 
import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split

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

if st.button("Transform"):
    if input_zip_file is not None:
        with zipfile.ZipFile(input_zip_file, 'r') as zip_ref:
            zip_ref.extractall('input_folder')
        st.write("Unzip the zip file successfully.")

# store the default folder 
default_folder = 'input_folder'
X = []
y = []

counter = 0
# check the folder structure to see if it is in the default format
for folder in os.listdir(default_folder):
    counter += 1
    if counter == 2:
        for data in os.listdir(folder):
            curr_path = os.path.join(folder, data)
            
            for file in os.listdir(curr_path):
                curr_file = os.path.join(curr_path, file)

                if curr_file.endswith('.jpg'):
                    
                    img = cv2.imread(curr_file)
                    img = cv2.resize(img, (224, 224))
                    X.append(img)
                    y.append(folder)


                
    

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

output_folder = 'output'

for folder in np.unique(y):
    curr_path = os.path.join(output_folder, 'train', folder)
    os.makedirs(curr_path, exist_ok=True)

    curr_path = os.path.join(output_folder, 'test', folder)
    os.makedirs(curr_path, exist_ok=True)

for i in range(len(X_train)):
    curr_path = os.path.join(output_folder, 'train', y_train[i], str(i) + '.jpg')
    cv2.imwrite(curr_path, X_train[i])

for i in range(len(X_test)):
    curr_path = os.path.join(output_folder, 'test', y_test[i], str(i) + '.jpg')
    cv2.imwrite(curr_path, X_test[i])

print('Done')
   
