from tkinter import StringVar
from LoadData import *
from Windows import *

w = tk.Tk()
w.title('debug window')
w.geometry('400x400')
var = StringVar()

#ttk.Button(w ,text="select file", command=lambda:[ReadData(),var.set(", ".join(s.split('/')[-1] for s in getInfo('dataset_info.json', 'fileNames')))], width=10).pack(fill='both', padx=20 ,pady=5)

f = FileWin(w)
#tk.Label(w, textvariable=var).pack()
w.mainloop()


