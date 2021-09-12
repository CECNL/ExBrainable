# Authors: Ya-Lin Huang <yalinhuang.bt06@nycu.edu.tw>
#       
global w_bar, win_main, saveweightfolder, loadweightfile, trainloader, valloader, testloader
global sf, ch, tp, net,epochs, lr, sub, netname, stop_thread, val_ratio, n_class, bs, training_time, situation
global acc, kappa
global montage, electrode
global x_train, y_train, x_test , y_test 

x_train=0
y_train=0
x_test=0
y_test=0 

w_bar= 0
win_main=0
saveweightfolder= 0
loadweightfile=0 

trainloader= 0
valloader =0
testloader= 0
val_ratio=0

n_class=0
epochs=0
lr=0
sub=0
netname=0 
stop_thread= 0
y_pred= 0
acc=0
kappa=0
net=0
sf=0
ch=0
tp=0
bs=0
training_time=0
situation=0

montage=0
electrode=0