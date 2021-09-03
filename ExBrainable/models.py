import torch
import torch.nn as nn
import math
import scheme_var


class EEGNet(nn.Module):
    def __init__(self):
        super(EEGNet, self).__init__()

        self.tp= scheme_var.tp
        self.ch= scheme_var.ch
        self.sf= scheme_var.sf
        self.n_class=scheme_var.n_class
        self.half_sf= math.floor(self.sf/2)
        print(f'timepoint:{self.tp}',
              f'\nch:{self.ch}',
              f'\nsf:{self.sf}',
              f'\nclasses:{self.n_class}'
            )

        self.F1 = 8
        self.F2 = 16
        self.D = 2 #spatial filters 
        
        self.conv1 = nn.Sequential(  
        #temporal kernel size(1, floor(sf*0.5)) means 500ms EEG at sf/2
        #padding=(0, floor(sf*0.5)/2) maintain raw data shape 
            nn.Conv2d(1, self.F1, (1, int(self.half_sf)), padding=(0, int(self.half_sf/2)), bias=False),
            nn.BatchNorm2d(self.F1)
        )

        self.conv2 = nn.Sequential(       
            # spatial kernel size (n_ch, 1)
            nn.Conv2d(self.F1, self.D*self.F1, (self.ch, 1), groups=self.F1, bias=False),
            nn.BatchNorm2d(self.D*self.F1),
            nn.ELU(),
            nn.AvgPool2d((1, 4)), #reduce the sf to sf/4
            nn.Dropout(0.5) # 0.25 in cross-subject classification beacuse the training size are larger 
        )

        self.Conv3 = nn.Sequential(
        # kernel size=(1, floor((sf/4))*0.5) means 500ms EEG at sf/4 Hz 
            nn.Conv2d(self.D*self.F1, self.D*self.F1, (1, int(self.half_sf/4)), padding=(0, int(self.half_sf/8)), groups=self.D*self.F1, bias=False),
            nn.Conv2d(self.D*self.F1, self.F2, (1, 1), bias=False),
            nn.BatchNorm2d(self.F2),
            nn.ELU(),
            nn.AvgPool2d((1, 8)), #dim reduction
            nn.Dropout(0.5)
        )
        
        #(floor((sf/4))/2 * timepoint//32, n_class)
        self.classifier = nn.Linear(int(self.half_sf/4)* int(self.tp//32), self.n_class, bias=True)
       
    def forward(self, x):
        x = self.conv1(x)
        #print(x.shape)
        x = self.conv2(x)
        #print(x.shape)
        x = self.Conv3(x)
        #print(x.shape)
        #(-1, sf/8* timepoint//32)
        x = x.view(-1, int(self.half_sf/4)* int(self.tp//32))
        #print(x.shape)
        x = self.classifier(x)
       
        return x

class SCCNet(nn.Module):
    def __init__(self):
        super(SCCNet, self).__init__() # input:bs, 1, channel, sample

        self.tp= scheme_var.tp
        self.ch= scheme_var.ch
        self.sf= scheme_var.sf
        self.n_class=scheme_var.n_class
        self.octsf= math.floor(self.sf*0.1)

        print(f'timepoint:{self.tp}',
        f'\nch:{self.ch}',
        f'\nsf:{self.sf}',
        f'\nclasses:{self.n_class}')


        # (1, n_ch, kernelsize=(n_ch,1))
        self.conv1 = nn.Conv2d(1, 22, (self.ch, 1))  
        self.Bn1 = nn.BatchNorm2d(22) #(n_ch) 
        #kernelsize=(1, floor(sf*0.1)) padding= (0, floor(sf*0.1)/2)
        self.conv2 = nn.Conv2d(22, 20, (1, int(self.octsf)), padding=(0, int(self.octsf/2))) 
        self.Bn2   = nn.BatchNorm2d(20)
        
        self.Drop1 = nn.Dropout(0.5) 
        #kernelsize=(1, sf/2) revise to 128/2?  stride=(1, floor(sf*0.1))
        self.AvgPool1 = nn.AvgPool2d((1, int(self.sf/2)), stride=(1, int(self.octsf))) 
        # (20* ceiling((timepoint-sf/2)/floor(sf*0.1)), n_class)
        self.classifier = nn.Linear(20*int(math.ceil((self.tp- self.sf/2)/ self.octsf)), self.n_class, bias=True)
        

    def forward(self, x):
        x = self.conv1(x) #(128,22,1,562)
        #print(x.shape)
        x = self.Bn1(x) 
        x = self.conv2(x) #(128,20,1,563)
        #print(x.shape)
        x = self.Bn2(x)
        x = x ** 2
        x = self.Drop1(x)
        x = self.AvgPool1(x) #(128,20,1,42)
        #print(x.shape)
        x = torch.log(x) 
        x = x.view(-1, int(20*math.ceil((self.tp- self.sf/2)/ self.octsf)))
        x = self.classifier(x)

       
        return x


class ShallowConvNet(nn.Module):
    def __init__(self):
        super(ShallowConvNet, self).__init__()

        self.tp= scheme_var.tp
        self.ch= scheme_var.ch
        self.sf= scheme_var.sf
        self.n_class=scheme_var.n_class
        self.octsf= int(math.ceil(self.sf*0.1)) #13
        self.tpconv1= int(self.tp- self.octsf+1) #550 time point after conv1 
        self.apstride= int(math.ceil(self.octsf/2))
 
        print(f'timepoint:{self.tp}',
              f'\nch:{self.ch}',
              f'\nsf:{self.sf}',
              f'\nclasses:{self.n_class}')
        
        # kernel size=(ceil(sf*0.1)
        self.conv1 = nn.Conv2d(1, 40, (1, self.octsf), bias=False)
        #(n_ch,1)
        self.conv2 = nn.Conv2d(40, 40, (self.ch, 1), bias=False)
        self.Bn1   = nn.BatchNorm2d(40)
       # not sure 
        self.AvgPool1 = nn.AvgPool2d((1, int(self.apstride*5)), stride=(1,self.apstride ))
       
        self.Drop1 = nn.Dropout(0.25)
        self.classifier = nn.Linear(int(40*math.ceil((self.tpconv1-self.apstride*5) / self.apstride)), 
                                    self.n_class, bias=True)
        

    def forward(self, x):
        x = self.conv1(x)
        #print('conv1',x.shape) # 36,40,22,550(no padding)
        x = self.conv2(x)
        #print('conv2',x.shape) # 36,40,1,550 
        x = self.Bn1(x)
        #print('bn1',x.shape) 
        x = x ** 2
        x = self.AvgPool1(x)
        #print('avp',x.shape) # 36,40,1,74 
        x = torch.log(x)
        x = self.Drop1(x)
        #print('drop1',x.shape)
        x = x.view(-1, int(40*math.ceil((self.tpconv1-self.apstride*5 )/ self.apstride))) #40*74
        x = self.classifier(x)

        #x = self.softmax(x)
        return x