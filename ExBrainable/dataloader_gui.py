import torch
import torch.utils.data as Data
import scipy.io
import scheme_var


    
def Individual_Dataset(X_train, Y_train,X_test, Y_test, FT= False):

    bs= scheme_var.bs
    ratio= scheme_var.val_ratio
    n_cuda= scheme_var.n_cuda 

    dev= torch.device(f"cuda:{n_cuda}") if torch.cuda.is_available() else torch.device("cpu")
    
    
    # data1 = scipy.io.loadmat(X_train)
    # data2 = scipy.io.loadmat(Y_train)
    # data3 = scipy.io.loadmat(X_test)
    # data4 = scipy.io.loadmat(Y_test)


    # x_T= torch.Tensor(data1['x_train']).unsqueeze(1)
    # y_T= torch.Tensor(data2['y_train']).view(-1)
    # x_test= torch.Tensor(data3['x_test']).unsqueeze(1)
    # y_test= torch.Tensor(data4['y_test']).view(-1)
    
    x_T= torch.Tensor(X_train).unsqueeze(1)
    y_T= torch.Tensor(Y_train).view(-1)
    x_test= torch.Tensor(X_test).unsqueeze(1)
    y_test= torch.Tensor(Y_test).view(-1)

    x_train, y_train, x_val, y_val= train_val_split(x_T, y_T, ratio)


    
    x_train= x_train.to(dev)
    y_train= y_train.long().to(dev)
    x_val= x_val.to(dev)
    y_val= y_val.long().to(dev)
    x_test= x_test.to(dev)
    y_test= y_test.long().to(dev)
    
        
    print('x_train shape:', x_train.shape)
    print('y_train shape:', y_train.shape)
    print('x_val shape:', x_val.shape)
    print('y_val shape:', y_val.shape)
    print('x_test shape:', x_test.shape)
    print('y_test shape:', y_test.shape)
       
    Train_Dataset = Data.TensorDataset(x_train, y_train )
    Val_Dataset = Data.TensorDataset(x_val, y_val )
    Test_Dataset = Data.TensorDataset(x_test, y_test )
    
    
    Trainloader = Data.DataLoader(Train_Dataset, 
                                  batch_size= bs,
                                  shuffle= True,
                                  num_workers = 0)

    Valloader = Data.DataLoader(Val_Dataset, 
                                  batch_size= len(y_val),
                                  shuffle= False,
                                  num_workers = 0)
    
    Testloader = Data.DataLoader(Test_Dataset, 
                                  batch_size= 1,
                                  shuffle= False,
                                  num_workers = 0)

                            
    return Trainloader,  Valloader, Testloader,  x_train.shape, x_val.shape,  x_test.shape
   


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


    
def Ind_withoutval(trainpath, testpath, bs):

    dev= torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    T = scipy.io.loadmat(trainpath)
    E = scipy.io.loadmat(testpath)

    x_train= torch.Tensor(T['x_train'])
    y_train= torch.Tensor(T['y_train']).view(-1)
    x_train= x_train.unsqueeze(1).to(dev)
    y_train= y_train.view(-1).long().to(dev)
    x_test= torch.Tensor(E['x_test']).unsqueeze(1).to(dev)
    y_test= torch.Tensor(E['y_test']).view(-1).long().to(dev)
    
    Train_Dataset = Data.TensorDataset(x_train, y_train )
    Test_Dataset = Data.TensorDataset(x_test, y_test )
    
    
    Trainloader = Data.DataLoader(dataset= Train_Dataset, 
                                  batch_size= bs,
                                  shuffle= True)
    
    Testloader = Data.DataLoader(dataset= Test_Dataset, 
                                  batch_size= 1,
                                  shuffle= False)
                                 
    return Trainloader,  Testloader, x_train.shape, x_test.shape