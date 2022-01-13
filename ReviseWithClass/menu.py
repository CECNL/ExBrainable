import tkinter as tk

import panel



class Load_File_Menu():
    def __init__(self, filemenu):
        self.filemenu = filemenu
        self.filemenu.add_command(label='Load Data', command=self.create_load_data_panel)
        self.filemenu.add_command(label='Load Model Weight', command=self.create_load_weight_panel)
        self.filemenu.add_command(label='Study(Cross Subject)')


    def create_load_data_panel(self):
        load_data_panel = panel.Load_Data_Panel()


    def create_load_weight_panel(self):
        load_weight_panel = panel.Load_Weight_Panel()



class Load_Model_Menu():
    def __init__(self, modelmenu):
        self.modelmenu = modelmenu
        self.modelmenu.add_command(label='Model Selection', command=self.create_load_struct_panel)
        self.modelmenu.add_command(label='Training Setting', command=self.create_model_setting_panel)
        self.modelmenu.add_command(label='Model Summary', command=self.create_summary_panel)

    
    def create_summary_panel():
        model_summary_panel = panel.Model_Summary_Panel()

    
    def create_load_struct_panel():
        load_struct_panel = panel.Load_Structure_Panel()

    
    def create_model_setting_panel():
        model_setting_panel = panel.Model_Setting_Panel()




class Training_Menu():
    def __init__(self, trainmenu):
        self.trainmenu = trainmenu
        self.trainmenu.add_command(label='Model Training', command=self.create_training_panel)
    

    def create_training_panel():
        training_panel = panel.Training_Panel()



class Result_Menu():
    def __init__(self, resultmenu):
        self.resultmenu = resultmenu
        self.visualmenu = tk.Menu(self.resultmenu, tearoff=0)
        self.resultmenu.add_command(label='Model Prediction', command=self.create_predicted_panel)
        self.resultmenu.add_command(label='Model Performance', command=self.create_performance_panel)
        self.resultmenu.add_cascade(label='Model Interpretation', menu=self.visualmenu)
        self.visualmenu.add_command(label='Spatial Pattern', command=self.create_visualization_panel)
        self.visualmenu.add_command(label='Temporal Pattern', command=self.create_visualization_panel)


    def create_predicted_panel():
        predicted_panel = panel.Predicted_Panel()


    def create_performance_panel():
        performance_panel = panel.Performance_Panel()


    def create_visualization_panel():
        visualization_panel = panel.Visualization_Panel()





