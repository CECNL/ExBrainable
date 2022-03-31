from contextlib import nullcontext
import json
import tkinter as tk
from tkinter.constants import ANCHOR
import tkinter.ttk as ttk
from tkinter import filedialog
from typing_extensions import IntVar
import numpy as np
import scipy.io
import mne
import pandas as pd


#======= Json file I/O =======
# keys in json file: camelCased
# json file indentation on windows: Alt + Shift + F

def saveInfo(fname, key, value):
    """
    fname: json filename to open
    {key: value} to store 
    """
    with open (fname) as fp:
        file_data = json.load(fp) # read as dict
    file_data[key] = value
    json.dump(file_data, open(fname, 'w'))
    
def getInfo(fname, key):
    """
    fname: json filename to open
    key of value to get 
    """
    with open (fname) as fp:
        file_data = json.load(fp) # read as dict
    return file_data[key]




def ReadData(mode="d"):
    """
    opens file explorer for selection,  and store data or label filenames to read into json file
    mode: "d" for data (default)
          "l" for value
    """
    fileTuple = filedialog.askopenfilenames()
    print(fileTuple)
    
    key = "fileNames"
    if mode == "l":
        key = "labelFileNames"
    
    fileList = getInfo('dataset_info.json', key)

    for t in fileTuple:  # avoided listing listed filename
        if not (t in fileList):
            fileList.append(t) # support cross folder file reading

    saveInfo('dataset_info.json', key, fileList)


class database:
    def __init__(self):
        self.Data = {} # {fname: content}
        self.Label = {} # {fname: content}

    def setData(self):
        """
        read contents from fileNames list and store into self.Data component
        """
        fileList = getInfo('dataset_info.json', "fileNames")
        for fn in fileList:
            try:    
                if '.set' in fn: 
                    data = mne.io.read_epochs_eeglab(fn, uint16_codec='latin1') 
                if '.edf' in fn: 
                    data= mne.io.read_raw_edf(fn,preload= True) 
                self.Data[fn] = data
            except TypeError:
                print('The file format is not supported.')
        print('data',self.Data)

    def setLabel(self):
        """
        read contents from labelFileNames list and store into self.Label component
        """
        labelFileList = getInfo('dataset_info.json', "labelFileNames")
        for fn in labelFileList:
            try:    
                # 問一下label file type & format
                if '.mat' in fn: 
                    label = scipy.io.loadmat(fn)
                if '.txt' in fn: 
                    fp = open(fn)
                    label = fp.read().split('\n')
                    fp.close()

                self.Label[fn] = label
            except TypeError:
                print('The file format is not supported.')

        print('label', self.Label)

        