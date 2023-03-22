#!/usr/bin/env python
# coding: utf-8

# In[127]:


import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import MaxPooling2D
from keras.layers import Conv2D, Flatten
import cv2
import pathlib
import numpy as np
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping,ModelCheckpoint
from tqdm import tqdm
import pandas as pd
from keras.models import load_model
from collections import Counter
import warnings
import math
warnings.filterwarnings('ignore')


# In[144]:


class cascade:
    def __init__(self):
        self.model_list = []
    def add(self,model):
        self.model_list.append(model)
    def predict(self,array):
        liste=[]
        for model in self.model_list:
            liste2=[]
            for pred in model.predict(array):
                try:
                    liste2.append(list(pred).index(max(list(pred))))
                
                except:
                    liste2.append(None)
            liste.append(liste2)
            self.prediction=liste
        return liste
    def none(self):
        try:
            model_name=[]
            model_tag=[]
            number_of_none=[]
            number_of_not_none=[]
            i=1
            for liste in self.prediction:
                model_name.append("Model %s"%i)
                model_tag.append(str(self.model_list[i-1]))
                number_of_none.append(self.prediction[i-1].count(None))
                number_of_not_none.append(len(self.prediction[i-1])-self.prediction[i-1].count(None))
                i+=1
            self.df=pd.DataFrame({"model name":model_name,"model tag":model_tag,"number of None": number_of_none,"number of not None": number_of_not_none})
            return self.df
        except AttributeError:
            raise AttributeError("Call .predict() function before calling .none()")
    def get_value(self,i):
        liste=[]
        for k in range(len(self.prediction)):
            if self.prediction[k][i]!=None:
                liste.append(self.prediction[k][i])
        return liste
    
    def tiebreak(self,based_on="most_common",accuracy=None):
        if accuracy is None and based_on=="accuracy_model":
            raise SyntaxError("Accuracy must be a list of your model's accuracy in order")
        if based_on not in ["most_common","accuracy_model"]:
            raise SyntaxError("%s is not a valid parameter, use 'most_common or 'accuracy_model'"%based_on)
        print(self.prediction)
        liste=[]
        for k in range(len(self.prediction[0])):
            if based_on=="most_common":
                try:
                    liste.append(Counter(self.get_value(k)).most_common(1)[0][0])
                    num=(Counter(self.get_value(k)).most_common(1)[0][1])
                    prob=1-(0.03**(num))
                except:
                    liste.append(None)
            if based_on=="accuracy_model":
                liste2=[]
                for p in set(self.get_value(k)):
                    liste2.append((p,math.prod([1-accuracy[i] for i, x in enumerate(self.get_value(k)) if x == p and p!=None])))
                #liste.append(self.get_value(k)[liste2.index(min(liste2))])
                try:
                    liste.append(list(set(self.get_value(k)))[liste2.index(min(liste2))])
                except:
                    liste.append(None)
        return str(liste[0]+1) , str(prob)[:5]

