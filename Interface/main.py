#!/usr/bin/env python
# coding: utf-8
import sys
import subprocess
import pip

"""
for package in ["pandas","PyQt6","opencv-python","tensorflow ","keras","numpy","scikit-learn"]:
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
"""


from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import *
from PyQt6.QtCore import *
import sys
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings('ignore')
from keras.models import load_model
import cv2
import numpy as np
from cascade import cascade
import ctypes


myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)




cas= cascade()
cas.add(load_model("../model/resnet50.hdf5"))

cas.add(load_model("../model/resnet101.hdf5"))
cas.add(load_model("../model/vgg16.hdf5"))
cas.add(load_model("../model/vgg19.hdf5"))
cas.add(load_model("../model/inceptionResNetV2.hdf5"))
cas.add(load_model("../model/inceptionV3.hdf5"))
cas.add(load_model("../model/xception.hdf5"))
cas.add(load_model("../model/mobileNetV2.hdf5"))





def increase_contrast(img):
    clahe = cv2.createCLAHE(clipLimit=25., tileGridSize=(8,8))
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



class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.page=0
        self.setWindowTitle("Identificateur par veines palamaires")
        self.setWindowIcon(QtGui.QIcon('../Image/cascade.svg'))

        self.resize(350,500)
        self.setAcceptDrops(True)
        self.AddButton(label="", setting=(0,0,350,500), trigger=self.nopurpose,style="background-color :rgb(2,14,26);")

        self.titre=self.AddLabel(label="         Glissez Déposez une image ici", setting=(0,0,300,50))
        self.AddButton(label="", setting=(312,12,20,20),tip="Modèle / binary_accuracy\nMobileNetV2 : 0.9971%\nResnet50 : 0.9982%\nResnet100 : 0.9971%\nVGG16 : 0.9949%\nVGG19 : 0.9950%\nXception : 0.9963%\nInceptionV3 : 0.9957%\nInceptionResNetV2 : 0.9955%", trigger=self.nopurpose,image="../Image/right.svg")

        self.loading,self.template=self.AddButtonVideo(label="",video="../Image/loading3.gif",start=False, setting=(0,350,350,150))
        self.image=self.AddButton(label="",setting=(10,50,330,330),image="../Image/hub.jpg",trigger=self.nopurpose)
        self.show()
        
        
    def AddLabel(self,label,setting,style=None):
        x,y,w,h=setting
        button = QLabel(label, self)
        button.setGeometry(x, y, w, h)
        
        button.setStyleSheet(style)
        button.setFont(QFont("Calibri",15))
        button.setStyleSheet("color: rgb(2, 147, 178)")
        button.show()
        
        return button
        
    def AddButton(self,label,setting,trigger,tip=None,image=None,style=None):
        x,y,w,h=setting
        button = QPushButton(label, self)
        button.setGeometry(x, y, w, h)
   
        button.clicked.connect(trigger)
        button.setStyleSheet("border-image : url(%s);"%image)
        button.setToolTip(tip)

        if style is not None:
            button.setStyleSheet(style)
        button.show()

        return button
    
    def nopurpose(self):
        pass
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            


    

    def dropEvent(self, event): 
        self.loading.jumpToFrame(0)
        print(self.loading.frameCount())
        for _ in range(55):
            time.sleep(0.05)
            self.loading.jumpToNextFrame()
            
            QApplication.instance().processEvents()

        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.titre.setText("Personne %s, image %s"%(f.split("/")[-2],f.split("/")[-1].split(".")[0]))
            self.image.setStyleSheet("border-image : url(%s);"%f)
            test=[]
            test.append(Preprocessing(f))
            cas.predict(np.array(test))
            for _ in range(26):
                time.sleep(0.1)
                self.loading.jumpToNextFrame()
                QApplication.instance().processEvents()
            self.titre.setText("C'est la personne n°%s à %s"%(cas.tiebreak(based_on="most_common"))+"%")
        


           
            
            
    def AddButtonVideo(self,label,setting,video=None,start=True):
        x,y,h,w=setting
        movie = QMovie(self)
        movie.setFileName(video)           # +
        movie.setScaledSize(QSize(h,w))
        movie.jumpToFrame(0)   
        movie.finished.connect(self.test)

        template = QLabel(self)                                       # +
        template.setGeometry(x, y, h, w)
        template.setMovie(movie) 
        template.show()
        if start:
            movie.start()
        button = QPushButton(label,self)
        button.setGeometry(x, y, w, h)
        
        button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        button.show()

        return movie,template
    def test(self):
        print("yes")


app = QApplication(sys.argv)
ui = MainWidget()
ui.show()
ui.setWindowIcon(QtGui.QIcon("../Image/ESME2.png"))
sys.exit(app.exec())

