# Authors: Ya-Lin Huang <yalinhuang.bt06@nycu.edu.tw>
#          Xin-Yao Huang <masaga.cs05@nctu.edu.tw>

import torch
import torch.optim as optim
import torch.nn as nn

import numpy as np
import tkinter as tk
from tkinter import ttk
import time

import variable
from scheme_var import *
            

class Evaluate():
    def __init__(self, sch_var):
        self.sch_var = sch_var
        self.dev = torch.device(f"cuda:0" if torch.cuda.is_available() else "cpu")

    def Test(self):
        saveweightfolder= self.sch_var.saveweightfolder
        Testloader= self.sch_var.testloader
        net= self.sch_var.net

        net.load_state_dict(torch.load(f'{saveweightfolder}/temp.pth'))
        net.eval()

        correct=0
        flag=0
        ypred=np.zeros((self.sch_var.y_train.shape[0]))
        ypr=np.zeros((self.sch_var.y_train.shape[0], self.sch_var.n_class))
        softmax = nn.Softmax(dim=1)

        if self.sch_var.situation==1:
            for xt,_ in Testloader:
                with torch.no_grad():
                    output= net(xt)
                    nor_y= softmax(output).reshape(-1)
                    ypred[flag]= nor_y.argmax().detach().cpu().numpy()
                    ypr[flag]= nor_y.detach().cpu().numpy()
                    flag+=1

            return ypred, ypr

        if self.sch_var.situation==2:
            for xt,yt in Testloader:
                with torch.no_grad():
                    output= net(xt)
                    nor_y= softmax(output).reshape(-1)
                    #print(nor_y[:,nor_y.argmax()])
                    if output.argmax() == yt:
                        correct+=1
                    ypred[flag]= nor_y.argmax().detach().cpu().numpy()
                    ypr[flag]= nor_y.detach().cpu().numpy()
                    flag+=1

            acc, k= kappa(net, Testloader, self.sch_var)
            return acc, k, ypred, ypr


    def kappa(self, net, testloader):
        net.eval()
        classNum = self.sch_var.n_class
        softmax = nn.Softmax(dim=1)
        table = np.zeros((classNum, classNum))
        for xb, yb in testloader:
            pred = net(xb)
            pred = torch.argmax(softmax(pred))
            table[int(pred.item()), int(yb.item())] += 1
        P0 = np.diagonal(table).sum() / table.sum()
        Pe = sum([table[:,i].sum() * table[i].sum() for i in range(classNum)]) / (table.sum() * table.sum())
        print('acc',  P0)
        print('kappa', (P0 - Pe) / (1 - Pe))
        return P0,(P0 - Pe) / (1 - Pe)


    def Scheme(self):
        epochs= self.sch_var.epochs
        trainloader= self.sch_var.trainloader
        Valloader= self.sch_var.valloader
        saveweightfolder= self.sch_var.saveweightfolder
        netname= self.sch_var.netname
        loadweightfile= self.sch_var.loadweightfile
        new_sch_var = self.sch_var

        start= time.time()
        net= netname.to(self.dev)
        #FT mode
        if loadweightfile != 0 : 
            print('Fine-tuning')
            net.load_state_dict(torch.load(loadweightfile, map_location= "cuda:0" if torch.cuda.is_available() else "cpu"))
        
        criterion = nn.CrossEntropyLoss() 
        opt = optim.Adam(net.parameters(),lr= self.sch_var.lr)
    
        min_loss=1e10
        for epoch in range(1,epochs+1):
            if self.sch_var.stop_thread == False:
                print(self.sch_var.stop_thread)
                new_sch_var.net = net #update net for testing 
                variable.update_epo = epoch
                time.sleep(0.1) 

                tloss= 0
                for x, y in trainloader:
                    net.train()
                    y_pred = net(x)
                    tloss_ = criterion(y_pred, y)
                    tloss += tloss_
                    tloss_.backward()
                    opt.step()
                    opt.zero_grad()

                net.eval()   
                vloss=0
                for xv, yv in Valloader:
                    with torch.no_grad():
                        yv_pred = net(xv)
                        vloss_ = criterion(yv_pred, yv)
                        vloss += vloss_.item()
                    
                if vloss< min_loss:
                    min_loss = vloss
                    torch.save(net.state_dict(), f'{saveweightfolder}/temp.pth')
                
                if (epoch + 1) % 10 == 0:
                    print(f"epoch:{epoch+1}  tloss:{tloss:.4f} vloss:{vloss:.4f} minloss:{min_loss:.4f}")

            else:
                break
        end= time.time()
        new_sch_var.training_time = end - start

        return new_sch_var

        
    