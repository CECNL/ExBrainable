# dashboard: file, dataset, model, train
from LoadData import *
from PreProcess import  *

def new_window(title="newWindow", size="400x300"):
    newindow= tk.Toplevel()
    newindow.geometry(size) 
    newindow.title(title)
    newindow.configure(bg='White')
    newindow.wm_attributes('-topmost', True)
    
    return newindow

class DashBoard:
    def __init__(self):
        self.DashBoard = tk.Tk()
        self.DashBoard.geometry("500x750")
        self.DashBoard.title("Exbrainable")
        
        # menubar
        # dataset info
        self.DashBoard.mainloop()


        

class FileWin:
    def __init__(self, dashboard):
        self.fnVar = tk.StringVar()
        self.init_var()



        self.window = new_window("Load data")
        tk.Label(self.window, text='dataset name', bg="White").grid(row=0, column=0, padx=0, ipady=0, sticky="w")
        tk.ttk.Separator(self.window, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky='we')
        tk.Label(self.window, text='dataset table heading', bg="White").grid(row=2, column=0, padx=0, ipady=0, sticky="w")
        tk.ttk.Separator(self.window, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='we')

        tk.Label(self.window, text='file name', bg="White").grid(row=4, column=0, padx=0, ipady=0, sticky="w")
        self.fnEntry = tk.Entry(self.window, textvariable=self.fnVar, bg="White").grid(row=4, column=1, padx=0, ipady=0, sticky="w")

        tk.Button(self.window, text="ok", command=self.get_var, width=8).grid(row=4, column=2)
    
    def init_var(self):
        # remove btn
        # filename
        #fn = getInfo('dataset_info.json', "fileNames")
        #fn = [f.split('/')[-1] for f in fn]
        tmp = getInfo('debug.json', "field1")
        tmp = ", ".join(tmp)
        print(tmp)
        self.fnVar.set(tmp)

    def get_var(self):
        tmp = self.fnVar.get()
        tmp = tmp.split(', ')
        print(tmp)
        saveInfo('debug.json', "field1", tmp)
        


       

