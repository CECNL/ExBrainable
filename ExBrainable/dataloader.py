# Authors: Ya-Lin Huang <yalinhuang.bt06@nycu.edu.tw>
#          Xin-Yao Huang <masaga.cs05@nctu.edu.tw>

import torch
import torch.utils.data as Data
import scheme_var

def Individual_Dataset(FT= False):

    bs= scheme_var.bs
    ratio= scheme_var.val_ratio
    situation= scheme_var.situation
    dev= torch.device(f"cuda:0") if torch.cuda.is_available() else torch.device("cpu")
    
    if (situation==0 or situation==1 or situation==2):

        x_T= torch.Tensor(scheme_var.x_train).unsqueeze(1)
        y_T= torch.Tensor(scheme_var.y_train).view(-1)
        x_train, y_train, x_val, y_val= train_val_split(x_T, y_T, ratio)

        x_train= x_train.to(dev)
        y_train= y_train.long().to(dev)
        x_val= x_val.to(dev)
        y_val= y_val.long().to(dev)

        Train_Dataset = Data.TensorDataset(x_train, y_train )
        Val_Dataset = Data.TensorDataset(x_val, y_val )

        Trainloader = Data.DataLoader(Train_Dataset, 
                                  batch_size= bs,
                                  shuffle= True,
                                  num_workers = 0)

        Valloader = Data.DataLoader(Val_Dataset, 
                                  batch_size= len(y_val),
                                  shuffle= False,
                                  num_workers = 0)
        
        print('x_train shape:', x_train.shape)
        print('y_train shape:', y_train.shape)
        print('x_val shape:', x_val.shape)
        print('y_val shape:', y_val.shape)
        

        if (situation==1 or situation==2): 
            x_test= torch.Tensor(scheme_var.x_test).unsqueeze(1)
            x_test= x_test.to(dev)

            if situation==1:
                Test_Dataset = Data.TensorDataset(x_test, torch.zeros(x_test.shape[0]).float())
                Testloader = Data.DataLoader(Test_Dataset, 
                                    batch_size= 1,
                                    shuffle= False,
                                    num_workers = 0)
                print('x_test shape:', x_test.shape)

            if situation==2 : 
                y_test= torch.Tensor(scheme_var.y_test).view(-1)
                y_test= y_test.long().to(dev)
                Test_Dataset = Data.TensorDataset(x_test, y_test )
                Testloader = Data.DataLoader(Test_Dataset, 
                                  batch_size= 1,
                                  shuffle= False,
                                  num_workers = 0)
                
                
                print('y_test shape:', y_test.shape)

            return Trainloader, Valloader, Testloader
        
        else: # situation==0 
            return Trainloader, Valloader 
   


def train_val_split(x_T, y_T, ratio):
    s = y_T.argsort() ## 排序並分開四個class
    x_T = x_T[s]
    y_T = y_T[s]

    cL = y_T[y_T==0].size()[0]

    class1_x = x_T[:cL]
    class2_x = x_T[cL:cL*2]
    class3_x = x_T[cL*2:cL*3]
    class4_x = x_T[cL*3:cL*4]

    class1_y = y_T[:cL]
    class2_y = y_T[cL:cL*2]
    class3_y = y_T[cL*2:cL*3]
    class4_y = y_T[cL*3:cL*4]

    vL= int(len(class1_y )*ratio) #1/32*4=1/8
 

    x_train = torch.cat((class1_x[:-vL], class2_x[:-vL], class3_x[:-vL], class4_x[:-vL]))
    y_train = torch.cat((class1_y[:-vL], class2_y[:-vL], class3_y[:-vL], class4_y[:-vL]))

    x_val = torch.cat((class1_x[-vL:], class2_x[-vL:], class3_x[-vL:], class4_x[-vL:]))
    y_val = torch.cat((class1_y[-vL:], class2_y[-vL:], class3_y[-vL:], class4_y[-vL:]))

    return x_train, y_train, x_val, y_val


    
