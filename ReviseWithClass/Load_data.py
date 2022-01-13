import tkinter as tk
from tkinter.constants import ANCHOR
import tkinter.ttk as ttk
from typing_extensions import IntVar
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
        ###database 
        self.Database={}

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

        text= ['Model', 'Sampliing Rate', 'Validation Split', 'Batch Size', 'Epoch',\
               'Learning Rate', 'Save Model Weight','Pretrained Model Weight',\
               'Training Time (sec)' ,'Trainable Parameters','Memory Size (MB)','EEG Montage'  ]
        for row, rowtext in enumerate(text):
            tk.Label(modelframe, text=f"{rowtext} :　", bg= 'White').grid(row=row, column=0, ipady=4, padx=20, sticky=tk.W)
        
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
        filemenu.add_command(label='Study(cross subject)', command=lambda:LoadFileMenu(self.Database))
        self.w_main.config(menu= menubar)
        





class LoadFileMenu():
    def __init__(self, Database):
        LoadDataPanel(Panel, Database)


class LoadDataPanel():
    def __init__(self,Panel, Database):
        
        self.w= Panel(Title='Load Data Files', size='500x450', x_pad=-10, y_pad=10)
        self.xframes = tk.LabelFrame(self.w, text="Data", height=10, bg='White', width=50, labelanchor='n')
        self.yframes = tk.LabelFrame(self.w, text="Labels", height=10, bg='White', width=50, labelanchor='n')
        self.xframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        self.yframes.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        
        ttk.Button(self.xframes, text='Add Files', command=(lambda : self.AllFiles('x',  Database)), width=10).pack()
        ttk.Button(self.yframes, text='Add Files', command=(lambda : self.AllFiles('y',  Database)), width=10).pack()
        ttk.Button(self.w ,text="Confirm", command=(lambda:self.RenameEvents(self.w, Database)), width=10).pack()

        
    def AllFiles(self, xory,  Database):

        if xory == 'x':
            frame= self.xframes
        if xory == 'y':
            frame= self.yframes
            

        files = filedialog.askopenfilenames()
        Path, Data, Eventids ={},{},{}
        
        for index, path in enumerate(files):
            Path[f'path_{index}']= path
            Data[f'data_{index}'], Eventids[f'eventid_{index}']= self.ReadFiles(path)
            #skip concat data 
            tk.Label(frame, text= path.split('/')[-1], bg='White').pack(fill='both',padx=20)

        Database[f'{xory}data']= Data
        Database[f'{xory}path']= Path
        Database[f'eventids']= Eventids
        

    def ReadFiles(self,path):
        try:    
            if '.set' in path: 
                data = mne.io.read_epochs_eeglab(path, uint16_codec='latin1')  
                print(data.event_id)

            if '.edf' in path: 
                data= mne.io.read_raw_edf(path,preload= True) 
            
            return data, data.event_id

        except TypeError:
            print('The file format is not supported.')

    
        

    def RenameEvents(self,wdata, Database):
        wdata.destroy()
        w= Panel('Rename Events', '500x250', x_pad=-10, y_pad=180)

        print('len of eventtype', len(self.uniquevent.keys()))
        self.uniquevents(Database)


        table= ttk.Treeview(w, height=len(self.uniquevent.keys()))
        sb = tk.Scrollbar(w, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        table.config(yscrollcommand=sb.set)
        sb.config(command=table.yview)

        table['column']= ['Event ID','Event type']
        table.column('#0', width=0, stretch=tk.NO)
        table.column('Event ID', anchor=tk.CENTER, width=30 )
        table.column('Event type', anchor=tk.CENTER, width=130)
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('Event ID', text='Event ID', anchor=tk.CENTER)
        table.heading('Event type', text='Event type', anchor=tk.CENTER)

        if '.set' in Database['xpath']['path_0']: 
            
            #for row in range(len(uniquevent.keys())):
            for row,(type, id) in enumerate(self.uniquevent.items()):
                #eventypes=list(event_ids.keys())
                print(row, type, id)
                item= table.insert(parent='', index=row, iid= row, text='', values=[id, type])
                table.item(item, tags=item)
        # # if ftype== '.mat':
        # #     global eventype
        # #     eventype= [None]*len(event_ids) # eventype is none default in mat file 
        # #     for row in range(len(event_ids)):
        # #         item= table.insert(parent='', index=row, iid= row, text='', values=[event_ids[row], eventype[row] ])
        # #         table.item(item, tags=item)

        # table.bind('<1>', self.Editname, table)
        # table.pack(side='top', fill='x',padx=10, pady=10)

        #Confirm = ttk.Button(w ,text="Confirm", command=(lambda:SplitData(w)), width=10).pack()
    def uniquevents(self, Database):        
        self.uniquevent={}
        EventFiles= Database['eventids']
        #for index in range(len())
        for fileevent in EventFiles.keys(): #fir each file 
            for eventype in EventFiles[fileevent].keys(): #each event 
                if eventype not in self.uniquevent:
                    self.uniquevent[eventype]= EventFiles[fileevent][eventype] # {'eventype', 'id'}  
    # # def findevents(self,x):
    # #     return {
    # #         #'.set': data.event_id,
    # #         '.mat': event_ids,
    # #     }[x]

    # def Editname(self,event, table):

    #     if table.identify_region(event.x, event.y) == 'cell':
    #         # the user clicked on a cell

    #         def ok(event):
    #             """Change item value."""
    #             #print(entry.get(), type(entry.get()))
    #             if column=='#1':
    #                 event_ids[int(item)]= int(entry.get())
    #             if column=='#2':
    #                 eventype[int(item)]= entry.get()
    #             print(event_ids, eventype)

    #             table.set(item, column, entry.get())
    #             entry.destroy()
            
    #         column = table.identify_column(event.x)  # identify column
    #         item = table.identify_row(event.y)  # identify item
    #         x, y, width, height = table.bbox(item, column) 
    #         value = table.set(item, column)

        
            

    #     elif table.identify_region(event.x, event.y) == 'heading': 
    #         # the user clicked on a heading

    #         def ok(event):
    #             """Change heading text."""
    #             table.heading(column, text=entry.get())
    #             entry.destroy()

    #         column = table.identify_column(event.x) # identify column
    #         # tree.bbox work sonly with items so we have to get the bbox of the heading differently
    #         x, y, width, _ = table.bbox(table.get_children('')[0], column) # get x and width (same as the one of any cell in the column)
    #         # get vertical coordinates (y1, y2)
    #         y2 = y
    #         # get bottom coordinate
    #         while table.identify_region(event.x, y2) != 'heading':  
    #             y2 -= 1
    #         # get top coordinate
    #         y1 = y2
    #         while table.identify_region(event.x, y1) == 'heading':
    #             y1 -= 1
    #         height = y2 - y1
    #         y = y1
    #         value = table.heading(column, 'text')

    #     elif table.identify_region(event.x, event.y) == 'nothing': 
    #         column = table.identify_column(event.x) # identify column
    #         # check whether we are below the last row:
    #         x, y, width, height =table.bbox(table.get_children('')[-1], column)
    #         if event.y > y:

    #             def ok(event):
    #                 """Change item value."""
    #                 # create item
    #                 item = table.insert("", "end", values=("", ""))
    #                 table.set(item, column, entry.get())
    #                 entry.destroy()

    #             y += height
    #             value = ""
    #         else:
    #             return
    #     else:
    #         return
    #     # display the Entry   
    #     entry = ttk.Entry(table)  # create edition entry
    #     entry.place(x=x, y=y, width=width, height=height,
    #                 anchor='nw')  # display entry on top of cell
    #     entry.insert(0, value)  # put former value in entry
    #     entry.bind('<FocusOut>', lambda e: entry.destroy())  
    #     entry.bind('<Return>', ok)  # validate with Enter
    #     entry.focus_set()

    

def Panel(Title, size, x_pad, y_pad):

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