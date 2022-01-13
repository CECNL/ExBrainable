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
        self.train_data = None
        self.test_data = None
        self.validate_data = None
        self.train_dataloader = None
        self.test_dataloader = None
        self.validate_dataloader = None
        self.train_data_len = 0
        self.test_data_len = 0



class Weight():
    def __init__(self):
        self.conv1 = None
        self.conv2 = None



class Model():
    def __init__(self):
        self.net = None



class Setting_Variable():
    def __init__(self):
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
        self.sf = 0
        self.ch = 0
        self.tp = 0
        self.bs = 0
        self.training_time = 0
        self.situation = 0
        self.montage = 0
        self.electrode = 0