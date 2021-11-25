# Authors: Ya-Lin Huang <yalinhuang.bt06@nycu.edu.tw>

import tkinter as tk
from tkinter.constants import FALSE
from tkinter.ttk import *
from mne import event
from torchsummary import summary

import threading
import numpy as np
import scipy.io
import io
import sys

from visualization import *
from dataloader import *
from train_test import *
import variable
from scheme_var import *


'''
situation    0  1  2  
xtrain       v  v  v
ytrain       v  v  v
xtest           v  v
ytest              v
'''


#====================== Main========================
#--------------------------Control Center----------------------------------

class ExBrainable():
    def __init__(self):
        #super(ExBrainable, self).__init__()

        self.sch_var = SchemeVariable()

        self.win_main = tk.Tk()
        self.win_main.geometry('500x750')
        self.win_main.title("ExBrainable")
        self.win_main.configure(background='White')
        self.sch_var.win_main= self.win_main
        
        self.trainframe = tk.LabelFrame(self.win_main, text="Training Data", height=10, bg='White', width=50, labelanchor='n')
        self.modelframe = tk.LabelFrame(self.win_main, text="Model and Training Setting", height=10, bg='White', width=50, labelanchor='n')
        self.testframe = tk.LabelFrame(self.win_main, text="Test Data", height=10, bg='White', width=50, labelanchor='n')

        self.shortweightfolder= tk.StringVar()
        self.shortloadweightfile= tk.StringVar()
        self.Montagename= tk.StringVar()

        # create menu
        self.menubar = tk.Menu(self.win_main)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.Model = tk.Menu(self.menubar, tearoff=0)
        self.Results = tk.Menu(self.menubar, tearoff=0)

        self.w_load = None

        self.X_trainpath = ""
        self.Y_trainpath = ""
        self.X_testpath = ""
        self.Y_testpath = ""

        self.X_train = []
        self.Y_train = []
        self.X_test = []
        self.Y_test = []

        self.conv1 = []
        self.conv2 = []

        self.concat_data = None
        self.event_ids = None
        self.subname = None
        self.sublen = None

        self.table = None

        self.shortfolder = ""

        self.output = ""

        self.train_thread = None

        self.y_pred = []
        self.y_pr = []

        self.progressbar = None
        self.value_label = None
        self.buttom = None


    def Main(self):
        self.trainframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        tk.Label(self.trainframe, text="Train Data (X_train) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.trainframe, text="Train Data size :　", bg= 'White').grid(row=1, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.trainframe, text="Train Label (Y_train) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.trainframe, text="Train Label size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)
        
        self.modelframe.pack(fill='both', ipadx=1 ,ipady= 10,padx= 20,pady= 0)
        tk.Label(self.modelframe, text="Model :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Sampliing Rate :　", bg= 'White').grid(row=1, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Validation Split :　", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Batch Size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Epoch :　", bg= 'White').grid(row=4, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Learning Rate :　", bg= 'White').grid(row=5, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Save Model Weight:　", bg= 'White').grid(row=6, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Pretrained Model Weight:　", bg= 'White').grid(row=7, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Training Time (sec) :　", bg= 'White').grid(row=8, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Trainable Parameters :　", bg= 'White').grid(row=9, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="Memory Size (MB) :　", bg= 'White').grid(row=10, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.modelframe, text="EEG Montage :　", bg= 'White').grid(row=11, column=0, ipady=4, padx=20, sticky=tk.W)
        
        #default pretrained weight and path of saving weight as None
        self.shortweightfolder.set('None')
        self.shortloadweightfile.set('None')
        self.Montagename.set('None')
        tk.Label(self.modelframe, textvariable= self.shortweightfolder, bg= 'White').grid(row=6, column=1,sticky=tk.W)
        tk.Label(self.modelframe, textvariable= self.shortloadweightfile, bg= 'White').grid(row=7, column=1,sticky=tk.W)
        tk.Label(self.modelframe, textvariable= self.Montagename, bg= 'White').grid(row=11, column=1,sticky=tk.W)

        self.testframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        tk.Label(self.testframe, text="Test Data(X_test) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.testframe, text="Test Data Size :　", bg= 'White').grid(row=1 ,column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.testframe, text="Test Label(Y_test) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.testframe, text="Test Label Size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)

        self.Menu()

        
    def Menu(self):
        # Menu- File
        self.menubar.add_cascade(label='File ', menu=self.filemenu)
        self.filemenu.add_command(label='Load Data', command=lambda:self.Load_dataset())
        self.filemenu.add_command(label='Load Model Weight', command=lambda:Weightname)
        self.filemenu.add_command(label='Study(cross subject)', command=lambda:self.load_files())

        # Menu-Model
        self.menubar.add_cascade(label='Model', menu=self.Model)
        self.Model.add_command(label='Model Selection', command=lambda:self.load_model_struct())
        self.Model.add_command(label='Training Setting', command=lambda:self.Model_Preparation())
        self.Model.add_command(label='Model Training', command=(lambda:self.bar()))
        self.Model.add_command(label='Model Summary', command=(lambda:self.full_model_summary()))
            
        # Menu- Results
        visual_class = Visualization(self.sch_var)

        self.menubar.add_cascade(label='Results', menu=self.Results)
        self.Results.add_command(label='Model Prediction', command=lambda:self.PredictiveLabel())
        Plot = tk.Menu(self.Results, tearoff=0)
        self.Results.add_command(label='Model Performance', command=lambda:Model_performance())
        self.Results.add_cascade(label='Model Interpretation', menu= Plot)
        Plot.add_command(label='Spatial Pattern', command=lambda:visual_class.montage_select(self.modelframe, self.Montagename))
        Plot.add_command(label='Temporal Pattern', command=lambda:visual_class.plot_mag())

        # disable menu only allows load data 
        self.filemenu.entryconfig("Load Model Weight", state= 'disabled')
        self.Model.entryconfig("Model Selection", state="disabled")
        self.Model.entryconfig("Training Setting", state="disabled")
        self.Model.entryconfig("Model Training", state="disabled")
        self.Model.entryconfig("Model Summary", state="disabled")
        self.Results.entryconfig("Model Performance", state="disabled")
        self.Results.entryconfig("Model Prediction", state="disabled")
        self.Results.entryconfig("Model Interpretation", state="disabled")

        self.win_main.config(menu=self.menubar)
        self.win_main.mainloop()


    def new_window(self, Title, size, x_pad, y_pad):
        win_main_x = self.win_main.winfo_rootx()+ x_pad
        win_main_y = self.win_main.winfo_rooty()+ y_pad

        newindow= tk.Toplevel()
        newindow.wm_attributes('-topmost', True )
        newindow.geometry(size)
        newindow.geometry(f'+{win_main_x}+{win_main_y}')  
        newindow.title(Title)
        newindow.configure(background='White')
    
        return newindow


    def Load_dataset(self):
        self.w_load = self.new_window(Title='Load Data', size='500x300', x_pad= -10, y_pad= 190)

        tk.Label(self.w_load, text="Train Data :　", bg= 'White').grid(row=0, column=0,padx=20,ipady=4,  sticky=tk.W)
        tk.Label(self.w_load, text="Train Label :　", bg= 'White').grid(row=1, column=0,padx=20,ipady=4,  sticky=tk.W)
        tk.Label(self.w_load, text="Test Data :　", bg= 'White').grid(row=2, column=0,padx=20,ipady=4,  sticky=tk.W)
        tk.Label(self.w_load, text="Test Label :　", bg= 'White').grid(row=3, column=0,padx=20,ipady=4,  sticky=tk.W)

        tk.Label(self.w_load, text="Number of Classes :　", bg= 'White').grid(row=4,padx=20,ipady=4, sticky=tk.W)
        tk.Label(self.w_load, text="Number of Channel :　", bg= 'White').grid(row=5,padx=20, ipady=4, sticky=tk.W)
        tk.Label(self.w_load, text="Sampling Rate :　", bg= 'White').grid(row=6,padx=20, ipady=4, sticky=tk.W)
        tk.Label(self.w_load, text="Timepoint (only load model weight) :  ", bg= 'White').grid(row=7,padx=20, ipady=4, sticky=tk.W)
    
        # textinput
        x_train = tk.Entry(self.w_load)
        y_train = tk.Entry(self.w_load)
        x_test = tk.Entry(self.w_load)
        y_test = tk.Entry(self.w_load)
   
        # n_cuda = tk.Entry(w)
        n_class = tk.Entry(self.w_load)
        ch = tk.Entry(self.w_load)
        sf = tk.Entry(self.w_load)
        tp = tk.Entry(self.w_load)
    
        x_train.grid(row=0, column=1)
        y_train.grid(row=1, column=1)
        x_test.grid(row=2, column=1)
        y_test.grid(row=3, column=1)
        # n_cuda.grid(row=6, column=1)
        n_class.grid(row=4, column=1)
        ch.grid(row=5, column=1)
        sf.grid(row=6, column=1)
        tp.grid(row=7, column=1)
    
        # load train test path by bottom
        ttk.Button(self.w_load, text="File", command=(lambda:self.path2entry(x_train, 'x_train')), width=10).grid(row=0,column=2,padx=10)
        ttk.Button(self.w_load, text="File", command=(lambda:self.path2entry(y_train,'y_train')), width=10).grid(row=1,column=2,padx=10)
        ttk.Button(self.w_load, text="File", command=(lambda:self.path2entry(x_test,'x_test')), width=10).grid(row=2,column=2,padx=10)
        ttk.Button(self.w_load, text="File", command=(lambda:self.path2entry(y_test, 'y_test')), width=10).grid(row=3,column=2,padx=10)
        # ttk.Button(w, text="Select ", command=(lambda:montage_select(w)), width=10).grid(row=8,column=2)

        Confirm = ttk.Button(self.w_load ,text="Confirm", 
                             command=(lambda:self.show_input(self.w_load, n_class, sf, ch, tp)), 
                             width=10).grid(row=9, column=1, pady=5)


    # load xy dataset and check size
    def path2entry(self, entry, set_type):
        path = tk.filedialog.askopenfilename()
        entry.insert(tk.END, path)
        data= self.read_path(path, set_type)
        self.identify_path_type(path, set_type) #identify path 
        self.identify_set_type(data, set_type) #identify data 


    def read_path(self, path, set_type):
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
                # data =data._data
                ftype='.set'

            if '.edf' in path: 
                data= mne.io.read_raw_edf(path,preload= True)
                data =data._data
                ftype='.edf'

            return data     

        except TypeError:
            print('The file format is not supported.')


    def identify_path_type(self, path, set_type): # classify xt, yt, xtest, ytest path
        path= "/".join(path.split('/')[-3:])
        if set_type=='x_train':
            self.X_trainpath= path
        elif set_type=='y_train':
            self.Y_trainpath= path
        elif set_type=='x_test':
            self.X_testpath= path 
        elif set_type=='y_test':
            self.Y_testpath= path

         
    def identify_set_type(self, data, set_type): # classify xt, yt, xtest, ytest data
        if set_type=='x_train':
            self.X_train= data
            self.sch_var.x_train= self.X_train
        elif set_type=='y_train':
            self.Y_train= data
            self.sch_var.y_train= self.Y_train
        elif set_type=='x_test':
            self.X_test= data 
            self.sch_var.x_test= self.X_test
        elif set_type=='y_test':
            self.Y_test= data
            self.sch_var.y_test= self.Y_test


    def confirm_xy_size(self): # numpy array (n_trials, n_chs, n_times) (n_trials,1)
        if (self.X_train != [] and self.Y_train != []):
            if (self.X_train.shape[0] == self.Y_train.shape[0]): # xy train same tiral 
                if self.X_test != []:  
                    if not (self.X_train.shape[1] == self.X_test.shape[1]) and (self.X_train.shape[2] == self.X_test.shape[2]): # xtrain xtest same channel timepoint
                        tk.messagebox.showerror("Error",'Shape of x_train and x_test have to be the same length.', parent=self.w_load) # showerror, showinfo, showwarning 
                        raise ValueError ('Shape of x_train and x_test have to be the same length.')
                    

                    # yes x_test & yes y_test 
                    if self.Y_test != []: 
                        self.sch_var.situation = 2
                        if not (self.X_test.shape[0] == self.Y_test.shape[0]): # X_test, ytest trial the same
                            tk.messagebox.showerror("Error",'Shape of x_test and y_test have to be the same length.', parent=self.w_load)
                            raise ValueError ('Shape of x_test and y_test have to be the same length.')
                        
                    else: # yes x_test , no y_test 
                        self.sch_var.situation=1
                elif 'Y_test' in globals():#no x_test , yes y_test 
                    tk.messagebox.showerror("Error",'You must also load Y_train Data.', parent=self.w_load)
                else: # no x_test, no_ytest  
                    self.sch_var.situation=0    
                
            else: 
                tk.messagebox.showerror("Error",'Trials of x_train and y_train have to be the same length.', parent=self.w_load)
                raise ValueError ('Trials of x_train and y_train have to be the same length.')
            
        else: 
            tk.messagebox.showerror("Error",'You must load files of Train Data and Train Label.')
            raise TypeError( 'You must load files of Train Data and Train Label.')
    
        print('situation: ', self.sch_var.situation)
          

    def show_input(self, w, n_class, sf ,ch, tp):
        self.sch_var.n_class= int(n_class.get())
        self.sch_var.ch= int(ch.get())
        self.sch_var.sf= int(sf.get())

        if (self.X_train != [] or self.Y_train != [] or self.X_test != [] or self.Y_test != []): # no load data, only input data properties and load model weight  
            self.confirm_xy_size()
            if (self.X_train != [] and self.Y_train != []): 
                tk.Label(self.trainframe, text= self.X_trainpath, bg= 'White').grid(row=0, column=1,  sticky=tk.W )
                tk.Label(self.trainframe, text= self.X_train.shape, bg= 'White').grid(row=1, column=1,  sticky=tk.W )
                tk.Label(self.trainframe, text= self.Y_trainpath, bg= 'White').grid(row=2, column=1,  sticky=tk.W )                                                                                                                       
                tk.Label(self.trainframe, text= self.Y_train.shape, bg= 'White').grid(row=3, column=1,  sticky=tk.W ) 
                self.sch_var.tp = self.X_train.shape[2]
                print('x_train size: ', self.X_train.shape,
                      '\ny_train size: ', self.Y_train.shape)

            if self.X_test != []:
                tk.Label(self.testframe, text = self.X_testpath, bg = 'White').grid(row=0, column=1,  sticky=tk.W )
                tk.Label(self.testframe, text = self.X_test.shape, bg = 'White').grid(row=1, column=1,  sticky=tk.W)
                print('x_test size: ', self.X_test.shape)

            if self.Y_test != []:
                tk.Label(self.testframe, text= self.Y_testpath, bg= 'White').grid(row=2, column=1,  sticky=tk.W )
                tk.Label(self.testframe, text= self.Y_test.shape, bg= 'White').grid(row=3, column=1,  sticky=tk.W)
                print('y_test size: ', self.Y_test.shape)

            else:
                self.sch_var.tp= int(tp.get())

            w.destroy()
            tk.Label(self.modelframe, text= self.scheme_var.sf, bg= 'White').grid(row=1, column=1,  sticky=tk.W)
            self.Model.entryconfig("Model Selection", state="normal")


    # Menu- File- Load weight
    def Weightname(self):
        file= tk.filedialog.askopenfilename()
        shortpath= "/".join(file.split('/')[-2:])
        self.shortloadweightfile.set(shortpath)
        tk.Label(self.modelframe, textvariable = self.shortloadweightfile, bg= 'White').grid(row=7, column=1)
        visual_class = Visualization(self.sch_var)
        self.conv1, self.conv2= visual_class.get_weight(filepath=file)
        self.sch_var.loadweightfile= file
        self.Results.entryconfig("Model Interpretation", state="normal")
    
    # print(f'conv1: {conv1.shape}')
    # conv1size = tk.Label(window, text= f'conv1: {conv1.shape}').grid(row=9, column=1)
    # conv2size = tk.Label(window, text= f'conv2: {conv2.shape}').grid(row=10, column=1)


    # Menu- Model- Model Selection   
    def load_model_struct(self): 
        win_lms = self.new_window(Title='Load model structure', size='500x200', x_pad=-10, y_pad=220)
        modelist = ttk.Combobox(win_lms,
                                values=['SCCNet',
                                        'EEGNet',
                                        'ShallowConvNet'],
                                state="readonly")

        Confirm = ttk.Button(win_lms ,text="Confirm", command=(lambda:[self.model_select(win_lms, modelist)]))
        modelist.pack()
        Confirm.pack()


    def model_select(self, win_lms, modelist):
        exec(open('./ExBrainable/ExBrainable/models.py').read(), globals()) # put all variable to globals()
        name = modelist.get()
        print(name)
        self.sch_var.netname= eval(str(name+'()'))
        tk.Label(self.modelframe, text=name, bg= 'White').grid(row=0, column=1,  sticky=tk.W ) 

        self.filemenu.entryconfig("Load Model Weight", state= 'normal')
        self.Model.entryconfig("Training Setting", state="normal")
    
        win_lms.destroy()


    # File- study
    def load_files(self):
        w_files = self.new_window(Title='Cross subject study', size='500x450', x_pad=-10, y_pad=10)

        xframes = tk.LabelFrame(w_files, text="Data", height=10, bg='White', width=50, labelanchor='n')
        xframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        yframes = tk.LabelFrame(w_files, text="Labels", height=10, bg='White', width=50, labelanchor='n')
        yframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)

        ttk.Button(xframes, text='Add Files', command=(lambda:self.read_data_path(xframes, 'x_train')), width=10).pack()
        ttk.Button(yframes, text='Add Files', command=(lambda:self.read_data_path(yframes, 'y_train')), width=10).pack()
   
        Confirm = ttk.Button(w_files ,text="Confirm", command=(lambda:self.rename_events(w_files)), width=10).pack()


    def read_data_path(self, frame, set_type):
        # identify pathtypes: multiple sub files are named as 'files_x_train','files_y_train'...
        files = tk.filedialog.askopenfilenames()
        fnum=1
        self.concat_data = []
        self.event_ids = []
        self.subname = []
        self.sublen = []

        for path in files:
            # name each path: 'x_trainpath_1','x_trainpath_2'
            globals()[str(set_type)+'path_'+str(fnum)] = path

            # read and each file:'xtrain_1', 'xtrain_2' 
            globals()[str(set_type)+'_'+str(fnum)] = self.read_path(path, set_type)

            #concat diff files labels #need revise  
            data= globals()[str(set_type)+'_'+str(fnum)]
            fnum+=1
        
            if '.mat' in path and 'y' in set_type:
                if self.concat_data != None:
                    self.concat_data= data.reshape(-1)
                else:
                    self.concat_data= np.concatenate((self.concat_data, data.reshape(-1)))
            
                # find eventids from labels
                for i in data.reshape(-1):
                    if i not in self.event_ids:
                        self.event_ids.append(i)
                self.event_ids.sort(reverse=False)

                print(self.concat_data.shape)
            
            # display each file name
            fname= path.split('/')[-1]
            tk.Label(frame, text= fname, bg='White').pack(fill='both',padx=20)
            self.subname.append( fname.split('.')[0])
            self.sublen.append( len(data))

        print(self.event_ids, self.subname, self.sublen)


    def findevents(self, x):
        return {
            #'.set': data.event_id,
            '.mat': self.event_ids,
        }[x]


    def rename_events(self, w_files):
        w_files.destroy()
        w = self.new_window('Rename Events', '500x250', x_pad=-10, y_pad=180)

        # t_frame = tk.Frame(w, bg="White", bd=1, relief="sunken", width=450, height=50)
        # t_frame.pack(side='top', fill='both',pady=30, ipady=20,ipadx=4)
        print('len of eventtype', len(self.findevents(ftype)))
        self.event_ids= self.findevents(ftype)

        self.table= ttk.Treeview(w, height=len(self.event_ids))
    
        # create scroll bar 
        sb = Scrollbar(w, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.config(yscrollcommand=sb.set)
        sb.config(command=self.table.yview)

        self.table['column']= ['Event ID','Event type']
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('Event ID', anchor=tk.CENTER, width=30 )
        self.table.column('Event type', anchor=tk.CENTER, width=130)
        # table.column('Count', anchor=tk.CENTER, width=80)

        self.table.heading('#0', text='', anchor=tk.CENTER)
        self.table.heading('Event ID', text='Event ID', anchor=tk.CENTER)
        self.table.heading('Event type', text='Event type', anchor=tk.CENTER)

        if ftype== '.set': 
            for row in range(len(self.event_ids)):
                eventypes=list(self.event_ids.keys())
                item= self.table.insert(parent='', index=row, iid= row, text='', values=[self.event_ids[eventypes[row]], eventypes[row] ])
                self.table.item(item, tags=item)
        if ftype== '.mat':
            global eventype
            eventype= [None]*len(self.event_ids) # eventype is none default in mat file 
            for row in range(len(self.event_ids)):
                item= self.table.insert(parent='', index=row, iid= row, text='', values=[self.event_ids[row], eventype[row] ])
                self.table.item(item, tags=item)

        self.table.bind('<1>', self.editname)
        self.table.pack(side='top', fill='x',padx=10, pady=10)

        Confirm = ttk.Button(w ,text="Confirm", command=(lambda:self.all_data(w)), width=10).pack()
        # plot events
        # figure = Figure(figsize=(5,5))
        # ax = figure.add_subplot(1, 1, 1)
        # mne.viz.plot_events(data.events, event_id=data.event_id, sfreq=562, axes=ax)
        # canvas = FigureCanvasTkAgg(figure, w)
        # canvas.get_tk_widget().pack(side='bottom')


    def editname(self, event):
        if self.table.identify_region(event.x, event.y) == 'cell':
            # the user clicked on a cell

            def ok(event):
                """Change item value."""
                #print(entry.get(), type(entry.get()))
                if column == '#1':
                    self.event_ids[int(item)]= int(entry.get())
                if column == '#2':
                    eventype[int(item)]= entry.get()
                print(self.event_ids, eventype)

                self.table.set(item, column, entry.get())
                entry.destroy()
        
            column = self.table.identify_column(event.x)  # identify column
            item = self.table.identify_row(event.y)  # identify item
            x, y, width, height = self.table.bbox(item, column) 
            value = self.table.set(item, column)

        elif self.table.identify_region(event.x, event.y) == 'heading': 
            # the user clicked on a heading

            def ok(event):
                """Change heading text."""
                self.table.heading(column, text=entry.get())
                entry.destroy()

            column = self.table.identify_column(event.x) # identify column
            # tree.bbox work sonly with items so we have to get the bbox of the heading differently
            x, y, width, _ = self.table.bbox(self.table.get_children('')[0], column) # get x and width (same as the one of any cell in the column)
            # get vertical coordinates (y1, y2)
            y2 = y
            # get bottom coordinate
            while self.table.identify_region(event.x, y2) != 'heading':  
                y2 -= 1
            # get top coordinate
            y1 = y2
            while self.table.identify_region(event.x, y1) == 'heading':
                y1 -= 1
            height = y2 - y1
            y = y1
            value = self.table.heading(column, 'text')

        elif self.table.identify_region(event.x, event.y) == 'nothing': 
            column = self.table.identify_column(event.x) # identify column
            # check whether we are below the last row:
            x, y, width, height = self.table.bbox(self.table.get_children('')[-1], column)
            if event.y > y:

                def ok(event):
                    """Change item value."""
                    # create item
                    item = self.table.insert("", "end", values=("", ""))
                    self.table.set(item, column, entry.get())
                    entry.destroy()

                y += height
                value = ""
            else:
                return
        else:
            return
        # display the Entry   
        entry = ttk.Entry(self.table)  # create edition entry
        entry.place(x=x, y=y, width=width, height=height,
                    anchor='nw')  # display entry on top of cell
        entry.insert(0, value)  # put former value in entry
        entry.bind('<FocusOut>', lambda e: entry.destroy())  
        entry.bind('<Return>', ok)  # validate with Enter
        entry.focus_set()


    def all_data(self, w):
        w.destroy()
        w_data= self.new_window('Events ', '900x500', x_pad=-10, y_pad=100)

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
            # print(len(concat_data))
        
            # create scroll bar
            sb = Scrollbar(locals()['frame_'+ t], orient=tk.VERTICAL)
            sb.grid(row=0,column=1,sticky='ns')
            tables[t].config(yscrollcommand=sb.set)
            sb.config(command=tables[t].yview)
        
            # create columns
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
                for row in range(len(self.concat_data)):
                    if row < self.sublen[i]:
                        tables[t].insert(parent='', index=row, iid= row, text='', 
                                         values=[self.subname[i], self.concat_data[row], 
                                         eventype[self.concat_data[row]] , 'None'])
                    else:
                        i+=1
                        self.sublen[i]+= self.sublen[i-1]    

                for col in columns:
                    tables[t].heading(col, text= col, command= lambda c=col: self.sort_id(tables[t], c, False))
                i=0

            elif t== 'train':
                for row in range(5):
                    tables[t].insert(parent='', index=row, iid= row, text='', values=['ha', 'he', 'he' , 'ge'])
                for col in columns:
                    tables[t].heading(col, text= col, command= lambda c=col: self.sort_id(tables[t], c, False))
        
            elif t== 'test':
                for row in range(5):
                    tables[t].insert(parent='', index=row, iid= row, text='', values=['ha', 'he', 'he' , 'ge'])
                for col in columns:
                    tables[t].heading(col, text= col, command= lambda c=col: self.sort_id(tables[t], c, False))
        #ttk.Button(frame_allevents ,text="Move to training set", command=(Moveto(tables))).grid(row=1, column=0)
        #ttk.Button(frame_allevents ,text="Move to test set", command=(Moveto(tables))).grid(row=1, column=1)
    

    def Moveto(self, tables):
        data= tk.Variable()
        print([self.table['allevents'].item(idx) for idx in tables['allevents'].selection()])
        #data.set([table['allevents'].item(idx) for idx in tables['allevents'].selection()])
    

    def sort_id(self, table, col, reverse):
        l = [(table.set(k, col), k) for k in table.get_children('')]
        #print(l) #[(eventid,rowindex), ... ]
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
        #print(l) #sort by eventid 

        for index, (val, k) in enumerate(l): # save sorted changes to table 
            table.move(item= k, parent= '', index= index) # move k to index position
            table.heading(col,command=lambda: self.sort_id(table, col, False))


    # Menu- Model- Training setting  
    def Model_Preparation(self):
        win_p=self.new_window(Title='Training Setting ', size='500x200', x_pad=-10, y_pad=180)
        # topic
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

        weightfolder= ttk.Button(win_p, text="Folder", command=(lambda:self.save_weight_folder(Save_weight)), width=10).grid(row=4,column=2)

        Confirm = ttk.Button(win_p ,text="Confirm", command=(lambda:self.show_para(win_p,Valratio, Batchsize, Epoch, Lr)), width=10).grid(row=6, column=1)


    def save_weight_folder(self, entry):
        folder= tk.filedialog.askdirectory()
        self.shortfolder= "/".join(folder.split('/')[-3:])
        entry.insert(tk.END, folder)
        self.sch_var.saveweightfolder= folder    


    def show_para(self, win_p, Valratio, Batchsize, Epoch, Lr):
        self.sch_var.val_ratio= float(Valratio.get())
        self.sch_var.bs= int(Batchsize.get())
        self.sch_var.epochs= int(Epoch.get())
        self.sch_var.lr= float(Lr.get())
        self.shortweightfolder.set(self.shortfolder)
        # close w
        win_p.destroy()

        # para in control display 
        tk.Label(self.modelframe, text= self.sch_var.val_ratio, bg= 'White').grid(row=2, column=1,  sticky=tk.W )
        tk.Label(self.modelframe, text= self.sch_var.bs, bg= 'White').grid(row=3, column=1,  sticky=tk.W )
        tk.Label(self.modelframe, text= self.sch_var.epochs, bg= 'White').grid(row=4, column=1 ,  sticky=tk.W)
        tk.Label(self.modelframe, text= self.sch_var.lr, bg= 'White').grid(row=5, column=1,  sticky=tk.W)
        tk.Label(self.modelframe, textvariable= self.shortweightfolder , bg= 'White').grid(row=6, column=1,  sticky=tk.W)
    
        self.model_summary()
        self.Model.entryconfig("Model Training", state="normal")


    def model_summary(self):
        net= self.sch_var.netname
        dev = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        summary(net.to(dev), (1,self.sch_var.ch, self.sch_var.tp), batch_size=self.sch_var.bs)
        self.output = new_stdout.getvalue()
        sys.stdout = old_stdout


        rows= self.output.split('\n')
        for row in rows:
            if 'Trainable params' in row:
                row= row.replace(',','').split(':')
                trainable_para= int(row[1])
            if 'Estimated Total Size' in row:
                row= row.split(':')
                memory_size= float(row[1].strip())

        tk.Label(self.modelframe, text=trainable_para, bg= 'White').grid(row=9, column=1, sticky=tk.W)
        tk.Label(self.modelframe, text=memory_size, bg= 'White').grid(row=10, column=1, sticky=tk.W)
        self.Model.entryconfig("Model Summary", state="normal")


    def full_model_summary(self):
        w = self.new_window('Model Summary', size= '500x500', x_pad=-10, y_pad=180)
        soutput= self.output.replace('=','').replace('-', '')
        tk.Label(w, text= soutput, bg= 'White').grid()
        # rows= output.split('\n')
        # srows= [row.replace('=','').replace('-', '')+ '\n' for row in rows]
        # i=0
        # for row in soutput: 
        #     tk.Label(w, text= row, bg= 'White').grid(row=i, column=0, sticky=tk.W)
        #     i+=1


    # Menu- Model- Start training
    def bar(self): # w_bar, ypred, ypr remove from scheme_var? 
        DLoader = DataLoader(FT = FALSE, sch_var = self.sch_var)
        self.sch_var.w_bar = self.new_window(Title='Model Training', size='500x150', x_pad=-10, y_pad=180)

        self.progressbar = Progressbar(self.sch_var.w_bar, mode='determinate',length= 500, maximum= self.sch_var.epochs)
        self.progressbar.pack(anchor= tk.CENTER)

        self.value_label = tk.Label(self.sch_var.w_bar, text= self.update_progress_label())
        self.value_label.pack(anchor= tk.CENTER)

        self.buttom= ttk.Button(self.sch_var.w_bar, text="Start Training",command=lambda:self.start_train_thread())
        self.buttom.pack(side= tk.BOTTOM, padx= 20, pady=10)

        # Dataloader 
        if (self.sch_var.situation==1 or self.sch_var.situation ==2) :
            self.sch_var.trainloader, self.sch_var.valloader, self.sch_var.testloader=DLoader.Individual_Dataset()
        else: # situation==0
            self.sch_var.trainloader, self.sch_var.valloader= DLoader.Individual_Dataset()
 
        self.sch_var.w_bar.protocol("WM_DELETE_WINDOW", lambda: self.quit_train()) # interaction between app and window manaager


    def start_train_thread(self):
        self.sch_var.stop_thread= False
        self.buttom['state'] = tk.DISABLED #disable buttom while training
        evaluate_class = Evaluate(self.sch_var)
        self.train_thread= threading.Thread(target= evaluate_class.Scheme, daemon= True) #aquire epoch from train scheme
        self.progressbar.start(interval= 400)
        self.train_thread.start()
        self.sch_var.w_bar.after(400, self.check_train_thread)
        self.control_menu_activity()
    

    def check_train_thread(self):
        print(variable.update_epo)

        self.progressbar["value"]= variable.update_epo
        self.value_label["text"] = self.update_progress_label()

        if self.train_thread.is_alive() :
            self.sch_var.w_bar.after(400, self.check_train_thread) # control update epoch speed
        else: 
            self.progressbar.stop()

            global conv1, conv2
            print(self.sch_var.saveweightfolder)
            visual_class = Visualization(self.sch_var)
            conv1,conv2= visual_class.get_weight(filepath=f'{self.sch_var.saveweightfolder}/temp.pth')
            self.shortloadweightfile.set(f'{self.shortfolder}/temp.pth')
            tk.Label(self.modelframe, textvariable= self.shortloadweightfile, bg= 'White').grid(row=7, column=1, sticky=tk.W) 
            tk.Label(self.modelframe, text= f'{self.sch_var.training_time:.2f}' , bg= 'White').grid(row=8, column=1, sticky=tk.W) 


    def update_progress_label(self):
        label= self.progressbar["value"]
        return f"Epoch: {label}/ {self.sch_var.epochs}"


    def quit_train(self):
        if tk.messagebox.askokcancel('Quit', 'Do you want to quit?', parent=self.sch_var.w_bar):
            self.sch_var.stop_thread= True
            self.sch_var.w_bar.destroy()


    def control_menu_activity(self):
        if self.sch_var.situation==0: #only xtrain ytrain 
            self.Results.entryconfig("Model Interpretation", state="normal")
        if (self.sch_var.situation==1 or self.sch_var.situation==2): 
            self.Results.entryconfig("Model Prediction", state="normal")
            self.Results.entryconfig("Model Interpretation", state="normal")


    # Menu- Results- Model Prediction
    def PredictiveLabel(self):
        w = self.new_window('Model Prediction', '500x250', x_pad=-10, y_pad=180)
        evaluate_class = Evaluate(self.sch_var)

        # Model testing 
        if self.sch_var.situation==1:
            self.y_pred, self.y_pr = evaluate_class.Test()
        if self.sch_var.situation==2:
            self.sch_var.acc, self.sch_var.kappa, self.y_pred, self.y_pr = evaluate_class.Test() 
            self.Results.entryconfig("Model Performance", state="normal")

        # save buttom
        # create table 
        table= ttk.Treeview(w)
        #create scroll bar 
        sb = Scrollbar(w, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        table.config(yscrollcommand=sb.set)
        sb.config(command=table.yview)

        table['column']= ['ID','Predictive Label']+[f'Class {i}'for i in range(self.sch_var.n_class)]
        table.column('#0', width=0, stretch=tk.NO)
        table.column('ID', anchor=tk.CENTER, width=30 )
        table.column('Predictive Label', anchor=tk.CENTER, width=130)
        [table.column(f'Class {i}', anchor=tk.CENTER, width=80) for i in range(self.sch_var.n_class)]

        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('ID', text='ID', anchor=tk.CENTER)
        table.heading('Predictive Label', text='Predictive Label', anchor=tk.CENTER)
        [table.heading(f'Class {i}', text=f'Class {i}', anchor=tk.CENTER) for i in range(self.sch_var.n_class)]

        for row in range(len(self.y_pred)):
            table.insert(parent='', index=row, iid= row, text='', values=[f'{row}', self.y_pred[row]]+[self.y_pr[row,i] for i in range(self.sch_var.n_class)])
        table.pack()

        tk.Button(w, text="Save",borderwidth=2, relief='solid',bg='White', command=lambda:self.save_y(self.y_pr, self.y_pred)).pack(fill='x')     


    def save_y(self, y_pr, y_pred):
        folder= tk.filedialog.askdirectory()
        y_pred= y_pred.reshape(-1,1)
        print('Probability size:', y_pr.shape,'\nLabel size', y_pred.shape)
        np.savetxt(folder+'/data.csv', np.concatenate((y_pred, y_pr), axis=1), delimiter=',')


    # Menu- Results- Model Interpretation - spatial/temporal pattern
    # plot_spatial, powerspectum in visualization.py

    # Menu- Results- Model Performance  
    def Model_performance(self):
        w = self.new_window('Model Performance', '700x500', x_pad=-10, y_pad=180)
 
        self.Results.entryconfig("Model Prediction", state="normal")

        #acc kappa cm
        visual_class = Visualization(self.sch_var)
        visual_class.Confusion_Matrix(w, self.Y_test, self.y_pred)  # in visualization.py 

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
        table.insert(parent='', index=0, iid= 0 , text='', values=[f'{self.sch_var.acc:.3f}', f'{self.sch_var.kappa:.3f}'])
        table.pack()  
        

        




if __name__ == '__main__':
    exbrainable1 = ExBrainable()
    exbrainable1.Main()
