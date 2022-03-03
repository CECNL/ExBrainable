import tkinter as tk
from tkinter.constants import ANCHOR
import tkinter.ttk as ttk
from typing_extensions import IntVar
import numpy as np
import scipy.io
import mne
from tkinter import filedialog
import pandas as pd


class LoadData:
    def __init__(self,database):
        self.data= database.data
        self.data.Data= {}
        self.data.Label={}

    def ReadData(self, frame):
        fileList = filedialog.askopenfilenames()

        for index, path in enumerate(fileList):
            fname= path.split('/')[-1]
            tk.Label(frame, text= fname, bg='White').pack(fill='both',padx=20)

            self.data.Data[fname]= self.ReadFiles(path)
            print(self.data.Data[fname].event_id)
            sub, session =self.splitsubsession(fname)
            df= self.MakeInfo(self.data.Data[fname], sub, session)

            if 'Info' not in locals(): #revised 
                Info= df
            else:
                temp= df
                Info= pd.concat([Info, temp])

            self.data.DataInfo= Info # each file has a raw in Data , all file events in info
            print(self.data.DataInfo)

    
    def ReadLabels(self, frame):
        files = filedialog.askopenfilenames()
        print('Read Labels')

    def splitsubsession(self,fname):  
        sfname= fname.split('_') # revise: cross subject
        sub = [int(i) for i in sfname[0] if i.isdigit()]
        sub = [j for j in sub if j>0]
        session = [int(s) for s in sfname[1] if s.isdigit()]

        return sub[0], session[0]

    def ReadFiles(self,path):

        '''read files based on filetype'''
        try:    
            if '.set' in path: 
                data = mne.io.read_epochs_eeglab(path, uint16_codec='latin1')  
                

            if '.edf' in path: 
                data= mne.io.read_raw_edf(path,preload= True) 

            # .txt revise

            return data

        except TypeError:
            print('The file format is not supported.')

    def MakeInfo(self,raw, sub,session): # sub,session : int
        onset= np.diff(raw.events[:,0])
        # insert length of last trial, make sure order is (trial, ch, tp)
        onset= np.insert(onset, len(raw.events)-1 , raw._data[-1,-1,:].shape , axis=0) 
        data={ 'Subject': [sub]* len(raw.events),
            'Session': [session]* len(raw.events), 
            'Class': raw.events[:,2],
            'Onset time':  onset}
        df= pd.DataFrame(data)

        return df
        

'''
class DataSplit
- Info (should move to load data)
  DataInfo(): stack info of each file
  MakeInfo(): sub/session/onset/class of event -> pd.dataframe
- Sort(): split data based on choices of 1. None 2. Split from train 3. choose a file
    Sortbycriteria(): convert filename into sub/session intlist  2. filtering onset/class/session
- Split(): kfold, train/val ,train/test split
    SplitData(): sklearn normal and stratified kfold
'''
from sklearn.model_selection import KFold, StratifiedKFold

