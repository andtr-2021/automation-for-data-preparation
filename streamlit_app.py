import streamlit as st
import zipfile
import os
import shutil
import os 
import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split

# set the title to be blue color
st.title("Automation for Data Preparation")

# change color to red
st.write("`- This app will automate data preparation to make it easier to handled by different ML libraries.`")

st.write(" ")

st.write("`- Online datasets are usually in the common format. However, different ML libraries require different formats. This app will help you to convert the common format to the converted format.`")

# draw a divider
st.write("---")

# create 2 columns
col1, col2 = st.columns(2)

# column 1
with col1:
    st.write("**Common Format:**")
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
    st.write("**Converted Format:**")
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


st.write("---")

# input folder
st.write("Please update a folder containing images in the default format as a zip file.")
input_zip_file = st.file_uploader("", type=["zip"])

default_folder = 'input_folder'

X = []
y = []

# add some space
st.write(" ")
st.write(" ")

# unzip the input folder
if st.button("Transform"):

    if input_zip_file is not None:

        with zipfile.ZipFile(input_zip_file, 'r') as zip_ref:
             zip_ref.extractall('input_folder')

        # transform the folder
        # check the folder structure to see if it is in the default format
        for folder in os.listdir(default_folder):
            
            if folder != '__MACOSX': # now at the root folder
            
                for class_folder in os.listdir(folder):
                    
                    classimg = os.path.join(folder, class_folder)
                    
                    for file in os.listdir(classimg):
                        curr_file = os.path.join(classimg, file)

                        if curr_file.endswith('.jpg'):
                            
                            img = cv2.imread(curr_file)
                            img = cv2.resize(img, (224, 224))
                            
                            X.append(img)
                            y.append(class_folder)

        X = np.array(X)
        y = np.array(y)

        print(len(X))
        print(len(y))    
        
        # create the new folder with new structure
        # - ouput
        #   - train
        #     - class1
        #       - image1.jpg
        #       - image2.jpg
        #       - ...
        #     - class2
        #   - test
        #     - class1
        #       - image1.jpg
        #       - image2.jpg
        #       - ...
        #     - class2

        output_folder = 'output'

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, random_state=42)

        # create the output folder
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

        # create the class folders
        # train
        # - class1
        # - class2
        # test
        # - class1
        # - class2

        st.write("Transform the folder successfully.")

        # zip the folder
        shutil.make_archive('output_folder', 'zip', 'output')

        def get_binary_file_downloader_html(bin_file, file_label='File'):
            with open(bin_file, 'rb') as f:
                data = f.read()
            bin_str = data
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
            return href
       
        get_binary_file_downloader_html('output_folder.zip', 'Zip File')

        st.write("Download the zip file successfully.")



    

