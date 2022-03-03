import tkinter as tk



def new_window(Title, size,x_pad, y_pad, database):
    
    x= database.set_var.win_main_x
    y= database.set_var.win_main_y
    
    win_main_x = x + x_pad
    win_main_y = y + y_pad

    newindow= tk.Toplevel()
    newindow.geometry(size)
    newindow.geometry(f'+{win_main_x}+{win_main_y}')  
    newindow.title(Title)
    newindow.configure(background='White')
    newindow.wm_attributes('-topmost', True)
    
    return newindow