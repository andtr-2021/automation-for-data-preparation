import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

X = []
y = []

default_folder = 'input_folder'
for folder in os.listdir(default_folder):
    if folder != '__MACOSX':
        print(folder)
        for class_folder in os.listdir(folder):
            print(class_folder)
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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8, random_state=42)

output_folder = 'output101'

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



