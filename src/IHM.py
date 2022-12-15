#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap,QFont
import sys
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings('ignore')
from keras.models import load_model
import cv2
import numpy as np
from cascade import cascade
cas= cascade()
cas.add(load_model("out/resnet50.hdf5"))
cas.add(load_model("out/resnet101.hdf5"))
cas.add(load_model("out/vgg16.hdf5"))
cas.add(load_model("out/vgg19.hdf5"))


# In[2]:


def increase_contrast(img):
    clahe = cv2.createCLAHE(clipLimit=50., tileGridSize=(8,8))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    return img 


def Preprocessing(image,noise=0.05):

    
    image=cv2.imread(r"%s"%image)
    
    image=increase_contrast(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))

    return image


# In[ ]:


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.page=0
        self.setWindowTitle("Identificateur par veines palamaires")
        self.resize(720, 480)
        self.setAcceptDrops(True)
        self.label = QLabel("Glissez une image à identifier ici",self)
        self.label.setGeometry(5,5,1000,30)
        self.label.setFont(QFont("Arial",20))
        self.label2 = QLabel("",self)
        self.label2.setGeometry(5,455,1000,20)
        self.label2.setFont(QFont("Arial",15))
        self.show()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event): 
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.label.setText("Personne %s, image %s"%(f.split("/")[-2],f.split("/")[-1].split(".")[0]))
            test=[]
            test.append(Preprocessing(f))
            cas.predict(np.array(test))
            
            self.label2.setText("Réponse du réseau de neurone : C'est la personne n°%s"% str(cas.tiebreak(based_on="most_common")[0]+1))


# In[ ]:





# In[ ]:





# In[ ]:




