import tkinter as tk
from tkinter.constants import CENTER
from tkinter.ttk import *
from tkinter import messagebox

import threading
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import scipy.io

# from freq_response import *
# from dataloader_gui import Individual_Dataset
# import variable
# import scheme_var
# from train_test import Test, Scheme

from .freq_response import *
from .dataloader_gui import Individual_Dataset
import variable
import scheme_var
from .train_test import Test, Scheme


#====================== Main========================
#--------------------------Control Center----------------------------------
def main(X_train, Y_train, X_test, Y_test):

    global win_main #new
    win_main = tk.Tk()
    win_main.geometry('350x300')
    win_main.title("ExBrainable")
    win_main.configure(background='White')

    # Control Center
    #tk.Label(win_main, text="X_train  :　", bg= 'White').grid(row=0, column=0, ipady=7, padx=20)
    #tk.Label(win_main, text="X_test :　", bg= 'White').grid(row=1, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Trainsize :　", bg= 'White').grid(row=2, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Validsize :　", bg= 'White').grid(row=3, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Testsize :　", bg= 'White').grid(row=4, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Sampliing rate :　", bg= 'White').grid(row=5, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Model :　", bg= 'White').grid(row=6, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Epoch :　", bg= 'White').grid(row=7, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Learning rate :　", bg= 'White').grid(row=8, column=0, ipady=7, padx=20)
    tk.Label(win_main, text="Weight :　", bg= 'White').grid(row=9, column=0, ipady=7, padx=20)

    #create menu
    menubar = tk.Menu(win_main)

    # Menu- File
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='Data Properties ', command=lambda:Load_dataset(X_train, Y_train, X_test, Y_test))
    filemenu.add_command(label='Load model ', command=lambda:load_model_struct())
    filemenu.add_command(label='Load weight ', command=Weightname)

    # Menu-Model
    Model = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Model', menu=Model)
    Model.add_command(label='Training setting', command=lambda:Model_Preparation())
    Model.add_command(label='Start Training', command=(lambda:bar()))
    #Model.add_command(label='Result', command=(lambda:Result()))


    #Menu- Plot
    Plot = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Plot', menu= Plot)
    Plot.add_command(label='Spatial Pattern ', command=lambda:Spatial_kernel(scheme_var.montage,scheme_var.electrode, conv1))
    Plot.add_command(label='Temporal Pattern ', command=lambda:plot_mag(conv2))


    win_main.config(menu=menubar)
    win_main.mainloop()


# Menu- File- Load dataset=================================    
def Load_dataset(X_train, Y_train, X_test, Y_test):

    w=new_window(Title='Load Dataset', size='400x200')
    #topic
    # tk.Label(w, text="x_train :　", bg= 'White').grid(row=0, column=0)
    # tk.Label(w, text="y_train :　", bg= 'White').grid(row=1, column=0)
    # tk.Label(w, text="x_test :　", bg= 'White').grid(row=2, column=0)
    # tk.Label(w, text="y_test :　", bg= 'White').grid(row=3, column=0)
    tk.Label(w, text="Validation ratio :　", bg= 'White').grid(row=4,padx=15)
    tk.Label(w, text="Batchsize :　", bg= 'White').grid(row=5,padx=15)
    tk.Label(w, text="Cuda device :　", bg= 'White').grid(row=6,padx=15)
    tk.Label(w, text="Number of Classes :　", bg= 'White').grid(row=7,padx=15)
    tk.Label(w, text="EEG Montage :　", bg= 'White').grid(row=8,padx=15)
    tk.Label(w, text="Sampling rate :　", bg= 'White').grid(row=9,padx=15)
    tk.Label(w, text="Number of channel :　", bg= 'White').grid(row=10,padx=15)

    #textinput
    # x_train = tk.Entry(w)
    # y_train = tk.Entry(w)
    # x_test = tk.Entry(w)
    # y_test = tk.Entry(w)
    Valratio = tk.Entry(w)
    Batchsize = tk.Entry(w)
    n_cuda = tk.Entry(w)
    n_class = tk.Entry(w)
    sf = tk.Entry(w)
    ch = tk.Entry(w)

    # x_train.grid(row=0, column=1)
    # y_train.grid(row=1, column=1)
    # x_test.grid(row=2, column=1)
    # y_test.grid(row=3, column=1)
    Valratio.grid(row=4, column=1)
    Batchsize.grid(row=5, column=1)
    n_cuda.grid(row=6, column=1)
    n_class.grid(row=7, column=1)
    sf.grid(row=9, column=1)
    ch.grid(row=10, column=1)

    #load train test path by bottom
    # ttk.Button(w, text="File", command=(lambda:path2entry(x_train, 'x_train')), width=10).grid(row=0,column=2)
    # ttk.Button(w, text="File", command=(lambda:path2entry(y_train,'y_train')), width=10).grid(row=1,column=2)
    # ttk.Button(w, text="File", command=(lambda:path2entry(x_test,'x_test')), width=10).grid(row=2,column=2)
    # ttk.Button(w, text="File", command=(lambda:path2entry(y_test, 'y_test')), width=10).grid(row=3,column=2)
    ttk.Button(w, text="Select ", command=(lambda:montage_select(w)), width=10).grid(row=8,column=2)


    Confirm = ttk.Button(w ,text="Confirm", 
                         command=(lambda:show_input(w,Batchsize, Valratio, n_cuda, n_class, sf, ch, X_train, Y_train, X_test, Y_test)), width=10).grid(row=11, column=1, pady=5)

