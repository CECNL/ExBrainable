# Authors: Ya-Lin Huang <yalinhuang.bt06@nycu.edu.tw>

import tkinter as tk
from tkinter.ttk import *
from mne import event
from torchsummary import summary

import threading
import numpy as np
import scipy.io
import io
import sys

from .visualization import *
from .dataloader import Individual_Dataset
from . import variable
from . import scheme_var
from .train_test import Test, Scheme


#====================== Main========================
#--------------------------Control Center----------------------------------
def main():

    global win_main #new
    win_main = tk.Tk()
    win_main.geometry('500x750')
    win_main.title("ExBrainable")
    win_main.configure(background='White')
    scheme_var.win_main= win_main

    # Panel
    global trainframe, modelframe, testframe

    trainframe = tk.LabelFrame(win_main, text="Training Data", height=10, bg='White', width=50, labelanchor='n')
    trainframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
    tk.Label(trainframe, text="Train Data (X_train) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(trainframe, text="Train Data size :　", bg= 'White').grid(row=1, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(trainframe, text="Train Label (Y_train) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(trainframe, text="Train Label size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)
   

    modelframe = tk.LabelFrame(win_main, text="Model and Training Setting", height=10, bg='White', width=50, labelanchor='n')
    modelframe.pack(fill='both', ipadx=1 ,ipady= 10,padx= 20,pady= 0)
    tk.Label(modelframe, text="Model :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Sampliing Rate :　", bg= 'White').grid(row=1, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Validation Split :　", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Batch Size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Epoch :　", bg= 'White').grid(row=4, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Learning Rate :　", bg= 'White').grid(row=5, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Save Model Weight:　", bg= 'White').grid(row=6, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Pretrained Model Weight:　", bg= 'White').grid(row=7, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Training Time (sec) :　", bg= 'White').grid(row=8, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Trainable Parameters :　", bg= 'White').grid(row=9, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="Memory Size (MB) :　", bg= 'White').grid(row=10, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(modelframe, text="EEG Montage :　", bg= 'White').grid(row=11, column=0, ipady=4, padx=20, sticky=tk.W)
    
    #default pretrained weight and path of saving weight as None
    global shortweightfolder, shortloadweightfile
    shortweightfolder= tk.StringVar()
    shortloadweightfile= tk.StringVar()
    Montagename= tk.StringVar()
    shortweightfolder.set('None')
    shortloadweightfile.set('None')
    Montagename.set('None')
    tk.Label(modelframe, textvariable= shortweightfolder, bg= 'White').grid(row=6, column=1,sticky=tk.W)
    tk.Label(modelframe, textvariable= shortloadweightfile, bg= 'White').grid(row=7, column=1,sticky=tk.W)
    tk.Label(modelframe, textvariable= Montagename, bg= 'White').grid(row=11, column=1,sticky=tk.W)


    
    testframe = tk.LabelFrame(win_main, text="Test Data", height=10, bg='White', width=50, labelanchor='n')
    testframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
    tk.Label(testframe, text="Test Data(X_test) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(testframe, text="Test Data Size :　", bg= 'White').grid(row=1 ,column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(testframe, text="Test Label(Y_test) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
    tk.Label(testframe, text="Test Label Size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)

 #--------------------------Contextual Menu----------------------------------   
    '''
    File 
        Load Data 
        Load Model Weight
    Model
        Model Selection
        Training Setting
        Model Training
        Model Summary 
    Results
        Model Prediction
        Model Performance
        Model Interpretation
            Spatial Pattern
            Temporal Pattern
    '''
    #create menu
    menubar = tk.Menu(win_main)
    global filemenu, Results, Model

    # Menu- File
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File ', menu=filemenu)
    filemenu.add_command(label='Load Data', command=lambda:Load_dataset())
    filemenu.add_command(label='Load Model Weight', command=lambda:Weightname())

    # Menu-Model
    Model = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Model', menu=Model)
    Model.add_command(label='Model Selection', command=lambda:load_model_struct())
    Model.add_command(label='Training Setting', command=lambda:Model_Preparation())
    Model.add_command(label='Model Training', command=(lambda:bar()))
    Model.add_command(label='Model Summary', command=(lambda:full_model_summary()))
    #Menu- Results 
    
    Results = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Results', menu= Results)
    Results.add_command(label='Model Prediction', command=lambda:PredictiveLabel())
    Plot = tk.Menu(Results, tearoff=0)
    Results.add_command(label='Model Performance', command=lambda:Model_performance())
    Results.add_cascade(label='Model Interpretation', menu= Plot)
    Plot.add_command(label='Spatial Pattern', command=lambda:montage_select(modelframe, Montagename))
    Plot.add_command(label='Temporal Pattern', command=lambda:plot_mag())

    #disable menu 只開放 load data 
    filemenu.entryconfig("Load Model Weight", state= 'disabled')
    Model.entryconfig("Model Selection", state="disabled")
    Model.entryconfig("Training Setting", state="disabled")
    Model.entryconfig("Model Training", state="disabled")
    Model.entryconfig("Model Summary", state="disabled")
    Results.entryconfig("Model Performance", state="disabled")
    Results.entryconfig("Model Prediction", state="disabled")
    Results.entryconfig("Model Interpretation", state="disabled")

    win_main.config(menu=menubar)
    win_main.mainloop()


# Menu- File- Load data=================================    
def Load_dataset():
    global w_load
    w_load=new_window(Title='Load Data', size='500x300', x_pad= -10, y_pad= 190)
    #topic
    tk.Label(w_load, text="Train Data :　", bg= 'White').grid(row=0, column=0,padx=20,ipady=4,  sticky=tk.W)
    tk.Label(w_load, text="Train Label :　", bg= 'White').grid(row=1, column=0,padx=20,ipady=4,  sticky=tk.W)
    tk.Label(w_load, text="Test Data :　", bg= 'White').grid(row=2, column=0,padx=20,ipady=4,  sticky=tk.W)
    tk.Label(w_load, text="Test Label :　", bg= 'White').grid(row=3, column=0,padx=20,ipady=4,  sticky=tk.W)

    tk.Label(w_load, text="Number of Classes :　", bg= 'White').grid(row=4,padx=20,ipady=4, sticky=tk.W)
    tk.Label(w_load, text="Number of Channel :　", bg= 'White').grid(row=5,padx=20, ipady=4, sticky=tk.W)
    tk.Label(w_load, text="Sampling Rate :　", bg= 'White').grid(row=6,padx=20, ipady=4, sticky=tk.W)
    tk.Label(w_load, text="Timepoint (only load model weight) :  ", bg= 'White').grid(row=7,padx=20, ipady=4, sticky=tk.W)
    
    

    #textinput
    x_train = tk.Entry(w_load)
    y_train = tk.Entry(w_load)
    x_test = tk.Entry(w_load)
    y_test = tk.Entry(w_load)
   
    #n_cuda = tk.Entry(w)
    n_class = tk.Entry(w_load)
    ch = tk.Entry(w_load)
    sf = tk.Entry(w_load)
    tp = tk.Entry(w_load)
    
    x_train.grid(row=0, column=1)
    y_train.grid(row=1, column=1)
    x_test.grid(row=2, column=1)
    y_test.grid(row=3, column=1)
    #n_cuda.grid(row=6, column=1)
    n_class.grid(row=4, column=1)
    ch.grid(row=5, column=1)
    sf.grid(row=6, column=1)
    tp.grid(row=7, column=1)
    

    
       #load train test path by bottom
    ttk.Button(w_load, text="File", command=(lambda:path2entry(w_load, x_train, 'x_train')), width=10).grid(row=0,column=2,padx=10)
    ttk.Button(w_load, text="File", command=(lambda:path2entry(w_load, y_train,'y_train')), width=10).grid(row=1,column=2,padx=10)
    ttk.Button(w_load, text="File", command=(lambda:path2entry(w_load, x_test,'x_test')), width=10).grid(row=2,column=2,padx=10)
    ttk.Button(w_load, text="File", command=(lambda:path2entry(w_load, y_test, 'y_test')), width=10).grid(row=3,column=2,padx=10)
    #ttk.Button(w, text="Select ", command=(lambda:montage_select(w)), width=10).grid(row=8,column=2)


    Confirm = ttk.Button(w_load ,text="Confirm", 
                         command=(lambda:show_input(w_load, n_class, sf, ch, tp)), width=10).grid(row=9, column=1, pady=5)



#####load xy dataset and check size#############
def path2entry(root, entry, set_type):
    path = tk.filedialog.askopenfilename(parent=w_load)
    entry.insert(tk.END, path)
    data= read_path(path, set_type)
    identify_path_type(path, set_type) #identify path 
    identify_set_type(data, set_type) #identify data 
    

def read_path(path, set_type):
    global ftype
    try: 
        if '.mat' in path:
            data_ = scipy.io.loadmat(path)
            if set_type not in data_.keys():
                raise ValueError (f'Dict key must be {set_type}.')
            data= data_[set_type]
            ftype= '.mat'

        if '.set' in path: 
            data = mne.io.read_epochs_eeglab(path, uint16_codec='latin1')
            #data =data._data
            ftype='.set'

        if '.edf' in path: 
            data= mne.io.read_raw_edf(path,preload= True)
            data =data._data
            ftype='.edf'

        return data     

    except TypeError:
        print('The file format is not supported.')

def identify_path_type(path, set_type):#辨別 xt, yt, xtest, ytest path
    
    global X_trainpath, Y_trainpath, X_testpath, Y_testpath

    path= "/".join(path.split('/')[-3:])
    if set_type=='x_train':
        X_trainpath= path
    elif set_type=='y_train':
        Y_trainpath= path
    elif set_type=='x_test':
        X_testpath= path 
    elif set_type=='y_test':
        Y_testpath= path
         
def identify_set_type(data, set_type):#辨別 xt, yt, xtest, ytest data
    
    global X_train, Y_train, X_test, Y_test

    if set_type=='x_train':
        X_train= data
        scheme_var.x_train= X_train
    elif set_type=='y_train':
        Y_train= data
        scheme_var.y_train= Y_train
    elif set_type=='x_test':
        X_test= data 
        scheme_var.x_test= X_test
    elif set_type=='y_test':
        Y_test= data
        scheme_var.y_test= Y_test
'''
situation    0  1  2  
xtrain       v  v  v
ytrain       v  v  v
xtest           v  v
ytest              v
'''

def confirm_xy_size(): #numpy array (n_trials, n_chs, n_times) (n_trials,1)
    if ('X_train' and 'Y_train' in globals()):
        if (X_train.shape[0]==Y_train.shape[0]): #xy train same tiral 
            if 'X_test' in globals()  :  
                if not (X_train.shape[1]== X_test.shape[1]) and  (X_train.shape[2]== X_test.shape[2]): #xtrain xtest same channel timepoint
                    tk.messagebox.showerror("Error",'Shape of x_train and x_test have to be the same length.', parent=w_load ) #showerror, showinfo, showwarning 
                    raise ValueError ('Shape of x_train and x_test have to be the same length.')
                    

                # yes x_test & yes y_test 
                if 'Y_test' in globals(): 
                    scheme_var.situation=2
                    if not (X_test.shape[0]== Y_test.shape[0]) : # X_test, ytest trial 一樣 
                        tk.messagebox.showerror("Error",'Shape of x_test and y_test have to be the same length.', parent=w_load)
                        raise ValueError ('Shape of x_test and y_test have to be the same length.')
                        
                else:#yes x_test , no y_test 
                    scheme_var.situation=1
            elif 'Y_test' in globals():#no x_test , yes y_test 
                tk.messagebox.showerror("Error",'You must also load Y_train Data.', parent=w_load)
            else: # no x_test, no_ytest  
                scheme_var.situation=0    
                
        else: 
            tk.messagebox.showerror("Error",'Trials of x_train and y_train have to be the same length.', parent=w_load)
            raise ValueError ('Trials of x_train and y_train have to be the same length.')
            
    else: 
        tk.messagebox.showerror("Error",'You must load files of Train Data and Train Label.')
        raise TypeError( 'You must load files of Train Data and Train Label.')
    
    print('situation: ', scheme_var.situation)
          
###################################################
    

def show_input(w, n_class, sf ,ch, tp):

    scheme_var.n_class= int(n_class.get())
    scheme_var.ch= int(ch.get())
    scheme_var.sf= int(sf.get())

    if ('X_train' or 'Y_train' or 'X_test' or 'Y_test') in globals(): #沒有load data，只輸入data properties，然後load model weight  
        confirm_xy_size()
        if ('X_train' and 'Y_train' in globals()): 
            tk.Label(trainframe, text= X_trainpath, bg= 'White').grid(row=0, column=1,  sticky=tk.W )
            tk.Label(trainframe, text= X_train.shape, bg= 'White').grid(row=1, column=1,  sticky=tk.W )
            tk.Label(trainframe, text= Y_trainpath, bg= 'White').grid(row=2, column=1,  sticky=tk.W )                                                                                                                       
            tk.Label(trainframe, text= Y_train.shape, bg= 'White').grid(row=3, column=1,  sticky=tk.W ) 
            scheme_var.tp= X_train.shape[2]
            print('x_train size: ',X_train.shape,
            '\ny_train size: ', Y_train.shape)

        if 'X_test' in globals():
            tk.Label(testframe, text= X_testpath, bg= 'White').grid(row=0, column=1,  sticky=tk.W )
            tk.Label(testframe, text= X_test.shape, bg= 'White').grid(row=1, column=1,  sticky=tk.W)
            print('x_test size: ', X_test.shape)

        if 'Y_test' in globals():
            tk.Label(testframe, text= Y_testpath, bg= 'White').grid(row=2, column=1,  sticky=tk.W )
            tk.Label(testframe, text= Y_test.shape, bg= 'White').grid(row=3, column=1,  sticky=tk.W)
            print('y_test size: ', Y_test.shape)

    else:
        scheme_var.tp= int(tp.get())

    w.destroy()
    tk.Label(modelframe, text= scheme_var.sf, bg= 'White').grid(row=1, column=1,  sticky=tk.W)
    Model.entryconfig("Model Selection", state="normal")

# Menu- File- Load weight====================================


def Weightname():
    global conv1, conv2

    file= tk.filedialog.askopenfilename()
    shortpath= "/".join(file.split('/')[-2:])
    shortloadweightfile.set(shortpath)
    tk.Label(modelframe, textvariable= shortloadweightfile, bg= 'White').grid(row=7, column=1)
    conv1,conv2= get_weight(filepath=file)
    scheme_var.loadweightfile= file
    Results.entryconfig("Model Interpretation", state="normal")
    
#print(f'conv1: {conv1.shape}')
#conv1size = tk.Label(window, text= f'conv1: {conv1.shape}').grid(row=9, column=1)

#conv2size = tk.Label(window, text= f'conv2: {conv2.shape}').grid(row=10, column=1)

# Menu- Model- Model Selection=================================    
def load_model_struct(): 
    win_lms=new_window(Title='Load model structure', size='500x200', x_pad=-10, y_pad=220)
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
    import os
    file_path = os.path.dirname(os.path.realpath(__file__))
    exec(open(os.path.join(file_path + '/models.py'),encoding="utf-8").read(), globals()) #put all variable to globals()
    name = modelist.get()
    print(name)
    scheme_var.netname= eval(str(name+'()'))
    tk.Label(modelframe, text=name, bg= 'White').grid(row=0, column=1,  sticky=tk.W ) 

    filemenu.entryconfig("Load Model Weight", state= 'normal')
    Model.entryconfig("Training Setting", state="normal")
    
    win_lms.destroy()

# File- study

def read_data_path(frame, set_type):
    global concat_data, event_ids, subname, sublen
    # identify pathtypes: multiple sub files are named as 'files_x_train','files_y_train'...
    files = tk.filedialog.askopenfilenames()
    fnum=1
    event_ids=[]
    subname=[]
    sublen=[]

    for path in files:
        # name each path: 'x_trainpath_1','x_trainpath_2'
        globals()[str(set_type)+'path_'+str(fnum)]= path

        # read and each file:'xtrain_1', 'xtrain_2' 
        globals()[str(set_type)+'_'+str(fnum)]= read_path(path, set_type)

        #concat diff files labels #need revise  
        data= globals()[str(set_type)+'_'+str(fnum)]
        fnum+=1
        

        if '.mat' in path and 'y' in set_type:
            if 'concat_data' not in globals():
                concat_data= data.reshape(-1)
            else:
                concat_data= np.concatenate((concat_data, data.reshape(-1)))
            
            # find eventids from labels
            for i in data.reshape(-1):
                if i not in event_ids:
                    event_ids.append(i)
            event_ids.sort(reverse=False)

            print(concat_data.shape)
            
        # display each file name
        fname= path.split('/')[-1]
        tk.Label(frame, text= fname, bg='White').pack(fill='both',padx=20)
        subname.append( fname.split('.')[0])
        sublen.append( len(data))

    print(event_ids, subname, sublen)
    
def findevents(x):
    return {
        #'.set': data.event_id,
        '.mat': event_ids,
    }[x]

def rename_events(w_files):

    w_files.destroy()
    w= new_window('Rename Events', '500x250', x_pad=-10, y_pad=180)
    global table

    # t_frame = tk.Frame(w, bg="White", bd=1, relief="sunken", width=450, height=50)
    # t_frame.pack(side='top', fill='both',pady=30, ipady=20,ipadx=4)
    print('len of eventtype', len(findevents(ftype)))
    event_ids= findevents(ftype)

    table= ttk.Treeview(w, height=len(event_ids))
    
    #create scroll bar 
    sb = Scrollbar(w, orient=tk.VERTICAL)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)

    table['column']= ['Event ID','Event type']
    table.column('#0', width=0, stretch=tk.NO)
    table.column('Event ID', anchor=tk.CENTER, width=30 )
    table.column('Event type', anchor=tk.CENTER, width=130)
    #table.column('Count', anchor=tk.CENTER, width=80)

    table.heading('#0', text='', anchor=tk.CENTER)
    table.heading('Event ID', text='Event ID', anchor=tk.CENTER)
    table.heading('Event type', text='Event type', anchor=tk.CENTER)

    if ftype== '.set': 
        for row in range(len(event_ids)):
            eventypes=list(event_ids.keys())
            item= table.insert(parent='', index=row, iid= row, text='', values=[event_ids[eventypes[row]], eventypes[row] ])
            table.item(item, tags=item)
    if ftype== '.mat':
        global eventype
        eventype= [None]*len(event_ids) # eventype is none default in mat file 
        for row in range(len(event_ids)):
            item= table.insert(parent='', index=row, iid= row, text='', values=[event_ids[row], eventype[row] ])
            table.item(item, tags=item)

    table.bind('<1>', editname)
    table.pack(side='top', fill='x',padx=10, pady=10)

    Confirm = ttk.Button(w ,text="Confirm", command=(lambda:all_data(w)), width=10).pack()
    # plot events
    # figure = Figure(figsize=(5,5))
    # ax = figure.add_subplot(1, 1, 1)
    # mne.viz.plot_events(data.events, event_id=data.event_id, sfreq=562, axes=ax)
    # canvas = FigureCanvasTkAgg(figure, w)
    # canvas.get_tk_widget().pack(side='bottom')

def editname(event):

    if table.identify_region(event.x, event.y) == 'cell':
        # the user clicked on a cell

        def ok(event):
            """Change item value."""
            #print(entry.get(), type(entry.get()))
            if column=='#1':
                event_ids[int(item)]= int(entry.get())
            if column=='#2':
                eventype[int(item)]= entry.get()
            print(event_ids, eventype)

            table.set(item, column, entry.get())
            entry.destroy()
        
        column = table.identify_column(event.x)  # identify column
        item = table.identify_row(event.y)  # identify item
        x, y, width, height = table.bbox(item, column) 
        value = table.set(item, column)

     
        

    elif table.identify_region(event.x, event.y) == 'heading': 
        # the user clicked on a heading

        def ok(event):
            """Change heading text."""
            table.heading(column, text=entry.get())
            entry.destroy()

        column = table.identify_column(event.x) # identify column
        # tree.bbox work sonly with items so we have to get the bbox of the heading differently
        x, y, width, _ = table.bbox(table.get_children('')[0], column) # get x and width (same as the one of any cell in the column)
        # get vertical coordinates (y1, y2)
        y2 = y
        # get bottom coordinate
        while table.identify_region(event.x, y2) != 'heading':  
            y2 -= 1
        # get top coordinate
        y1 = y2
        while table.identify_region(event.x, y1) == 'heading':
            y1 -= 1
        height = y2 - y1
        y = y1
        value = table.heading(column, 'text')

    elif table.identify_region(event.x, event.y) == 'nothing': 
        column = table.identify_column(event.x) # identify column
        # check whether we are below the last row:
        x, y, width, height =table.bbox(table.get_children('')[-1], column)
        if event.y > y:

            def ok(event):
                """Change item value."""
                # create item
                item = table.insert("", "end", values=("", ""))
                table.set(item, column, entry.get())
                entry.destroy()

            y += height
            value = ""
        else:
            return
    else:
        return
    # display the Entry   
    entry = ttk.Entry(table)  # create edition entry
    entry.place(x=x, y=y, width=width, height=height,
                anchor='nw')  # display entry on top of cell
    entry.insert(0, value)  # put former value in entry
    entry.bind('<FocusOut>', lambda e: entry.destroy())  
    entry.bind('<Return>', ok)  # validate with Enter
    entry.focus_set()

def all_data(w):
    w.destroy()
    w_data= new_window('Events ', '900x500', x_pad=-10, y_pad=100)

    frame_allevents= tk.LabelFrame(w_data,text="All Events",bg="White", labelanchor='n')
    frame_train= tk.LabelFrame(w_data, text="Training set",bg="White", labelanchor='n')
    frame_test= tk.LabelFrame(w_data, text="Testing set",bg="White", labelanchor='n')

    frame_allevents.grid(row=0, column=0)
    frame_train.grid(row=0, column=1)
    frame_test.grid(row=0, column=2)

    
    # .mat 
    tabletype=['allevents', 'train', 'test']
    tables= {}
    for t in tabletype:
        tables[t]= ttk.Treeview(locals()['frame_'+ t], height=20)
        # globals()['table_'+ t]= ttk.Treeview(locals()['frame_'+ t], height=20)
        # globals()['table_'+ t].grid()
        #print(len(concat_data))
        
        #create scroll bar
        sb = Scrollbar(locals()['frame_'+ t], orient=tk.VERTICAL)
        sb.grid(row=0,column=1,sticky='ns')
        tables[t].config(yscrollcommand=sb.set)
        sb.config(command=tables[t].yview)
        
        #create columns
        tables[t]['column']= ['Subject','Event ID','Event type','Onset time']
        columns= tables[t]['column']

        tables[t].column('#0', width=0, stretch=tk.NO)
        tables[t].heading('#0', text='', anchor=tk.CENTER)
        for col in columns:
            tables[t].column(col, anchor=tk.CENTER, width=70 )
            tables[t].heading(col, text='', anchor=tk.CENTER)

        tables[t].grid(row=0, sticky= tk.N)
        # table.column('Subject', anchor=tk.CENTER, width=30 )
        # table.column('Event ID', anchor=tk.CENTER, width=30 )
        # table.column('Event type', anchor=tk.CENTER, width=30)
        # table.column('Onset time', anchor=tk.CENTER, width=50)

        # table.heading('#0', text='', anchor=tk.CENTER)
        # table.heading('Subject', text='Subject', anchor=tk.CENTER)
        # table.heading('Event ID', text='Event ID', anchor=tk.CENTER)
        # table.heading('Event type', text='Event type', anchor=tk.CENTER)
        # table.heading('Onset time', text='Onset time', anchor=tk.CENTER)

        if t=='allevents':
            i=0
            for row in range(len(concat_data)):
                if row < sublen[i]:
                    tables[t].insert(parent='', index=row, iid= row, text='', values=[subname[i], concat_data[row], eventype[concat_data[row]] , 'None'])
                else:
                    i+=1
                    sublen[i]+= sublen[i-1]    

            for col in columns:
                tables[t].heading(col, text= col, command= lambda c=col: sort_id(tables[t], c, False))
            i=0

        elif t== 'train':
            for row in range(5):
                tables[t].insert(parent='', index=row, iid= row, text='', values=['ha', 'he', 'he' , 'ge'])
            for col in columns:
                tables[t].heading(col, text= col, command= lambda c=col: sort_id(tables[t], c, False))
        
        elif t== 'test':
            for row in range(5):
                tables[t].insert(parent='', index=row, iid= row, text='', values=['ha', 'he', 'he' , 'ge'])
            for col in columns:
                tables[t].heading(col, text= col, command= lambda c=col: sort_id(tables[t], c, False))
    #ttk.Button(frame_allevents ,text="Move to training set", command=(Moveto(tables))).grid(row=1, column=0)
    #ttk.Button(frame_allevents ,text="Move to test set", command=(Moveto(tables))).grid(row=1, column=1)
    

def Moveto(tables):
    data= tk.Variable()
    print([table['allevents'].item(idx) for idx in tables['allevents'].selection()])
    #data.set([table['allevents'].item(idx) for idx in tables['allevents'].selection()])
    


def sort_id(table, col, reverse):
    l = [(table.set(k, col), k) for k in table.get_children('')]
    #print(l) #[(eventid,rowindex), ... ]
    l.sort(key=lambda t: int(t[0]), reverse=reverse)
    #print(l) #sort by eventid 

    for index, (val, k) in enumerate(l): # save sorted changes to table 
        table.move(item= k, parent= '', index= index) # move k to index position
        table.heading(col,command=lambda: sort_id(table, col, False))

# Menu- Model- Training setting =================================    

def Model_Preparation():
    win_p=new_window(Title='Training Setting ', size='500x200', x_pad=-10, y_pad=180)
    #topic
    tk.Label(win_p, text="Validation split :　", bg= 'White').grid(row=0,padx=20,ipady=4,  sticky=tk.W)
    tk.Label(win_p, text="Batch Size :　", bg= 'White').grid(row=1,padx=20,ipady=4,  sticky=tk.W)
    tk.Label(win_p, text="Epoch :　", bg= 'White').grid(row=2, column=0, padx=20,ipady=4,  sticky=tk.W)
    tk.Label(win_p, text="Learning Rate :　", bg= 'White').grid(row=3, column=0, padx=20,ipady=4,  sticky=tk.W)
    tk.Label(win_p, text="Save Weight to : 　", bg= 'White').grid(row=4,column=0, padx=20,ipady=4,  sticky=tk.W)
    
    Valratio = tk.Entry(win_p)
    Batchsize = tk.Entry(win_p)
    Epoch = tk.Entry(win_p)
    Lr = tk.Entry(win_p)
    Save_weight = tk.Entry(win_p)


    Valratio.grid(row=0, column=1)
    Batchsize.grid(row=1, column=1)
    Epoch.grid(row=2, column=1)
    Lr.grid(row=3, column=1)
    Save_weight.grid(row=4, column=1)

    weightfolder= ttk.Button(win_p, text="Folder", command=(lambda:save_weight_folder(win_p, Save_weight)), width=10).grid(row=4,column=2)

    Confirm = ttk.Button(win_p ,text="Confirm", command=(lambda:show_para(win_p,Valratio, Batchsize, Epoch, Lr)), width=10).grid(row=6, column=1)

def save_weight_folder(win_p, entry):
    global shortfolder
    folder= tk.filedialog.askdirectory(parent=win_p)
    shortfolder= "/".join(folder.split('/')[-3:])
    entry.insert(tk.END, folder)
    scheme_var.saveweightfolder= folder    

def show_para(win_p, Valratio, Batchsize, Epoch, Lr ):

    scheme_var.val_ratio= float(Valratio.get())
    scheme_var.bs= int(Batchsize.get())
    scheme_var.epochs= int(Epoch.get())
    scheme_var.lr= float(Lr.get())
    shortweightfolder.set(shortfolder)
    #close w
    win_p.destroy()

    #para in control display 
    tk.Label(modelframe, text= scheme_var.val_ratio, bg= 'White').grid(row=2, column=1,  sticky=tk.W )
    tk.Label(modelframe, text= scheme_var.bs, bg= 'White').grid(row=3, column=1,  sticky=tk.W )
    tk.Label(modelframe, text= scheme_var.epochs, bg= 'White').grid(row=4, column=1 ,  sticky=tk.W)
    tk.Label(modelframe, text= scheme_var.lr, bg= 'White').grid(row=5, column=1,  sticky=tk.W)
    tk.Label(modelframe, textvariable= shortweightfolder , bg= 'White').grid(row=6, column=1,  sticky=tk.W)
    
    model_summary()
    Model.entryconfig("Model Training", state="normal")

def model_summary():
    global output 
    net= scheme_var.netname
    dev = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    summary(net.to(dev), (1,scheme_var.ch, scheme_var.tp), batch_size=scheme_var.bs)
    output = new_stdout.getvalue()
    sys.stdout = old_stdout


    rows= output.split('\n')
    for row in rows:
        if 'Trainable params' in row:
            row= row.replace(',','').split(':')
            trainable_para= int(row[1])
        if 'Estimated Total Size' in row:
            row= row.split(':')
            memory_size= float(row[1].strip())

    tk.Label(modelframe, text=trainable_para, bg= 'White').grid(row=9, column=1, sticky=tk.W)
    tk.Label(modelframe, text=memory_size, bg= 'White').grid(row=10, column=1, sticky=tk.W)
    Model.entryconfig("Model Summary", state="normal")

def full_model_summary():
    w= new_window('Model Summary', size= '500x500', x_pad=-10, y_pad=180)
    soutput= output.replace('=','').replace('-', '')
    tk.Label(w, text= soutput, bg= 'White').grid()
    #rows= output.split('\n')
    # srows= [row.replace('=','').replace('-', '')+ '\n' for row in rows]
    # i=0
    # for row in soutput: 
    #     tk.Label(w, text= row, bg= 'White').grid(row=i, column=0, sticky=tk.W)
    #     i+=1
# Menu- Model- Start training =================================

def bar(): #w_bar, ypred, ypr remove from scheme_var? 
    global progressbar, value_label, buttom 
    scheme_var.w_bar = new_window(Title='Model Training', size='500x150', x_pad=-10, y_pad=180)

    progressbar = Progressbar(scheme_var.w_bar, mode='determinate',length= 500, maximum= scheme_var.epochs)
    progressbar.pack(anchor= tk.CENTER)

    value_label = tk.Label(scheme_var.w_bar, text= update_progress_label())
    value_label.pack(anchor= tk.CENTER)

    buttom= ttk.Button(scheme_var.w_bar, text="Start Training",command=lambda:start_train_thread())
    buttom.pack(side= tk.BOTTOM, padx= 20, pady=10)

    #Dataloader 
    if (scheme_var.situation==1 or scheme_var.situation ==2) :
        scheme_var.trainloader, scheme_var.valloader, scheme_var.testloader=Individual_Dataset()
    else: #situation==0
        scheme_var.trainloader, scheme_var.valloader= Individual_Dataset()
 
    scheme_var.w_bar.protocol("WM_DELETE_WINDOW", lambda: quit_train()) #interaction between app and window manaager



def start_train_thread():
    global train_thread

    scheme_var.stop_thread= False
    buttom['state'] = tk.DISABLED #disable buttom while training 
    train_thread= threading.Thread(target= Scheme, daemon= True) #aquire epoch from train scheme
    progressbar.start(interval= 400)
    train_thread.start()
    scheme_var.w_bar.after(400, check_train_thread)
    control_menu_activity()
    

def check_train_thread():
    print(variable.update_epo)

    progressbar["value"]= variable.update_epo
    value_label["text"] = update_progress_label()

    if train_thread.is_alive() :
        scheme_var.w_bar.after(400, check_train_thread) # control update epoch speed
    else: 
        progressbar.stop()

        global conv1, conv2
        print(scheme_var.saveweightfolder)
        conv1,conv2= get_weight(filepath=f'{scheme_var.saveweightfolder}/temp.pth')
        shortloadweightfile.set(f'{shortfolder}/temp.pth')
        tk.Label(modelframe, textvariable= shortloadweightfile, bg= 'White').grid(row=7, column=1, sticky=tk.W) 
        tk.Label(modelframe, text= f'{scheme_var.training_time:.2f}' , bg= 'White').grid(row=8, column=1, sticky=tk.W) 

def update_progress_label():
    label= progressbar["value"]
    return f"Epoch: {label}/ {scheme_var.epochs}"

def quit_train():
    if tk.messagebox.askokcancel('Quit', 'Do you want to quit?', parent=scheme_var.w_bar):
        scheme_var.stop_thread= True
        scheme_var.w_bar.destroy()

def control_menu_activity():
    if scheme_var.situation==0: #only xtrain ytrain 
        Results.entryconfig("Model Interpretation", state="normal")
    if (scheme_var.situation==1 or scheme_var.situation==2): 
        Results.entryconfig("Model Prediction", state="normal")
        Results.entryconfig("Model Interpretation", state="normal")

# Menu- Results- Model Prediction ==============================================   

def PredictiveLabel():
    
    w= new_window('Model Prediction', '500x250', x_pad=-10, y_pad=180)

    #Model testing 
    global y_pred, y_pr
    if scheme_var.situation==1:
        y_pred, y_pr = Test()
    if scheme_var.situation==2:
        scheme_var.acc, scheme_var.kappa, y_pred, y_pr = Test() 
        Results.entryconfig("Model Performance", state="normal")

    #save buttom
    

    #create table 
    table= ttk.Treeview(w)
    #create scroll bar 
    sb = Scrollbar(w, orient=tk.VERTICAL)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)

    table['column']= ['ID','Predictive Label']+[f'Class {i}'for i in range(scheme_var.n_class)]
    table.column('#0', width=0, stretch=tk.NO)
    table.column('ID', anchor=tk.CENTER, width=30 )
    table.column('Predictive Label', anchor=tk.CENTER, width=130)
    [table.column(f'Class {i}', anchor=tk.CENTER, width=80) for i in range(scheme_var.n_class)]

    table.heading('#0', text='', anchor=tk.CENTER)
    table.heading('ID', text='ID', anchor=tk.CENTER)
    table.heading('Predictive Label', text='Predictive Label', anchor=tk.CENTER)
    [table.heading(f'Class {i}', text=f'Class {i}', anchor=tk.CENTER) for i in range(scheme_var.n_class)]

    for row in range(len(y_pred)):
        table.insert(parent='', index=row, iid= row, text='', values=[f'{row}', y_pred[row]]+[y_pr[row,i] for i in range(scheme_var.n_class)])
    table.pack()

    tk.Button(w, text="Save",borderwidth=2, relief='solid',bg='White', command=lambda:save_y(y_pr, y_pred)).pack(fill='x')     

def save_y(y_pr, y_pred):
    folder= tk.filedialog.askdirectory()
    y_pred= y_pred.reshape(-1,1)
    print('Probability size:', y_pr.shape,'\nLabel size', y_pred.shape)
    np.savetxt(folder+'/data.csv', np.concatenate((y_pred, y_pr), axis=1), delimiter=',')


# Menu- Results- Model Interpretation - spatial/temporal pattern ==============================================    
# plot_spatial, powerspectum in visualization.py

# Menu- Results- Model Performance ==============================================    
def Model_performance():
    w= new_window('Model Performance', '700x500', x_pad=-10, y_pad=180)
 
    Results.entryconfig("Model Prediction", state="normal")

    #acc kappa cm
    Confusion_Matrix(w, Y_test, y_pred)  # in visualization.py 

    ak_frame = tk.Frame(w, bg="White", bd=1, relief="sunken")
    ak_frame.pack(side='left', fill='both',pady=50, ipady=20,ipadx=4)
    table= Treeview(ak_frame)
    table['column']= ['Accuracy','Kappa']
    table.column('#0', width=0, stretch=tk.NO)
    table.column('Accuracy', anchor=tk.CENTER, width=80 )
    table.column('Kappa', anchor=tk.CENTER, width=80)
    table.heading('#0', text='', anchor=tk.CENTER)
    table.heading('Accuracy', text='Accuracy', anchor=tk.CENTER)
    table.heading('Kappa', text='Kappa', anchor=tk.CENTER)
    table.insert(parent='', index=0, iid= 0 , text='', values=[f'{scheme_var.acc:.3f}', f'{scheme_var.kappa:.3f}'])
    table.pack()  

#====================== others========================
def new_window(Title, size, x_pad, y_pad):

    win_main_x = win_main.winfo_rootx()+ x_pad
    win_main_y = win_main.winfo_rooty()+ y_pad

    newindow= tk.Toplevel()
    # newindow.wm_attributes('-topmost', True )
    newindow.geometry(size)
    newindow.geometry(f'+{win_main_x}+{win_main_y}')  
    newindow.title(Title)
    newindow.configure(background='White')
    
    
    return newindow


if __name__ == '__main__':
    main() 

