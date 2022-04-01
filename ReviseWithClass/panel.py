import tkinter as tk
import tkinter.ttk as ttk
import io
import sys

from tkinter import messagebox
from window import new_window
from Load_data import LoadData, DataSortandSplit



'''
(finished)
class Load_Data_Panel:
ps. from Load_data import LoadData, DataSortandSplit
'''
class Load_Data_Panel():
    def __init__(self, database):
        self.database= database
        d= LoadData(self.database)
        #r= RenameEvents()
        self.w= new_window(Title='Load Data Files', size='500x450', x_pad=-10, y_pad=10, database= self.database)
        self.xframes = tk.LabelFrame(self.w, text="Data", height=50, bg='White', width=50, labelanchor='n')
        self.yframes = tk.LabelFrame(self.w, text="Labels", height=10, bg='White', width=50, labelanchor='n')
        self.properyframe = tk.LabelFrame(self.w, text="Properties", height=10, bg='White', width=50, labelanchor='n')
        self.xframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        self.yframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        self.properyframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)

        ttk.Button(self.xframes, text='Add Files', command=(lambda : d.ReadData(self.xframes)), width=10).pack(fill='both', ipadx=1 ,padx=20 ,pady=5)
        ttk.Button(self.yframes, text='Add Files', command=(lambda : d.ReadLabels(self.yframes)), width=10).pack(fill='both', ipadx=1 ,padx=20 ,pady=5)
        
        tk.Label(self.properyframe, text="Sampling Rate :　", bg= 'White').grid(row=0, column=0, sticky=tk.W,padx=10, pady=5)
        tk.Label(self.properyframe, text="Timepoint :  ", bg= 'White').grid(row=1, column=0, sticky=tk.W,padx=10, pady=5)
        self.database.set_var.sf =  tk.StringVar()
        self.database.set_var.tp =  tk.StringVar()
        self.sfentry= tk.Entry(self.properyframe, textvariable=self.database.set_var.sf)
        self.tpentry= tk.Entry(self.properyframe,textvariable=self.database.set_var.tp)
        self.sfentry.grid(row=0, column=1, sticky=tk.W)
        self.tpentry.grid(row=1, column=1, sticky=tk.W)

        ttk.Button(self.w ,text="Confirm", command=(lambda:Rename_Events_Panel(self.w, self.database)), width=10).pack(fill='both', ipadx=1 ,ipady= 5,padx=20 ,pady=5)