# def path2entry(entry, set_type):
#     path = tk.filedialog.askopenfilename()
#     entry.insert(tk.END, path)
#     data= read_path(path)
#     identify_path_type(path, set_type) #identify path 
#     identify_set_type(data, set_type) #identify data 


# def read_path(path):
#     try: 
#         if '.mat' in path:
#             path = scipy.io.loadmat(path)
#             settype=['x_train', 'y_train', 'x_test', 'y_test']
#             for atype in settype:
#                 if atype in path.keys():
#                     data= path[atype]

#         if '.set' in path: 
#             data = mne.io.read_epochs_eeglab(path)
#             data =data._data
            
#         if '.edf' in path: 
#             data= mne.io.read_raw_edf(path,preload= True)
#             data =data._data
            
#         return data     

#     except TypeError:
#         print('The file format is not supported.')

# def identify_path_type(path, set_type):#辨別 xt, yt, xtest, ytest path

#     global X_trainpath, Y_trainpath, X_testpath, Y_testpath

#     if set_type=='x_train':
#         X_trainpath= path
#     elif set_type=='y_train':
#         Y_trainpath= path
#     elif set_type=='x_test':
#         X_testpath= path 
#     elif set_type=='y_test':
#         Y_testpath= path
        
# def identify_set_type(data, set_type):#辨別 xt, yt, xtest, ytest data

#     global X_train, Y_train, X_test, Y_test

#     if set_type=='x_train':
#         X_train= data
#     elif set_type=='y_train':
#         Y_train= data
#     elif set_type=='x_test':
#         X_test= data 
#     elif set_type=='y_test':
#         Y_test= data



def show_input(w, Batchsize, Valratio, n_cuda, n_class, sf ,ch,X_train, Y_train, X_test, Y_test):

    scheme_var.val_ratio= float(Valratio.get())
    scheme_var.bs= int(Batchsize.get())
    scheme_var.n_cuda= int(n_cuda.get())
    scheme_var.n_class= int(n_class.get())
    scheme_var.sf= int(sf.get())
    scheme_var.ch= int(ch.get())

    w.destroy()


    # tk.Label(win_main, text= "/".join(X_trainpath.split('/')[-2:])).grid(row=0, column=1 )
    # tk.Label(win_main, text= "/".join(X_testpath.split('/')[-2:])).grid(row=1, column=1)


    scheme_var.trainloader, scheme_var.valloader,  scheme_var.testloader, trainsize, validsize,  testsize= Individual_Dataset(X_train, Y_train,X_test, Y_test)
                                                                                                                            
    tk.Label(win_main, text= trainsize, bg= 'White').grid(row=2, column=1 )
    tk.Label(win_main, text= validsize, bg= 'White').grid(row=3, column=1 )
    tk.Label(win_main, text= testsize, bg= 'White').grid(row=4, column=1)
    tk.Label(win_main, text= scheme_var.sf, bg= 'White').grid(row=5, column=1)
    scheme_var.tp= trainsize[-1]

    print('x_train size: ',X_train.shape,
            '\ny_train size: ', Y_train.shape,
            '\nx_test size: ', X_test.shape,
            '\ny_test size: ', Y_test.shape)

    # print('x_train path: ',X_trainpath,
    #         '\ny_train path: ', Y_trainpath,
    #         '\nx_test path: ', X_testpath,
    #         '\ny_test path: ', Y_testpath)


# Menu- File- Load Model=================================    
def load_model_struct(): #load .py with models structure
    win_lms=new_window(Title='Load model structure', size='400x200')
    modelist = ttk.Combobox(win_lms,
                    values=['SCCNet',
                            'EEGNet',
                            'ShallowConvNet',
                            ],
                    state="readonly"
            )

    Confirm = ttk.Button(win_lms ,text="Confirm", command=(lambda:[model_select(win_lms, modelist)]))
    modelist.pack()
    Confirm.pack()

def model_select(win_lms, modelist):
    exec(open('models.py').read(), globals()) #put all variable to globals()
    name = modelist.get()
    print(name)
    scheme_var.netname= eval(str(name+'()'))
    tk.Label(win_main, text=name, bg= 'White').grid(row=6, column=1) #show on center 

    win_lms.destroy()

# Menu- File- Load weight====================================
# def Filename(): #revise
#     name= tk.filedialog.askopenfilename(initialdir = "/")
#     FileName = tk.Label(win_main, text= name)
#     FileName.place(x=90, y=20)

def Weightname():
    global conv1, conv2

    file= tk.filedialog.askopenfilename()
    shortpath= "/".join(file.split('/')[-2:])
    tk.Label(win_main, text= shortpath, bg= 'White').grid(row=9, column=1)
    conv1,conv2= get_weight(filepath=file)
    scheme_var.savedweight= file
#print(f'conv1: {conv1.shape}')
#conv1size = tk.Label(window, text= f'conv1: {conv1.shape}').grid(row=9, column=1)

#conv2size = tk.Label(window, text= f'conv2: {conv2.shape}').grid(row=10, column=1)

# Menu- Model- Set hyperparameter =================================    

def Model_Preparation():
    win_p=new_window(Title='Training setting ', size='400x200')
    #topic
    tk.Label(win_p, text="Epoch :　", bg= 'White').grid(row=0, column=0, ipady=10, padx=20)
    tk.Label(win_p, text="Learning rate :　", bg= 'White').grid(row=1, column=0, ipady=10, padx=20)

    tk.Label(win_p, text="Save weight : 　", bg= 'White').grid(row=2,column=0, ipady=10, padx=20)

    Epoch = tk.Entry(win_p)
    Lr = tk.Entry(win_p)

    Save_weight = tk.Entry(win_p)

    Epoch.grid(row=0, column=1)
    Lr.grid(row=1, column=1)
    Save_weight.grid(row=2, column=1)

    weightfolder= ttk.Button(win_p, text="Folder", command=(lambda:folder2entry(Save_weight)), width=10).grid(row=2,column=2)

    Confirm = ttk.Button(win_p ,text="Confirm", command=(lambda:show_para(win_p, Epoch, Lr)), width=10).grid(row=3, column=1)


def show_para(win_p, Epoch, Lr ):

#global epochs, lr
    scheme_var.epochs= int(Epoch.get())
    scheme_var.lr= float(Lr.get())


    #close w
    win_p.destroy()
    #para in control display 
    tk.Label(win_main, text= scheme_var.epochs, bg= 'White').grid(row=7, column=1 )
    tk.Label(win_main, text= scheme_var.lr, bg= 'White').grid(row=8, column=1)
    tk.Label(win_main, text= shortweightfolder, bg= 'White').grid(row=9, column=1)


# Menu- Model- Start training =================================

