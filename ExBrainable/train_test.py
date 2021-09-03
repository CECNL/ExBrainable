import torch
import torch.optim as optim
import torch.nn as nn

import numpy as np
import tkinter as tk
from tkinter import ttk
import time
            
            
def Test():

    weightfolder= scheme_var.weightfolder
    Testloader= scheme_var.testloader
    net= scheme_var.net

    net.load_state_dict(torch.load(f'{weightfolder}/temp.pth'))
    net.eval()

    correct=0
    
#     classes = ('left_arm', 'right_arm', 'leg', 'tongue')
#     class_correct = list(0. for i in range(4))
#     class_total = list(0. for i in range(4))
    
    #yt_ =[]
    ypred=np.zeros((288))
    ypr=np.zeros((288,scheme_var.n_class))
    softmax = nn.Softmax(dim=1)
    flag=0

    for xt,yt in Testloader:
        with torch.no_grad():
            output= net(xt)
            nor_y= softmax(output).reshape(-1)
            #print(nor_y[:,nor_y.argmax()])
            if output.argmax() == yt:
                correct+=1

            #yt_.append( yt.detach().cpu().numpy())
            ypred[flag]= nor_y.argmax().detach().cpu().numpy()
            ypr[flag]= nor_y.detach().cpu().numpy()
            flag+=1

        # acc for each class
#         c = (yt_pred == yt)
#         for i in range(yt.size(0)):
#             label = yt[i]
#             class_correct[label] += c[i].item()
#             class_total[label] += 1

    acc= correct/ len(Testloader)
    

    print('=================')
    print(f' Acc: {acc:.4f}')
    print('=================')
    
    #yt_= np.asarray(yt_)

#     for i in range(4):
#         print(f'{classes[i]} : {(class_correct[i] / class_total[i]):.4f}')
#     print('=================')

    return acc, ypred, ypr

#=======================main=================================
import variable
import scheme_var

def Scheme():
    epochs= scheme_var.epochs
    trainloader= scheme_var.trainloader
    Valloader= scheme_var.valloader
    weightfolder= scheme_var.weightfolder
    netname= scheme_var.netname
    savedweight= scheme_var.savedweight
    n_cuda= scheme_var.n_cuda


   
    dev = torch.device(f"cuda:{n_cuda}" if torch.cuda.is_available() else "cpu")
    net= netname.to(dev)
    #FT mode
    if savedweight !=0 : 
        print('aaaaaaaaaaaaaaaaa ft')
        net.load_state_dict(torch.load(savedweight))
        
    criterion = nn.CrossEntropyLoss() 
    opt = optim.Adam(net.parameters(),lr= scheme_var.lr)
    
    min_loss=1e10
    for epoch in range(1,epochs+1):
        if scheme_var.stop_thread== False:
            print(scheme_var.stop_thread)
            scheme_var.net= net #update net for testing 
            variable.update_epo= epoch
            time.sleep(0.1) 

            tloss= 0
            for x, y in trainloader:
                net.train()
                y_pred= net(x)
                tloss_ = criterion(y_pred, y)
                tloss+= tloss_
                tloss_.backward()
                opt.step()
                opt.zero_grad()

            net.eval()   
            vloss=0
            for xv, yv in Valloader:
                with torch.no_grad():
                    yv_pred= net(xv)
                    vloss_ = criterion(yv_pred, yv)
                    vloss += vloss_.item()
                    
            if vloss< min_loss:
                min_loss= vloss
                torch.save(net.state_dict(), f'{weightfolder}/temp.pth')
                
            if (epoch + 1) % 10 == 0:
                print(f"epoch:{epoch+1}  tloss:{tloss:.4f} vloss:{vloss:.4f} minloss:{min_loss:.4f}")

        else:
                break
    

    # if scheme_var.stop_thread == False:
    #     acc_,y_true , scheme_var.ypred, scheme_var.ypr = Test(weightfolder, testloader, net= net )
    #     scheme_var.acc.set(f'Accuracy: {acc_:4f}')
        
    


        