'''
(finished)
class Rename_Events_Panel
- uniqueevents(): find all eventsid, eventype from all input files 
- Eventable(): build a table listing all eventids, eventype 
- Editname(): functions of renaming events by clicking the table cell
- updatevent(): update changed events to all original events
'''
class Rename_Events_Panel():
    def __init__(self, wdata, database):
        self.database= database
        wdata.destroy()
        self.w= new_window('Rename Events', '500x250', x_pad=-10, y_pad=180, database= self.database)
        self.uniquevents()
        self.Eventable()

        print('len of eventtype', len(self.uniquevent.keys()))
        print(self.uniquevent)
        self.database.set_var.n_class= len(self.uniquevent.keys())

    def uniquevents(self):        
        self.uniquevent={}
        self.EventFiles= self.database.data.Data
        #for index in range(len())
        for fileevent in self.EventFiles.keys(): #fir each file 
            for eventype in self.EventFiles[fileevent].event_id.keys(): #each event 
                if eventype not in self.uniquevent:
                    eventlist= self.EventFiles[fileevent].event_id
                    self.uniquevent[eventype]=eventlist[eventype] # {'eventype', 'id'}  

    def Eventable(self):
        self.table= ttk.Treeview(self.w, height=len(self.uniquevent.keys()))
        sb = tk.Scrollbar(self.w, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.config(yscrollcommand=sb.set)
        sb.config(command=self.table.yview)

        self.table['column']= ['Event ID','Event type']
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('Event ID', anchor=tk.CENTER, width=30 )
        self.table.column('Event type', anchor=tk.CENTER, width=130)
        self.table.heading('#0', text='', anchor=tk.CENTER)
        self.table.heading('Event ID', text='Event ID', anchor=tk.CENTER)
        self.table.heading('Event type', text='Event type', anchor=tk.CENTER)
        
        self.fnames= self.EventFiles.keys()
        self.dictEventypeid= self.uniquevent.items()
        
        print(self.fnames)
        if '.set' in list(self.fnames)[0]: 
            for row,(type, id) in enumerate(self.dictEventypeid):
                #eventypes=list(event_ids.keys())
                print(row, type, id)
                item= self.table.insert(parent='', index=row, iid= row, text='', values=[id, type])
                self.table.item(item, tags=item)

        self.eventype = list(self.uniquevent.keys())
        self.event_ids = list(self.uniquevent.values())

        self.table.bind('<1>', self.Editname, self.table)
        self.table.pack(side='top', fill='x',padx=10, pady=10)


        Confirm = ttk.Button(self.w ,text="Confirm", command=(self.updatevent), width=10).pack()
        

    def Editname(self,event):
        

        if self.table.identify_region(event.x, event.y) == 'cell':
            # the user clicked on a cell
            
            def ok(event):
                """Change item value."""
                #print(entry.get(), type(entry.get()))
                if column=='#1':
                    self.event_ids[int(item)]= int(entry.get())
                if column=='#2':
                    self.eventype[int(item)]= entry.get()
                print(column,item,self.event_ids, self.eventype)

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
            x, y, width, height =self.table.bbox(self.table.get_children('')[-1], column)
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

    def updatevent(self):
        
        '''change eventid eventtype to each files'''
        self.renamevent={}
        for i in range(len(self.uniquevent)):
            self.renamevent[self.eventype[i]]= self.event_ids[i] 
            #print(self.eventype[i],self.event_ids[i])
        print('Rename Events:', self.renamevent)

        for fname in self.fnames:
            self.database.data.Data[fname].event_id = self.renamevent
            print(self.database.data.Data[fname].event_id)    
        
        CrossValidation_Panel(self.w, self.database)


'''
(finished)
class Crossvalidation_Panel: contains 2 tabs including the Individual panel and the Cross subject panel.
'''

class CrossValidation_Panel:
    def __init__(self, wRenamevent, database):
        self.database= database
        wRenamevent.destroy()
        COLOR= 'White'
        '''define frame and notebook style'''
        noteStyler = ttk.Style()
        noteStyler.configure("TNotebook", background=COLOR, borderwidth=0)
        noteStyler.configure("TNotebook.Tab", background=COLOR, foreground='Black', lightcolor=COLOR, borderwidth=0)
        noteStyler.configure("TFrame", background=COLOR, foreground=COLOR, borderwidth=0)

        '''create tabs'''
        w =new_window('Cross Validation', '400x600', x_pad=60, y_pad=50, database= self.database)
        TabParent=ttk.Notebook(w, style= "TNotebook")
        Tab1= ttk.Frame(TabParent, style='TFrame')
        Tab2= ttk.Frame(TabParent, style='TFrame')
        TabParent.add(Tab1, text= 'Individual Subject')
        TabParent.add(Tab2, text= 'Cross Subject')
        TabParent.grid(row=0, column=0)

        '''Tab1: Individual Panel
           Tab2: Cross Subject Panel'''
        Individual_Panel(Tab1, self.database)
        CrossSubject_Panel(Tab2, self.database)
   
'''
(almost finished)需要將combobox 改為listbox，因為listbox可以同時選擇多個檔案

class Individual_Panel
- kfoldstate():不同cv method -> frame disable/normal
- state(): frame裡面的comobox/entry disable/normal 
- Input2Database(): transfer entry values to database
    + checkemptyvalues(): empty entry show error
        completeNumber(): string to list ex: class= '1,2,3,4' ->  ['1']
    + Checkfile(): identify val/test belongs to choices of 
                 split from train or choose a file

'''
class Individual_Panel:
    def __init__(self,w, Database):
        self.w =w 
        self.data = Database.data

        self.CrossFile = tk.LabelFrame(self.w, text="Cross Validation File", height=10, bg='White', width=50, labelanchor='n')
        self.Rangeframe = tk.LabelFrame(self.w, text="Selected Range", height=10, bg='White', width=50, labelanchor='n')
        self.Trainframe = tk.LabelFrame(self.w, text="Train", height=10, bg='White', width=50, labelanchor='n')
        self.Valframe = tk.LabelFrame(self.w, text="Validation", height=10, bg='White', width=50, labelanchor='n')
        self.Testframe = tk.LabelFrame(self.w, text="Test", height=10, bg='White', width=50, labelanchor='n')
        self.autosplitvar = tk.IntVar()
        self.autosplitbutton = tk.Checkbutton(self.w, text='Auto split all files by formats above.', var=self.autosplitvar, onvalue=1, offvalue=0,  bg='White') 

        
        self.CrossFile.grid(row=0, column=0,padx=20,pady=5, ipady=4,sticky=tk.W)
        self.Rangeframe.grid(row=1, column=0,padx=20,pady=5,  ipady=4,sticky=tk.W)
        self.Trainframe.grid(row=2, column=0,padx=20,pady=5,  ipady=4,sticky=tk.W)
        self.Valframe.grid(row=3, column=0,padx=20,pady=5, ipady=4,sticky=tk.W)
        self.Testframe.grid(row=4, column=0,padx=20,pady=5, ipady=4,sticky=tk.W)
        self.autosplitbutton.grid(row=5, column=0, padx=20,ipady=4,sticky=tk.W)
        

        # self.crossFile
        self.FileValue = tk.IntVar() 
        NoneButton = tk.Radiobutton(self.CrossFile, text='None',variable= self.FileValue, value=1, bg= 'White', command = self.kfoldstate) 
        kFoldButton = tk.Radiobutton(self.CrossFile, text='k fold',variable= self.FileValue, value=2, bg= 'White', command = self.kfoldstate)
        NoneButton.grid(row=0, column=0,padx=20,ipady=2,sticky=tk.W)
        kFoldButton.grid(row=1, column=0,padx=20,ipady=2,sticky=tk.W) 
        
            # input k
        tk.Label(self.CrossFile, text="k =", bg= 'White').grid(row=1, column=1,padx=20,ipady=4,sticky=tk.W)
        self.data.kfold= tk.Entry(self.CrossFile) 
        self.data.kfold.grid(row=1, column=2, padx=20,ipady=4,sticky=tk.W)

        # range frame: class onset
        tk.Label(self.Rangeframe, text="Excluded Class", bg= 'White').grid(row=0, column=0,padx=20,ipady=4,sticky=tk.W)
        tk.Label(self.Rangeframe, text="Onset Time(ms)", bg= 'White').grid(row=1, column=0,padx=10,ipady=4,sticky=tk.W)
        self.data.ExcludedClass= tk.Entry(self.Rangeframe) 
        self.data.ExcludedClass.insert(0, 'ex: 1')
        self.data.SelectedOnset= tk.Entry(self.Rangeframe)
        self.data.SelectedOnset.insert(0, 'ex: -100~3000')
      
        self.data.ExcludedClass.grid(row=0, column=1, padx=20,ipady=4,sticky=tk.W)
        self.data.SelectedOnset.grid(row=1, column=1, padx=20,ipady=4,sticky=tk.W)
        

        # data frame: train val test 
        tk.Label(self.Trainframe, text="Choose a file ", bg= 'White').grid(row=0, column=0,padx=20,ipady=2,sticky=tk.W)
        tk.Label(self.Valframe, text="File: ", bg= 'White').grid(row=0, column=0,padx=20,ipady=2,sticky=tk.W)
        tk.Label(self.Valframe, text="Choose a file: ", bg= 'White').grid(row=1, column=0,padx=20,ipady=2,sticky=tk.W)
        tk.Label(self.Valframe, text="Train/Val ratio: ", bg= 'White').grid(row=2, column=0,padx=20,ipady=2,sticky=tk.W)
        tk.Label(self.Testframe, text="File: ", bg= 'White').grid(row=0, column=0,padx=20,ipady=2,sticky=tk.W)
        tk.Label(self.Testframe, text="Choose a file: ", bg= 'White').grid(row=1, column=0,padx=20,ipady=2,sticky=tk.W)
        tk.Label(self.Testframe, text="Train/Test ratio: ", bg= 'White').grid(row=2, column=0,padx=20,ipady=2,sticky=tk.W)

        self.TrainFilesbox = ttk.Combobox(self.Trainframe, values=[file for file in list(self.data.Data.keys())],state="readonly")
        self.ValFilebox = ttk.Combobox(self.Valframe, values=['None','Split from Train set','Choose a file'],state="readonly")
        self.ValFilesbox = ttk.Combobox(self.Valframe, values=[file for file in list(self.data.Data.keys())],state="readonly")
        self.TrainValratiobox= tk.Entry(self.Valframe) 
        self.TestFilebox = ttk.Combobox(self.Testframe, values=['None','Split from Train set', 'Choose a file'],state="readonly")
        self.TestFilesbox = ttk.Combobox(self.Testframe, values=[file for file in list(self.data.Data.keys())],state="readonly")
        self.TrainTestratiobox= tk.Entry(self.Testframe) 
        
        self.TrainFilesbox.grid(row=0, column=1,padx=20,ipady=2,sticky=tk.W)
        self.ValFilebox.grid(row=0, column=1,padx=20,ipady=2,sticky=tk.W)
        self.ValFilesbox.grid(row=1, column=1,padx=20,ipady=2,sticky=tk.W)
        self.TrainValratiobox.grid(row=2, column=1, padx=20,ipady=4,sticky=tk.W)
        self.TestFilebox.grid(row=0, column=1,padx=20,ipady=2,sticky=tk.W)
        self.TestFilesbox.grid(row=1, column=1,padx=20,ipady=2,sticky=tk.W)
        self.TrainTestratiobox.grid(row=2, column=1, padx=20,ipady=4,sticky=tk.W)
        
        self.ValFilebox['state']= 'disabled'
        self.ValFilesbox['state']= 'disabled'
        self.TestFilesbox['state']= 'disabled'
        self.TrainValratiobox['state']= 'disabled'
        self.TrainTestratiobox['state']= 'disabled'

        
        self.ValFilebox.bind('<<ComboboxSelected>>', lambda x :self.state('val'))
        self.TestFilebox.bind('<<ComboboxSelected>>', lambda x : self.state('test'))
        
        tk.Button(self.w, text="Confirm", bg= 'White', command= self.Input2Database).grid(row=6, column=0,padx=150,pady = 10, ipady=2,sticky=tk.W)
        
        
        

    def kfoldstate(self):
        if int(self.FileValue.get()) == 1 : #none
            self.ValFilebox['state']= 'readonly'

        elif int(self.FileValue.get()) == 2 : #kfold
            self.ValFilebox['state']= 'disabled'
           
    def state(self, box):
       
        if box == 'val' :
            if str(self.ValFilebox.get())== 'Choose a file':
                self.ValFilesbox['state']= 'readonly'
                self.TrainValratiobox['state']= 'disable'

            elif str(self.ValFilebox.get())=='Split from Train set':
                self.TrainValratiobox['state']= 'normal'
                self.ValFilesbox['state']= 'disabled'

        elif box == 'test':
            if str(self.TestFilebox.get())== 'Choose a file':
                self.TestFilesbox['state']= 'readonly' 
                self.TrainTestratiobox['state']= 'disable'

            elif str(self.TestFilebox.get())=='Split from Train set':
                self.TrainTestratiobox['state']= 'normal' 
                self.TestFilesbox['state']= 'disable' 
      
                
                
    def Input2Database(self):
        self.data.ExcludedClass= self.CheckEmptyValues(self.data.ExcludedClass)
        self.data.SelectedOnset= self.CheckEmptyValues(self.data.SelectedOnset)
        if self.FileValue.get() ==2:
            self.data.kfold= int(self.CheckEmptyValues(self.data.kfold))
        elif self.FileValue.get()==1:
            self.data.kfold= None
        self.data.autosplit= int(self.autosplitvar.get())
        self.CheckFile('Train')
        self.CheckFile('Val')
        self.CheckFile('Test')

        print('Trainfile: ', self.data.TrainFile)
        print('Valfile: ',self.data.ValFile)
        print('Testfile: ', self.data.TestFile)
        print('TrainValRatio:',self.data.TrainValratio)
        print('TrainTestratio: ',self.data.TrainTestratio)
        print(f'excluded class: {self.data.ExcludedClass}')
        print('kfold: ', self.data.kfold)
        print('autosplit: ', self.data.autosplit)
        self.w.destroy()

        '''Data Sort and Split'''
        DataSortandSplit(self.data)
        
                
    def CheckEmptyValues(self, value):

        #check empty values
        if len(value.get()) != 0:
                temp= str(value.get())
                value= self.CompleteNumber(temp)
                
        else:
                messagebox.showerror("Error",f'You must enter a number.', parent=self.w)
                
        return temp #str
    
    def CompleteNumber(self,string): # for 1~5 -> 1,2,3,4,5
        # if onsetorclass ='onset':
        #     if '~' in string: 
        #         string= string.split('~')
        #         strList = [i for i in range(int(string[0]),int(string[1]))] 
        #         #strList= [sub for sub in self.AllSub if sub >= string[0] and sub <= string[1]]

        if ',' in string:
            
            intList= [int(i) for i in string.split(',')]
            output= intList

        else:
            strList= string
            output= string 
        
        return output # string or intlist

        
    def CheckFile(self, filetype):
        if filetype == 'Train':
            self.data.TrainFile=str(self.TrainFilesbox.get())
            
        if filetype =='Val':
            box = self.ValFilebox
            
            if str(box.get()) == 'Split from Train set':
                self.data.TrainValratio= int(self.TrainValratiobox.get())

            elif str(box.get()) == 'Choose a file':
                self.data.ValFile=str(self.ValFilesbox.get())

        elif filetype =='Test':
            box = self.TestFilebox
            if str(box.get()) == 'Split from Train set':
                self.data.TrainTestratio= int(self.TrainTestratiobox.get())

            elif str(box.get()) == 'Choose a file':
                self.data.TestFile=str(self.TestFilesbox.get())

'''
(almost finished): 需要加入、測試class DataSortandSplit

class CrossSubject_Panel: similar to Individual Panel
- ResetorConfirm(): choose file -> confirm button -> reset button -> rechoose files
- CreateListbox(): create box of listing all files 
- LOSOstate(): 不同cv method -> frame disable/normal
- state(): is identical to functions in Individual_Panel
- Input2Database(): is identical to functions in Individual_Panel

'''
class CrossSubject_Panel:
    def __init__(self,w, Database):
        self.w =w 
        self.data = Database.data

        self.CrossFile = tk.LabelFrame(self.w, text="Cross Validation File", height=150, bg='White', width=200, labelanchor='n')
        self.Rangeframe = tk.LabelFrame(self.w, text="Selected Range", height=150, bg='White', width=200, labelanchor='n')
        self.Trainframe = tk.LabelFrame(self.w, text="Train", height=150, bg='White', width=200, labelanchor='n')
        self.Valframe = tk.LabelFrame(self.w, text="Validation", height=150, bg='White', width=200, labelanchor='n')
        self.Testframe = tk.LabelFrame(self.w, text="Test", height=150, bg='White', width=200, labelanchor='n')
        self.autosplitvar = tk.IntVar()
        self.autosplitbutton = tk.Checkbutton(self.w, text='Auto split all files by formats above.',var=self.autosplitvar, onvalue=1, offvalue=0,  bg='White') 
        
        self.CrossFile.grid(row=0, column=0,padx=10,pady=5, ipady=4,sticky='w')
        self.Rangeframe.grid(row=0, column=1,padx=10,pady=5,  ipady=4,sticky='w')
        self.Trainframe.grid(row=1, column=0,padx=10,pady=5,  ipady=4,sticky='w')
        self.Valframe.grid(row=1, column=1,padx=10,pady=5, ipady=4,sticky='w')
        self.Testframe.grid(row=1, column=2,padx=10,pady=5, ipady=4,sticky='w')
        self.autosplitbutton.grid(row=2, column=0,columnspan=2,padx=10,ipady=4,sticky='w')
        tk.Button(self.w, text="Confirm", bg= 'White', command=self.Input2Database).grid(row=3, column=1,padx=15,pady = 10, ipady=2,sticky=tk.W)

        '''crossfile frame'''
        self.FileValue = tk.IntVar() 
        NoneButton = tk.Radiobutton(self.CrossFile, text='None',variable= self.FileValue, value=1, bg= 'White', command = self.LOSOstate) 
        LOSOButton = tk.Radiobutton(self.CrossFile, text='Leave-one-subject-out',variable= self.FileValue, value=2, bg= 'White', command = self.LOSOstate)
        NoneButton.grid(row=0, column=0,padx=20,ipady=2,sticky=tk.W)
        LOSOButton.grid(row=1, column=0,padx=20,ipady=2,sticky=tk.W) 
        
        '''rangeframe'''
        tk.Label(self.Rangeframe, text="Excluded Class", bg= 'White').grid(row=0, column=0,padx=10,ipady=4,sticky=tk.W)
        tk.Label(self.Rangeframe, text="Onset Time(ms)", bg= 'White').grid(row=1, column=0,padx=10,ipady=4,sticky=tk.W)
        self.data.ExcludedClass= tk.Entry(self.Rangeframe) 
        self.data.ExcludedClass.insert(0, 'ex: 1')
        self.data.SelectedOnset= tk.Entry(self.Rangeframe)
        self.data.SelectedOnset.insert(0, 'ex: -100~3000')
      
        self.data.ExcludedClass.grid(row=0, column=1, padx=10,ipady=4,sticky=tk.W)
        self.data.SelectedOnset.grid(row=1, column=1, padx=10,ipady=4,sticky=tk.W)
        

        ''' frame of train/val/test'''
        self.files= ['S01_1.set', 'S01_2.set']

        '''Trainframe'''
        tk.Label(self.Trainframe, text="Choose files ", bg= 'White').grid(row=0, column=0,padx=10,ipady=2,sticky=tk.W)
        #box
        self.TrainFilesbox= self.CreateListbox(self.Trainframe, self.files, row=1)
        self.TrainFilesbox.grid(row=1, column=0,rowspan=2,columnspan=2, padx=10,ipady=4,sticky=tk.W)
        self.TrainFilesbox['state']= 'disabled'
        
        #button
        self.TrainConfirmButton= tk.Button(self.Trainframe, text="Confirm", bg= 'White', command=lambda:self.ResetorConfirm(self.TrainFilesbox, 'Train', reset=False))
        self.TrainResetButton= tk.Button(self.Trainframe, text="Reset", bg= 'White', command=lambda:self.ResetorConfirm(self.TrainFilesbox,'Train', reset= True))
        self.TrainConfirmButton.grid(row=3, column=0,padx=10,pady = 5, ipady=2,sticky=tk.W)
        self.TrainResetButton.grid(row=3, column=1,padx=5,pady = 5, ipady=2,sticky=tk.W)

        '''valframe'''
        tk.Label(self.Valframe, text="File: ", bg= 'White').grid(row=0, column=0,padx=10,ipady=2,sticky=tk.W)
        tk.Label(self.Valframe, text="Train/Val ratio: ", bg= 'White').grid(row=1, column=0,padx=10,ipady=2,sticky=tk.W)
        tk.Label(self.Valframe, text="Choose files: ", bg= 'White').grid(row=2, column=0,padx=10,ipady=2,sticky=tk.W)
        #box
        self.ValFilebox = ttk.Combobox(self.Valframe, values=['None','Split from Train set','Choose a file'])
        self.ValFilesbox= self.CreateListbox(self.Valframe, self.files, row=3 )
        self.TrainValratiobox= tk.Entry(self.Valframe)

        self.ValFilebox.grid(row=0, column=1,padx=10,ipady=2,sticky=tk.W)
        self.TrainValratiobox.grid(row=1, column=1, padx=10,ipady=4,sticky=tk.W)
        self.ValFilesbox.grid(row=2, column=1,rowspan=2,columnspan=2,padx=10,ipady=2,sticky=tk.W)
        self.ValFilebox['state']='disabled'
        self.ValFilesbox['state']='disabled'
        self.TrainValratiobox['state']='disabled'
        self.ValFilebox.bind('<<ComboboxSelected>>', lambda x :self.state('val'))

        #button
        self.ValConfirmButton= tk.Button(self.Valframe, text="Confirm", bg= 'White', command=lambda:self.ResetorConfirm(self.ValFilesbox, 'Val', reset=False))
        self.ValResetButton= tk.Button(self.Valframe, text="Reset", bg= 'White', command=lambda:self.ResetorConfirm(self.ValFilesbox,'Val', reset= True))
        self.ValConfirmButton.grid(row=5, column=1,padx=10,pady = 5, ipady=2,sticky=tk.W)
        self.ValResetButton.grid(row=5, column=2,padx=0,pady = 5, ipady=2,sticky=tk.W)
      

        

        '''Testframe'''
        tk.Label(self.Testframe, text="File: ", bg= 'White').grid(row=0, column=0,padx=10,ipady=2,sticky=tk.W)
        tk.Label(self.Testframe, text="Train/Test ratio: ", bg= 'White').grid(row=1, column=0,padx=10,ipady=2,sticky=tk.W)
        tk.Label(self.Testframe, text="Choose files: ", bg= 'White').grid(row=2, column=0,padx=10,ipady=2,sticky=tk.W)
        
        #box
        self.TestFilebox = ttk.Combobox(self.Testframe, values=['None','Split from Train set', 'Choose a file'])
        self.TestFilesbox= self.CreateListbox(self.Testframe, self.files, row=2)
        self.TrainTestratiobox= tk.Entry(self.Testframe) 

        self.TestFilebox.grid(row=0, column=1,padx=10,ipady=2,sticky=tk.W)
        self.TrainTestratiobox.grid(row=1, column=1, padx=10,ipady=4,sticky=tk.W)
        self.TestFilesbox.grid(row=2, column=1,rowspan=2,columnspan=2, padx=10,ipady=2,sticky=tk.W)
        self.TestFilebox.bind('<<ComboboxSelected>>', lambda x : self.state('test'))

        self.TestFilebox['state']='disabled'
        self.TestFilesbox['state']='disabled'
        self.TrainTestratiobox['state']= 'disabled'

        #button
        self.TestConfirmButton= tk.Button(self.Testframe, text="Confirm", bg= 'White', command=lambda:self.ResetorConfirm(self.TestFilesbox, 'Test', reset=False))
        self.TestResetButton= tk.Button(self.Testframe, text="Reset", bg= 'White', command=lambda:self.ResetorConfirm(self.TestFilesbox,'Test', reset= True))
        self.TestConfirmButton.grid(row=4, column=1,padx=10,pady = 5, ipady=2,sticky=tk.W)
        self.TestResetButton.grid(row=4, column=2,padx=5,pady = 5, ipady=2,sticky=tk.W)
       
    def ResetorConfirm(self,box,filetype, reset):
        if reset ==False:
            box['state']= 'disabled'
            
            if filetype == 'Train':
                self.data.TrainFile= [self.files[idx] for idx in box.curselection()]
                self.TrainConfirmButton['state']= 'disabled'
                self.TrainResetButton['state']= 'normal'
                print(self.data.TrainFile)
            elif filetype =='Val':
                self.data.ValFile= box.curselection()
                self.ValConfirmButton['state']= 'disabled'
                self.ValResetButton['state']= 'normal'
                
            elif filetype == 'Test':
                self.data.TestFile= box.curselection()
                self.TestConfirmButton['state']= 'disabled'
                self.TestResetButton['state']= 'normal'
        else:
            box['state']= 'normal'

            if filetype == 'Train':
                self.data.TrainFile= None
                print(self.data.TrainFile)
                self.TrainConfirmButton['state']= 'normal'
                self.TrainResetButton['state']= 'disabled'
            elif filetype =='Val':
                self.data.ValFile= None
                self.ValConfirmButton['state']= 'normal'
                self.ValResetButton['state']= 'disabled'
            elif filetype == 'Test':
                self.data.TestFile= None
                self.TestConfirmButton['state']= 'normal'
                self.TestResetButton['state']= 'disabled'
        
    def CreateListbox(self, frame, files, row):
        box = tk.Listbox(frame, selectmode=tk.EXTENDED)
        [box.insert(tk.END, file) for file in files]

        sb = tk.Scrollbar(frame, orient=tk.VERTICAL)
        sb.grid(row=row,column=2,sticky=tk.N+tk.S+tk.W)
        box.config(yscrollcommand=sb.set)
        sb.config(command=box.yview)

        return box
    
    def LOSOstate(self):
        if int(self.FileValue.get()) == 1 : #none
           self.TrainFilesbox['state']= 'normal'
           self.ValFilebox['state']='readonly'
           self.TestFilebox['state']='readonly'
        
           self.TrainConfirmButton['state']= 'normal'
           self.ValConfirmButton['state']= 'normal'
           self.TestConfirmButton['state']= 'normal'
           

        elif int(self.FileValue.get()) == 2 : #LOSO
            self.TrainFilesbox['state']= 'disabled'
            self.ValFilebox['state']='disabled'
            self.ValFilesbox['state']='disabled'
            self.TrainValratiobox['state']='disabled' 
            self.TestFilebox['state']='disabled'
            self.TestFilesbox['state']='disabled'
            self.TrainTestratiobox['state']= 'disabled'

            self.TrainConfirmButton['state']= 'disabled'
            self.TrainResetButton['state']= 'disabled'
            self.ValConfirmButton['state']= 'disabled'
            self.ValResetButton['state']= 'disabled'
            self.TestConfirmButton['state']= 'disabled'
            self.TestResetButton['state']= 'disabled'

    def state(self, box):
        
        if box == 'val' :
            if str(self.ValFilebox.get())== 'Choose a file':
                self.ValFilesbox['state']= 'normal'
                self.TrainValratiobox['state']= 'disable'

            elif str(self.ValFilebox.get())=='Split from Train set':
                self.TrainValratiobox['state']= 'normal'
                self.ValFilesbox['state']= 'disabled'

        elif box == 'test':
            if str(self.TestFilebox.get())== 'Choose a file':
                self.TestFilesbox['state']= 'normal' 
                self.TrainTestratiobox['state']= 'disable'

            elif str(self.TestFilebox.get())=='Split from Train set':
                self.TrainTestratiobox['state']= 'normal' 
                self.TestFilesbox['state']= 'disable' 
      
    def Input2Database(self):
        self.data.ExcludedClass= self.CheckEmptyValues(self.data.ExcludedClass)
        self.data.SelectedOnset= self.CheckEmptyValues(self.data.SelectedOnset)
        self.data.autosplit= int(self.autosplitvar.get())
        self.CheckFile('Train')
        self.CheckFile('Val')
        self.CheckFile('Test')

        print('cv method: ', self.FileValue.get()) # 1> self defined 2> LOSO
        print('Trainfile: ', self.data.TrainFile)
        print('Valfile: ',self.data.ValFile)
        print('Testfile: ', self.data.TestFile)
        print('TrainValRatio:',self.data.TrainValratio)
        print('TrainTestratio: ',self.data.TrainTestratio)
        print(f'excluded class: {self.data.ExcludedClass}')
        print('autosplit: ', self.data.autosplit)
        self.w.destroy()

        # '''Data Sort and Split'''
        # DataSortandSplit(self.data)
    
    def CheckFile(self, filetype):
        if filetype == 'Train':
            self.data.TrainFile=self.data.TrainFile
            
        if filetype =='Val':
            box = self.ValFilebox
            
            if str(box.get()) == 'Split from Train set':
                self.data.TrainValratio= int(self.TrainValratiobox.get())

            elif str(box.get()) == 'Choose a file':
                self.data.ValFile=self.data.ValFile

        elif filetype =='Test':
            box = self.TestFilebox
            if str(box.get()) == 'Split from Train set':
                self.data.TrainTestratio= int(self.TrainTestratiobox.get())

            elif str(box.get()) == 'Choose a file':
                self.data.TestFile= self.data.TestFile

    def CheckEmptyValues(self, value):

        #check empty values
        if len(value.get()) != 0:
                temp= str(value.get())
                value= self.CompleteNumber(temp)
                
        else:
                messagebox.showerror("Error",f'You must enter a number.', parent=self.w)
                
        return temp #str
    
    def CompleteNumber(self,string): # for 1~5 -> 1,2,3,4,5
        # if onsetorclass ='onset':
        #     if '~' in string: 
        #         string= string.split('~')
        #         strList = [i for i in range(int(string[0]),int(string[1]))] 
        #         #strList= [sub for sub in self.AllSub if sub >= string[0] and sub <= string[1]]

        if ',' in string:
            
            intList= [int(i) for i in string.split(',')]
            output= intList

        else:
            strList= string
            output= string 
        
        return output # string or intlist            

'''
(finished)
class Load_Structure_Panel
- ExecModel(): 
1. get values of sf, tp, n_class
2. get model structure from models.py
3. display model info on dashboard 
'''
class Load_Structure_Panel:
    def __init__(self, database, modelframe, filemenu, modelmenu):
 
        self.database= database
        self.modelframe= modelframe
        self.filemenu= filemenu
        self.modelmenu= modelmenu
        self.w=new_window(Title='Load model structure', size='500x200', x_pad=-10, y_pad=220, database=self.database)
        self.modelist = ttk.Combobox(self.w,
                        values=['SCCNet',
                                'EEGNet',
                                'ShallowConvNet',
                                ],
                        state="readonly"
                )

        Confirm = ttk.Button(self.w ,text="Confirm", command=(self.ExecModel))
        self.modelist.pack()
        Confirm.pack()
    
    def ExecModel(self):
        
        from models import EEGNet, ShallowConvNet, SCCNet
        '''get entry values'''
        fnames=list(self.database.data.Data.keys())
        self.database.set_var.n_ch=len(self.database.data.Data[fnames[0]].ch_names)
        self.database.set_var.sf= self.CheckEmptyValues(self.database.set_var.sf)
        self.database.set_var.tp= self.CheckEmptyValues(self.database.set_var.tp)
        
        
        '''exec models'''
        name = self.modelist.get()
        #exec(open('G:/我的雲端硬碟/109_2 course/Project/ExBrainable/ExBrainable/ReviseWithClass/models.py').read(), globals()) #put all variable to globals()
        self.database.model.net= eval(str(name+'(self.database)'))

        '''display info on dashboard'''
        print(self.database.model.net)
        tk.Label(self.modelframe, text=name, bg= 'White').grid(row=0, column=1,  sticky=tk.W ) 
        self.filemenu.entryconfig("Load Model Weight", state= 'normal')
        self.modelmenu.entryconfig("Training Setting", state="normal")
        
        self.w.destroy()

    def CheckEmptyValues(self, value):

        #check empty values
        if len(value.get()) != 0:
                temp= int(value.get())
                
        else:
                messagebox.showerror("Error",f'You must enter a number.', parent=self.w)
                
        return temp #str

class Load_Weight_Panel():
    def __init__(self):
        pass
'''
(finished)
class TrainingSetting_Panel:
- save_weight_folder()
- Input2database(): store entry variables to database 
'''
class TrainingSetting_Panel:
    def __init__(self, database, modelframe):
        self.database= database
        self.modelframe= modelframe
        #self.Trainmenu= Trainmenu

        self.w=new_window(Title='Training Setting ', size='500x200', x_pad=-10, y_pad=180, database= self.database)
        #tk.Label(self.w, text="Validation split :　", bg= 'White').grid(row=0,padx=20,ipady=4,  sticky=tk.W)
        tk.Label(self.w, text="Batch Size :　", bg= 'White').grid(row=1,padx=20,ipady=4,  sticky=tk.W)
        tk.Label(self.w, text="Epoch :　", bg= 'White').grid(row=2, column=0, padx=20,ipady=4,  sticky=tk.W)
        tk.Label(self.w, text="Learning Rate :　", bg= 'White').grid(row=3, column=0, padx=20,ipady=4,  sticky=tk.W)
        tk.Label(self.w, text="Save Weight to : 　", bg= 'White').grid(row=4,column=0, padx=20,ipady=4,  sticky=tk.W)
        
        #self.Valratio = tk.Entry(self.w)
        self.Batchsize = tk.Entry(self.w)
        self.Epoch = tk.Entry(self.w)
        self.Lr = tk.Entry(self.w)
        self.Saveweight = tk.Entry(self.w)

        #self.Valratio.grid(row=0, column=1)
        self.Batchsize.grid(row=1, column=1)
        self.Epoch.grid(row=2, column=1)
        self.Lr.grid(row=3, column=1)
        self.Saveweight.grid(row=4, column=1)
        ttk.Button(self.w, text="Folder", command=(self.save_weight_folder), width=10).grid(row=4,column=2)
        ttk.Button(self.w ,text="Confirm", command=(self.Input2database), width=10).grid(row=6, column=1)

    def save_weight_folder(self):
        #global shortfolder
        folder= tk.filedialog.askdirectory()
        self.shortfolder= "/".join(folder.split('/')[-3:])
        self.Saveweight.insert(tk.END, folder)
        self.database.set_var.saveweightfolder= folder    


    def Input2database(self):

        #self.database.set_var.val_ratio= float(self.Valratio.get())
        self.database.set_var.bs= int(self.Batchsize.get())
        self.database.set_var.epochs= int(self.Epoch.get())
        self.database.set_var.lr= float(self.Lr.get())

        self.w.destroy()

        '''display on dashboard'''
        #tk.Label(self.modelframe, text= self.database.set_var.val_ratio, bg= 'White').grid(row=2, column=1,  sticky=tk.W )
        tk.Label(self.modelframe, text= self.database.set_var.bs, bg= 'White').grid(row=3, column=1,  sticky=tk.W )
        tk.Label(self.modelframe, text= self.database.set_var.epochs, bg= 'White').grid(row=4, column=1 ,  sticky=tk.W)
        tk.Label(self.modelframe, text= self.database.set_var.lr, bg= 'White').grid(row=5, column=1,  sticky=tk.W)
        tk.Label(self.modelframe, textvariable= self.shortfolder , bg= 'White').grid(row=6, column=1,  sticky=tk.W)

        '''enable model training button'''
        #self.Trainmenu.entryconfig("Model Training", state="normal")

class Training_Panel():
    def __init__(self):
        pass



class Predicted_Panel():
    def __init__(self):
        pass



class Performance_Panel():
    def __init__(self):
        pass



class Visualization_Panel():
    def __init__(self):
        pass