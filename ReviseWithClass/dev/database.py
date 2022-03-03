import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np



class Database():
    def __init__(self):
        self.data = Data()
        self.weight = Weight()
        self.model = Model()
        self.set_var = Setting_Variable()



class Data():
    def __init__(self):
        
        self.train_dataloader = None
        self.test_dataloader = None
        self.validate_dataloader = None
       
        # new added from data split
        self.Data = None # dict
        self.Label= None # dict
        self.DataInfo= None # pd.dataframe
        self.TrainData = None
        self.TestData = None
        self.ValData = None
        self.TrainLabel= None
        self.ValLabel= None
        self.TestLabel= None
        self.kfoldTrainValidx= None
        
        # new added from individual panel
        self.ExcludedClass  = None
        self.SelectedOnset = None
        
        self.TrainFile= None
        self.ValFile = None
        self.TestFile= None
       
        self.TrainValratio = None
        self.TrainTestratio = None
        
        #self.AllSub= ['1','3','4','5','7','8']
        self.kfold= None
        self.autosplit= None
        # self.AllSub= {'1': ['1','2'], 
        #               '3': ['1','2'],
        #               '4': ['1','2'],
        #               '5': ['1','2'],
        #               '7': ['1','2'],
        #               '8': ['1','2'] }
    

class Weight():
    def __init__(self):
        self.conv1 = None
        self.conv2 = None



class Model():
    def __init__(self):
        self.net = None



class Setting_Variable():
    def __init__(self):
        

        self.win_main_x= 0
        self.win_main_y= 0
        self.sf = 0
        self.tp = 0
        ######
        self.w_bar = 0
        self.win_main = 0
        self.saveweightfolder = 0
        self.loadweightfile = 0
        self.val_ratio = 0
        self.n_class = 0
        self.epochs = 0
        self.lr = 0
        self.sub = 0
        self.netname = 0  
        self.stop_thread = 0
        self.y_pred = 0
        self.acc = 0
        self.kappa = 0
        self.net = 0
        
        self.ch = 0
        
        self.bs = 0
        self.training_time = 0
        self.situation = 0
        self.montage = 0
        self.electrode = 0