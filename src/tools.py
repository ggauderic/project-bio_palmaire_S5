import pathlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
import cv2
import random

# Return X_train, X_test, y_train, y_test
def get_train_test_split(data_path, num_classes, sep):
    X=[]
    y=[]
    for path in pathlib.Path(data_path).iterdir():
        for path2 in pathlib.Path(path).iterdir():
            index = int(str(path).split(sep)[-1])-1
            image=np.array(plt.imread(path2))
            X.append(list(image))
            matrix=np.zeros((num_classes,))
            matrix[index] = 1
            y.append(matrix)

    X=np.array(X)
    y=np.array(y)
           
    return train_test_split(X, y, test_size=0.01, random_state=42)



# Section 2: Image preprocessing

def increase_contrast(img):
    clahe = cv2.createCLAHE(clipLimit=50., tileGridSize=(8,8))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    return img 


def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def flip(img,direction):
    return cv2.flip(img, direction)

def blur(img):
    return cv2.GaussianBlur(img, (11, 11), 0)

def decrease_brightness(img, value=100):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 0 + value
    v[v < lim] = 0
    v[v >= lim] -= value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img    

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img