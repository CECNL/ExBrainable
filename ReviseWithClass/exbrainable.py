import tkinter as tk

import database
import menu



class ExBrainable():
    def __init__(self):
        self.win_main = tk.Tk()
        self.win_main.geometry('500x750')
        self.win_main.title("ExBrainable")
        self.win_main.configure(background='White')
        self.menubar = tk.Menu(self.win_main)
        self.trainframe = tk.LabelFrame(self.win_main, text="Training Data", height=10, bg='White', width=50, labelanchor='n')
        self.modelframe = tk.LabelFrame(self.win_main, text="Model and Training Setting", height=10, bg='White', width=50, labelanchor='n')
        self.testframe = tk.LabelFrame(self.win_main, text="Test Data", height=10, bg='White', width=50, labelanchor='n')


    def execution(self):
        data = database.Database()

        # Construct the ExBrainable Panel
        self.construct_framework()

        # Construct Load File Menu
        filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = 'File ', menu = filemenu)
        load_file_menu = menu.Load_File_Menu(filemenu)

        # Construct Load Model Menu
        modelmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = 'Model', menu = modelmenu)
        load_model_menu = menu.Load_Model_Menu(modelmenu)

        # Construct Training Menu
        trainmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = 'Training', menu = trainmenu)
        training_menu = menu.Training_Menu(trainmenu)

        # Construct Result Menu
        resultmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label = 'Results', menu = resultmenu)
        result_menu = menu.Result_Menu(resultmenu)

        # Create the ExBrainable Panel
        self.win_main.config(menu = self.menubar)
        self.win_main.mainloop()


    def construct_framework(self):
        # Show Training Data Information
        self.trainframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        tk.Label(self.trainframe, text="Train Data (X_train) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.trainframe, text="Train Data size :　", bg= 'White').grid(row=1, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.trainframe, text="Train Label (Y_train) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.trainframe, text="Train Label size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)

        # Show Model and Training Setting
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

        # Show Test Data Information
        self.testframe.pack(fill='both', ipadx=1 ,ipady= 10,padx=20 ,pady= 18)
        tk.Label(self.testframe, text="Test Data(X_test) :　", bg= 'White').grid(row=0, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.testframe, text="Test Data Size :　", bg= 'White').grid(row=1 ,column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.testframe, text="Test Label(Y_test) :  ", bg= 'White').grid(row=2, column=0, ipady=4, padx=20, sticky=tk.W)
        tk.Label(self.testframe, text="Test Label Size :　", bg= 'White').grid(row=3, column=0, ipady=4, padx=20, sticky=tk.W)
