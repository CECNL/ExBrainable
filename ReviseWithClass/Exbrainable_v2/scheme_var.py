# Authors: Ya-Lin Huang <yalinhuang.bt06@nycu.edu.tw>  
#

class SchemeVariable():
    def __init__(self):
        super(SchemeVariable, self).__init__()

        self.x_train = 0
        self.y_train = 0
        self.x_test = 0
        self.y_test = 0 

        self.w_bar= 0
        self.win_main=0
        self.saveweightfolder= 0
        self.loadweightfile=0 

        self.trainloader= 0
        self.valloader =0
        self.testloader= 0
        self.val_ratio=0

        self.n_class=0
        self.epochs=0
        self.lr=0
        self.sub=0
        self.netname=0 
        self.stop_thread= 0
        self.y_pred= 0
        self.acc=0
        self.kappa=0
        self.net=0
        self.sf=0
        self.ch=0
        self.tp=0
        self.bs=0
        self.training_time=0
        self.situation=0

        self.montage=0
        self.electrode=0