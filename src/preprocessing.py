import pathlib
import cv2
import numpy as np

class Preprocessing:
    def __init__(self,directory):
        self.list_image=[]
        self.directory=directory
       
    def init(self):
        for path in pathlib.Path(r"%s"%self.directory).iterdir():
            for path2 in pathlib.Path(path).iterdir():
                self.list_image.append(cv2.imread(r"%s"%path2))
                
    def increase_contrast(self,value=50.):
        liste=[]
        for img in self.list_image:
            clahe = cv2.createCLAHE(clipLimit=value, tileGridSize=(8,8))
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
            l, a, b = cv2.split(lab)  # split on 3 different channels
            l2 = clahe.apply(l)  # apply CLAHE to the L-channel
            lab = cv2.merge((l2,a,b))  # merge channels
            liste.append(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR))  # convert from LAB to BGR
        self.list_image=liste
        return self.list_image
    
    def colorize(self, color):
        liste=[]
        for img in self.liste_image:
            liste.append(cv2.cvtColor(img, color))
        self.list_image=liste
        return self.list_image