def bar(): #w_bar, ypred, ypr remove from scheme_var? 
    global progressbar, value_label, buttom 
    scheme_var.w_bar = new_window(Title='Evaluation', size='350x150')

    progressbar = Progressbar(scheme_var.w_bar, mode='determinate',length= 350, maximum= scheme_var.epochs+1)
    progressbar.pack(anchor= tk.CENTER)

    value_label = tk.Label(scheme_var.w_bar, text= update_progress_label())
    value_label.pack(anchor= tk.CENTER)

    scheme_var.acc= tk.StringVar()
    scheme_var.acc.set('Accuracy: None')
    tk.Label(scheme_var.w_bar, textvariable= scheme_var.acc, bg='White').pack(anchor= tk.CENTER)


    buttom= ttk.Button(scheme_var.w_bar, text="Start Training",command=lambda:start_train_thread(test_buttom))
    buttom.pack(side= tk.LEFT, padx= 20, pady=10)


    test_buttom= ttk.Button(scheme_var.w_bar, text="Start Testing",command=lambda:start_test_thread(test_buttom, label_buttom))
    test_buttom.pack(side= tk.LEFT, padx= 10, pady=10)
    test_buttom['state']= tk.DISABLED

    label_buttom= ttk.Button(scheme_var.w_bar, text="Predictive Label",command=lambda:PredictiveLabel(scheme_var.ypr, scheme_var.ypred ))
    label_buttom.pack(side= tk.LEFT, padx=10,pady=10)
    label_buttom['state']= tk.DISABLED

    scheme_var.w_bar.protocol("WM_DELETE_WINDOW", lambda: quit_train()) #interaction between app and window manaager

def start_test_thread(test_buttom, label_buttom):
    test_buttom['state']= tk.NORMAL
    acc,scheme_var.ypred, scheme_var.ypr = Test() 
    scheme_var.acc.set(f'Accuracy: {acc:.4f}')
    label_buttom['state']= tk.NORMAL


def start_train_thread(test_buttom):
    global train_thread

    scheme_var.stop_thread= False
    buttom['state'] = tk.DISABLED #disable buttom while training 
    train_thread= threading.Thread(target= Scheme, daemon= True) #aquire epoch from train scheme
    progressbar.start(interval= 400)
    train_thread.start()
    scheme_var.w_bar.after(400, check_train_thread)
    test_buttom['state']= tk.NORMAL

def check_train_thread():
    print(variable.update_epo)

    progressbar["value"]= variable.update_epo
    value_label["text"] = update_progress_label()

    if train_thread.is_alive() :
        scheme_var.w_bar.after(400, check_train_thread) # control update epoch speed
    else: 
        progressbar.stop()
        

def update_progress_label():
    label= progressbar["value"]
    return f"Epoch: {label}/ {scheme_var.epochs}"

def quit_train():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        scheme_var.stop_thread= True
        scheme_var.w_bar.destroy()
        

#display the predictive label and probability 
def PredictiveLabel( y_pr, y_pred):
    w= new_window('Predictive Label', '550x250')
    tk.Button(w, text="Save", command=lambda:save_y(y_pr, y_pred)).pack(fill='x')

    table= ttk.Treeview(w)
    #scroll bar 
    sb = Scrollbar(w, orient=tk.VERTICAL)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)

    table['column']= ['ID','Predictive Label']+[f'Class {i}'for i in range(scheme_var.n_class)]
    table.column('#0', width=0, stretch=tk.NO)
    table.column('ID', anchor=CENTER, width=30 )
    table.column('Predictive Label', anchor=CENTER, width=130)
    [table.column(f'Class {i}', anchor=tk.CENTER, width=80) for i in range(scheme_var.n_class)]

    table.heading('#0', text='', anchor=CENTER)
    table.heading('ID', text='ID', anchor=CENTER)
    table.heading('Predictive Label', text='Predictive Label', anchor=CENTER)
    [table.heading(f'Class {i}', text=f'Class {i}', anchor=tk.CENTER) for i in range(scheme_var.n_class)]

    for row in range(len(y_pred)):
        table.insert(parent='', index=row, iid= row, text='', values=[f'{row}', y_pred[row]]+[y_pr[row,i] for i in range(scheme_var.n_class)])
    table.pack()     

def save_y(y_pr, y_pred):
    folder= tk.filedialog.askdirectory()
    y_pred= y_pred.reshape(-1,1)
    print('Probability size:', y_pr.shape,'\nLabel size', y_pred.shape)
    np.savetxt(folder+'/data.csv', np.concatenate((y_pred, y_pr), axis=1), delimiter=',')


# Menu- Plot- spatial ==============================================    
# plot_spatial, mag_response in freq_response.py


#====================== others========================
def new_window(Title, size):
    newindow= tk.Toplevel()
    newindow.geometry(size)
    newindow.title(Title)
    newindow.configure(background='White')
    newindow.wm_attributes('-topmost', True)
    return newindow


def folder2entry(entry):
    global shortweightfolder
    folder= tk.filedialog.askdirectory()
    shortweightfolder= "/".join(folder.split('/')[-2:])
    entry.insert(tk.END, folder)
    scheme_var.weightfolder= folder    


