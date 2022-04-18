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
# json file defaults should be cleared in final version.
def jsonValidation(key, value):
    """
    checking value datatype/filetype validity before dump into json file
    """

    listSet = {"fileNames", "labelFileNames", "shape", "subjects", "sessions"}
    intSet = {"channels", "sampling rate", "trials", "timepoints"}
    # others: montage, onset time
    if key in listSet:
        try:
            if(key == "fileNames" and isinstance(value[0], str)):
                if ('.set' in value or '.edf' in value):
                    return
                else:
                    raise TypeError('dataset file should be in .set or .edf format')
            if(key=="labelFileNames" and isinstance(value[0], str)):
                if ('.mat' in value or '.txt' in value):
                    return
                else:
                    raise TypeError('label file should be in .mat or .txt format')
            
            if(isinstance(value[0], int)):
                return
            typeMsg = 'string'  if (key == "fileNames" or key=="labelFileNames") else'int'
            raise TypeError('value type for %s field expected to be %s'%(key, typeMsg))
        except TypeError as e:
            print(repr(e))
    
    elif key in intSet:
        try:
            if(isinstance(value, int)):
                return
            else:
                raise TypeError('value type for %s field should be int'%(key))
        except TypeError as e:
            print(repr(e))   

def saveInfo(fname, key, value):
    """
    fname: json filename to open
    {key: value} to store 
    """
    try:
        with open (fname) as fp:
            file_data = json.load(fp) # read as dict
        
        jsonValidation(key, value) # caught value type error
        file_data[key] = value
        json.dump(file_data, open(fname, 'w'))
    except FileNotFoundError as e: # file not found error
        print(repr(e))
    except KeyError as e: # key not in json error
        print(repr(e))
    
def getInfo(fname, key):
    """
    fname: json filename to open
    key of value to get 
    """
    try:
        with open (fname) as fp:
            file_data = json.load(fp) # read as dict
        return file_data[key]
    except FileNotFoundError as e:
        print(repr(e))
    except KeyError as e:
        print(repr(e))

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
    subList = getInfo('dataset_info.json', 'subjects')
    sessionList = getInfo('dataset_info.json', 'sessions')
    subject = 0
    session = 0

    for t in fileTuple:  # avoided listing listed filename
        if t not in fileList:
            fileList.append(t) # support cross folder file reading
            subject = t.split('/')[-1].split('_')[0]
            session = t.split('/')[-1].split('_')[1]
            try:
                subList.append(int(subject[1:])) # subject number
                sessionList.append(int(session[:-4])) #session number
                print('sub: ', subject, ' session: ', session)
                saveInfo('dataset_info.json', key, fileList)
                saveInfo('dataset_info.json', 'subjects', subList)
                saveInfo('dataset_info.json', 'sessions', sessionList)
            except ValueError as e: # subj or session is not numeric string
                print(repr(e))

def setEventId():
    """
    edit event id
    """
    IdDict = getInfo('dataset_info.json', "event_ids")
    newDict = dict()
    # auto?
    i = 0
    for key, value in IdDict:
        newDict[i] = value
        i+=1
    saveInfo('dataset_info.json', "event_ids", newDict)


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
                elif '.edf' in fn: 
                    data= mne.io.read_raw_edf(fn,preload= True) 
                self.Data[fn] = data
                print(data.event_id)

                # check shape consistency
                shape = getInfo('dataset_info.json', "shape")
                if shape == []:
                    shape= list(data._data.shape)
                elif shape != data._data.shape:
                    raise ValueError('Data shape inconsistent: should be %s'%(str(shape)))

                # check event_id consistency
                # 這樣是先全部讀完再一起編輯?
                eventIdDict = getInfo('dataset_info.json', "event_ids")
                if eventIdDict == {}:
                    saveInfo('dataset_info.json', "event_ids", data.event_id)
                elif eventIdDict != data.event_id:
                    raise ValueError('Event Id inconsistent')
                
            except OSError as e: # failed to open file?
                print(repr(e))
            except ValueError as e: #shape inconsistent
                print(repr(e))
        

    def setLabel(self):
        """
        read contents from labelFileNames list and store into self.Label component
        """
        labelFileList = getInfo('dataset_info.json', "labelFileNames")
        for lfn in labelFileList:
            try:
                # 問一下label file type & format
                if '.mat' in lfn: 
                    label = scipy.io.loadmat(lfn)
                elif '.txt' in lfn: 
                    fp = open(fn)
                    label = fp.read().split('\n')
                    fp.close() 
                self.Label[lfn] = label
                
                shape = getInfo('dataset_info.json', "shape")
                if shape == []:
                    shape= [list(label._data.shape)[1], 1]
                if shape != [list(label._data.shape)[1], 1]:
                    raise ValueError('Label data shape inconsistent: should be %s'%(str(shape)))
                
            except OSError as e: # failed to open file?
                print(repr(e))
            except ValueError as e: #shape inconsistent
                print(repr(e))
        print('label', self.Label)

    
