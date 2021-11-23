import tkinter as tk
from tkinter.constants import ANCHOR
import tkinter.ttk as ttk
import numpy as np
import scipy.io
import mne

from tkinter import filedialog

class ExBrainable():
    def __init__(self):
        self.w_main= tk.Tk()
        self.w_main.geometry('500x750')
        self.w_main.title("ExBrainable")
        self.w_main.configure(background='White')
        self.MainDashBoard()
        self.Menu()

    def MainDashBoard(self):
        global trainframe, modelframe, testframe

        trainframe = tk.LabelFrame(self.w_main, text="Training Data", height=10, bg='White', width=50, labelanchor='n')
        trainframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        tk.Label(trainframe, text="Train Data (X_train) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(trainframe, text="Train Data size :　", bg= 'White').grid(row=1, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(trainframe, text="Train Label (Y_train) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(trainframe, text="Train Label size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)
    

        modelframe = tk.LabelFrame(self.w_main, text="Model and Training Setting", height=10, bg='White', width=50, labelanchor='n')
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

        testframe = tk.LabelFrame(self.w_main, text="Test Data", height=10, bg='White', width=50, labelanchor='n')
        testframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        tk.Label(testframe, text="Test Data(X_test) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(testframe, text="Test Data Size :　", bg= 'White').grid(row=1 ,column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(testframe, text="Test Label(Y_test) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(testframe, text="Test Label Size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)

    def Menu(self):
        menubar = tk.Menu(self.w_main)
        global filemenu, Results, Model, wmainself

        # Menu- File
        wmainself=self
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File ', menu=filemenu)
        filemenu.add_command(label='Study(cross subject)', command=lambda:MultiSubjects())
        self.w_main.config(menu= menubar)
        




class MultiSubjects():
    def __init__(self):
        self.w= new_window(Title='Cross subject study', size='500x450', x_pad=-10, y_pad=10)
        self.Display()
    
    def Display(self):
        xframes = tk.LabelFrame(self.w, text="Data", height=10, bg='White', width=50, labelanchor='n')
        xframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        yframes = tk.LabelFrame(self.w, text="Labels", height=10, bg='White', width=50, labelanchor='n')
        yframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)

        ttk.Button(xframes, text='Add Files', command=(lambda:self.ReadFilesFindEventids(xframes, 'x_train')), width=10).pack()
        ttk.Button(yframes, text='Add Files', command=(lambda:self.ReadFilesFindEventids(yframes, 'y_train')), width=10).pack()

        Confirm = ttk.Button(self.w ,text="Confirm", command=(lambda:self.RenameEvents(self.w)), width=10).pack()

    def ReadFilesFindEventids(self,frame, set_type):
        global concat_data, event_ids, subname, sublen
        # identify pathtypes: multiple sub files are named as 'files_x_train','files_y_train'...
        files = filedialog.askopenfilenames()
        fnum=1
        event_ids=[]
        subname=[]
        sublen=[]

        for path in files:
            # name each path: 'x_trainpath_1','x_trainpath_2'
            globals()[str(set_type)+'path_'+str(fnum)]= path

            # read and each file:'xtrain_1', 'xtrain_2' 
            globals()[str(set_type)+'_'+str(fnum)]= self.ReadFiles(path, set_type)

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

    def ReadFiles(self,path, set_type):
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

    def RenameEvents(self,wcross):
        wcross.destroy()
        w= new_window('Rename Events', '500x250', x_pad=-10, y_pad=180)
        global table

        # t_frame = tk.Frame(w, bg="White", bd=1, relief="sunken", width=450, height=50)
        # t_frame.pack(side='top', fill='both',pady=30, ipady=20,ipadx=4)
        print('len of eventtype', len(self.findevents(ftype)))
        event_ids= self.findevents(ftype)

        table= ttk.Treeview(w, height=len(event_ids))
        
        #create scroll bar 
        sb = tk.Scrollbar(w, orient=tk.VERTICAL)
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

        table.bind('<1>', self.Editname)
        table.pack(side='top', fill='x',padx=10, pady=10)

        Confirm = ttk.Button(w ,text="Confirm", command=(lambda:DataOverview(w)), width=10).pack()

    def findevents(self,x):
        return {
            #'.set': data.event_id,
            '.mat': event_ids,
        }[x]

    def Editname(self,event):

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

class DataOverview():
    def __init__(self,w):
        self.Display(w)
        self.ListAllEvents()

    def Display(self,w):
        w.destroy()
        self.w_data= new_window('Events ', '500x380', x_pad=-10, y_pad=100)
        self.frame_allevents= tk.LabelFrame(self.w_data,text="All Events",bg="White", labelanchor='n')
        self.frame_validation= tk.LabelFrame(self.w_data,text="Validation",bg="White", labelanchor='n')
        self.frame_allevents.grid(row=0, column=0,padx=10,pady=10)
        self.frame_validation.grid(row=0, column=1)

        #individual scheme
        self.WithinorCross = tk.IntVar()
        self.ValMethod= tk.IntVar()

        tk.Label(self.frame_validation, text='Session', bg="White").grid(row=0, column=0)
        tk.Checkbutton(self.frame_validation, text='Train within a session',variable=self.WithinorCross, onvalue=1, offvalue=0, bg="White").grid(row=1, column=0, sticky=tk.W)
        tk.Checkbutton(self.frame_validation, text='Train cross sessions ',variable=self.WithinorCross, onvalue=2, offvalue=0,bg="White").grid(row=2, column=0, sticky=tk.W)
        tk.Label(self.frame_validation, text='Method', bg="White").grid(row=3, column=0)
        tk.Checkbutton(self.frame_validation, text='5-fold',variable=self.ValMethod, onvalue=1, offvalue=0,bg="White").grid(row=4, column=0, sticky=tk.W)
        tk.Checkbutton(self.frame_validation, text='10-fold',variable=self.ValMethod, onvalue=2, offvalue=0, bg="White").grid(row=5, column=0, sticky=tk.W)
        tk.Checkbutton(self.frame_validation, text='LOOCV(trial) ',variable=self.ValMethod, onvalue=3, offvalue=0,bg="White").grid(row=6 ,column=0, sticky=tk.W)
        ttk.Button(self.frame_validation ,text="Confirm", command=(lambda:SchemeValMethod(self.WithinorCross.get(), self.ValMethod.get() )), width=10).grid(row=7 ,column=0)

        # adjust row space 
        _, row_count = self.frame_validation.grid_size()
        for row in range(row_count):
            self.frame_validation.grid_rowconfigure(row, minsize=40) 

        

    def ListAllEvents(self):
        # .mat 
        table= ttk.Treeview(self.frame_allevents, height=15)
        
        #create scroll bar
        sb = tk.Scrollbar(self.frame_allevents, orient=tk.VERTICAL)
        sb.grid(row=0,column=1,sticky='ns')
        table.config(yscrollcommand=sb.set)
        sb.config(command=table.yview)
        
        #create columns
        table['column']= ['Subject','Event ID','Event type','Onset time']
        columns= table['column']

        table.column('#0', width=0, stretch=tk.NO)
        table.heading('#0', text='', anchor=tk.CENTER)
        for col in columns:
            table.column(col, anchor=tk.CENTER, width=70 )
            table.heading(col, text='', anchor=tk.CENTER)

        table.grid(row=0, sticky= tk.N)

        i=0
        for row in range(len(concat_data)):
            if row < sublen[i]:
                table.insert(parent='', index=row, iid= row, text='', values=[subname[i], concat_data[row], eventype[concat_data[row]] , 'None'])
            else:
                i+=1
                sublen[i]+= sublen[i-1]    

        for col in columns:
            table.heading(col, text= col, command= lambda c=col: self.sort_id(table, c, False))
        i=0


    def sort_id(table, col, reverse):
        l = [(table.set(k, col), k) for k in table.get_children('')]
        #print(l) #[(eventid,rowindex), ... ]
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
        #print(l) #sort by eventid 

        for index, (val, k) in enumerate(l): # save sorted changes to table 
            table.move(item= k, parent= '', index= index) # move k to index position
            table.heading(col,command=lambda: self.sort_id(table, col, False))

              

class SchemeValMethod():
    def __init__(self,userscheme,usermethod):
        self.Scheme= {1: 'Within', 2: 'Cross'}
        self.Method= {1 : '5fold', 2: '10fold', 3: 'LOOCV'}
        self.userscheme= userscheme
        self.usermethod= usermethod
        print(f'{self.userscheme} {self.usermethod} session')

    def GetMethod(self):
        # .get(key, default)
        self.Scheme.get(self.userscheme, 'Within')()
        self.Method.get(self.usermethod, '5fold')()
    # def Within():

    # def Cross(): 
    
    # def kfold():

    # def loocv():





        







def new_window(Title, size, x_pad, y_pad):

    win_main_x = wmainself.w_main.winfo_rootx()+ x_pad
    win_main_y = wmainself.w_main.winfo_rooty()+ y_pad

    newindow= tk.Toplevel()
    newindow.wm_attributes('-topmost', True )
    newindow.geometry(size)
    newindow.geometry(f'+{win_main_x}+{win_main_y}')  
    newindow.title(Title)
    newindow.configure(background='White')

    return newindow

if __name__ == '__main__':
    gui= ExBrainable()
    gui.w_main.mainloop()