class DataSortandSplit:
    def __init__(self,data):
        self.data= data

        # self.data.ExcludedClass  = ['1','2'] # mne event num 1~n, eventdict revise
        # self.data.ExcludedClass = [int(i) for i in self.data.ExcludedClass] #revised ok
        # self.data.SelectedOnset = '-100~3000'
        # self.data.TrainFile = ['S03_1.set']
        # #self.data.ValFile = ['S03_1.set'] 
        # #self.data.ValFile = None
        # self.data.TestFile = ['S03_2.set']
        # #self.data.TestFile = None
        # self.data.TrainValratio = None
        # self.data.TrainTestratio = None
        # self.data.kfold= 4

        #print(f'kfold: {self.data.kfold}')
        #print(f'excluded class: {self.data.ExcludedClass}')
        #print(f'TrainValratio: {self.data.TrainValratio}')
        #print(f'TrainTestratio: {self.data.TrainTestratio}')
        
        self.data.Info= self.data.DataInfo
        self.main()
    
    def main(self):

        if self.data.kfold == None:
            print('no kfold')
            self.Train()
            self.Test()
            self.Validation()
        else: 
            print('kfold split')
            
            self.Train()
            self.Test()

            '''kfold'''
            ratio= self.data.kfold
            iterate = True
            self.data.kfoldTrainValidx=self.SplitData(self.data.TrainData._data, self.data.TrainLabel,ratio= ratio, kfold='Stratified', iterate= iterate)
            print(self.data.TrainData.events)
            print('fold 1 train',self.data.TrainLabel[self.data.kfoldTrainValidx[0]])
            print('fold 1 test',self.data.TrainLabel[self.data.kfoldTrainValidx[1]])
            print('fold 2 train',self.data.TrainLabel[self.data.kfoldTrainValidx[2]])
            print('fold 2 test',self.data.TrainLabel[self.data.kfoldTrainValidx[3]])
            print('fold 3 train',self.data.TrainLabel[self.data.kfoldTrainValidx[4]])
            print('fold 3 test',self.data.TrainLabel[self.data.kfoldTrainValidx[5]])
            print('fold 4 train',self.data.TrainLabel[self.data.kfoldTrainValidx[6]])
            print('fold 4 test',self.data.TrainLabel[self.data.kfoldTrainValidx[7]])

       
    def Train(self):
        '''Train'''
        print(self.data.TrainFile)
        self.data.TrainData, self.data.TrainLabel, self.Trainsub, self.Trainsess= self.Sortbycriteria(self.data.TrainFile) # onset, class
        
        print('Trainsub/sess: ',self.Trainsub, self.Trainsess)
        print('Train seleted data: ',self.data.TrainData)   
        print('shape',self.data.TrainData._data.shape)
        print('label shape', self.data.TrainLabel.shape)

    def Test(self):
        '''Test'''
        # split from train
        if self.data.TrainTestratio != None: 
            print('split from train')
            self.Testsub = self.Trainsub
            self.Testsess= self.Trainsess
            self.data.TrainData, self.data.TestData, self.data.TrainLabel, self.data.TestLabel=self.SplitfromTrain(self.data.TrainTestratio)
            
            print('Test seleted data: ',self.data.TestData)   
            print('shape',self.data.TestData._data.shape)
            print('label shape', self.data.TestLabel.shape)
         # choose test file
         
        elif self.data.TestFile != None: 
            print('choose test file')    
            self.data.TestData, self.data.TestLabel, self.Testsub, self.Testsess =self.Sortbycriteria(self.data.TestFile)

        
            
            print('Test seleted data: ',self.data.TestData)   
            print('shape',self.data.TestData._data.shape)
            print('label shape', self.data.TestLabel.shape)

        else: 
            print('No test data and labels')
        
    def Validation(self):
        '''Validation'''
        # split from train
        if self.data.TrainValratio != None: 
            print('split from train')
            self.Valsub = self.Trainsub
            self.Valsess= self.Trainsess
            self.data.TrainData, self.data.ValData, self.data.TrainLabel, self.data.ValLabel=self.SplitfromTrain(self.data.TrainValratio)

            print('Val seleted data: ',self.data.ValData)   
            print('shape',self.data.ValData._data.shape)
            print('label shape', self.data.ValLabel.shape)

        # choose val file 
        elif self.data.ValFile != None: 
            print('choose val file')    
            self.data.ValData, self.data.ValLabel,self.Valsub, self.Valsess= self.Sortbycriteria(self.data.ValFile[0])
            
        
            print('Val seleted data: ',self.data.ValData)   
            print('shape',self.data.ValData._data.shape)
            print('label shape', self.data.ValLabel.shape)

        else:
            print('No val data and labels')
        
    def SplitfromTrain(self, ratio):
        iterate= False
        TrainTestidx=self.SplitData(self.data.TrainData._data, self.data.TrainLabel,ratio= ratio, kfold='Stratified', iterate= iterate)
        traindata= self.data.TrainData[TrainTestidx[0]]
        testdata= self.data.TrainData[TrainTestidx[1]]
        trainlabel= self.data.TrainLabel[TrainTestidx[0]]
        testlabel= self.data.TrainLabel[TrainTestidx[1]]

        return traindata, testdata, trainlabel, testlabel

    def Sortbycriteria(self, Filename):
        
        '''split file string into sublist, sessionlist'''# intlist
        file= Filename.split('_') # revise: cross subject
        SelectedSub = [int(i) for i in file[0] if i.isdigit()]
        SelectedSub = [j for j in SelectedSub if j>0]
        SelectedSession = [int(s) for s in file[1] if s.isdigit()]
        
        if self.data.ExcludedClass != None:
            Eclass= self.data.ExcludedClass
            self.data.ExcludedClass= [int(s) for s in Eclass ]
        

        '''filtering subject/session/class/onset(revised)'''
        include= self.data.Info['Subject'].isin(SelectedSub)
        SelectedData= self.data.Info[include]
        #print(SelectedData)
        include= SelectedData['Session'].isin(SelectedSession)
        SelectedData= SelectedData[include]
        
        if self.data.ExcludedClass != None: 
            mask= SelectedData['Class'].isin(self.data.ExcludedClass)
            SelectedData= SelectedData[~mask]

        # onsettime

        '''select array by index'''
        index= SelectedData.index
        SelectedData= self.data.Data[Filename][index]
        SelectedLabel= np.asarray(SelectedData.events[:,2])
    
        return SelectedData, SelectedLabel, SelectedSub, SelectedSession # dataframe 
        #SelectedSub, SelectedSession : list .ex: [3]

  

       
    '''iterate= False -> 只有kfold第一份，拿來當單純的split
    iterate= True -> 完整的kfold
    '''
    def SplitData(self,data, label, ratio, kfold='Stratified', iterate= True):
        TrainTestidx= [] # even: Train, odd: Test

        if kfold == 'Stratified':
            kf = StratifiedKFold(n_splits=ratio, shuffle= True, random_state= 1)
            split= kf.split(data,label)
        elif kfold == 'normal':
            kf = KFold(n_splits=ratio, shuffle= True,random_state= 1)
            split = kf.split(data)

        for trainidx, testidx in split:
            TrainTestidx.append(trainidx)
            TrainTestidx.append(testidx)
            if iterate ==False: # train/val split只需要第一份
                break

        
        return TrainTestidx
       
