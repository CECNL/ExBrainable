# Authors: Ya-Lin Huang <yalinhuang.bt06@nycu.edu.tw>
#          Chia-Ying Hsieh <irishsieh0720.cs07@nycu.edu.tw>


from models import * 
import scheme_var

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import signal
from scipy.fft import fft, fftfreq
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import ACTIVE
import torch
import torch.nn as nn
import mne
from sklearn.metrics import confusion_matrix



def new_window(Title, size, x_pad, y_pad):
    win_main_x = scheme_var.win_main.winfo_rootx()+ x_pad
    win_main_y = scheme_var.win_main.winfo_rooty()+ y_pad

    newindow= tk.Toplevel()
    newindow.geometry(size)
    newindow.geometry(f'+{win_main_x}+{win_main_y}')  
    newindow.title(Title)
    newindow.configure(background='White')
    newindow.wm_attributes('-topmost', True)
    
    return newindow

def get_weight(filepath):
    global conv1, conv2
    net= SCCNet()
    weights= torch.load(filepath, map_location= torch.device('cpu'))
#     for weight in weights:
#         if 'weight' in weight:
#             print(f'{weight}: {weights[weight].shape}')

    #spatial ((kernelsize),n_kernel,1)
    conv1= weights['conv1.weight'].detach().cpu().numpy().squeeze()

    #temporal (n_kernel, inputnode  ,kernelsize)
    conv2= weights['conv2.weight'].detach().cpu().numpy().squeeze()
    conv2= conv2.reshape(20*22,12) 
    
    return conv1,conv2

def montage_select(modelframe, Montagename):
    w = new_window('montage selection', '500x200', x_pad=-8, y_pad=150 )
    stdmontagelist = ttk.Combobox(w,
                    values=["BCI_IV 2a",  # only for test 
                            "standard_1005", 
                            "standard_1020",
                            "standard_1020_32ch",
                            "standard_alphabetic",
                            "standard_postfixed",
                            "standard_prefixed",
                            "standard_primed",
                            "biosemi16",
                            "biosemi32",
                            "biosemi64",
                            "biosemi128",
                            "biosemi256",
                            "easycap-M1",
                            "easycap-M10",
                            "EGI_256",
                            "GSN-HydroCel-32",
                            "GSN-HydroCel-64_1.0",
                            "GSN-HydroCel-65_1.0",
                            "GSN-HydroCel-128",
                            "GSN-HydroCel-129",
                            "GSN-HydroCel-256",
                            "GSN-HydroCel-257",
                            "mgh60",
                            "mgh70",
                            "artinis-octamon",
                            "artinis-brite23"
                            ],
                    state="readonly"
            )
    
  
    Confirm = ttk.Button(w ,text="Confirm", command=(lambda:[channel_select(w,modelframe, stdmontagelist, Montagename)]))
    stdmontagelist.pack()
    Confirm.pack()



def channel_select(w,modelframe, stdmontagelist, Montagename):
    name = stdmontagelist.get()
    print(name)
    if name== 'BCI_IV 2a':
        montage= mne.channels.make_standard_montage("standard_1020")
        chs=['Fz', 'FC3', 'FC1','FCz', 'FC2','FC4',
             'C5','C3','C1','Cz','C2','C4','C6',
             'CP3','CP1','CPz','CP2','CP4',
             'P1','Pz','P2','POz']
          
    elif name== 'standard_1020_32ch':
        montage= mne.channels.make_standard_montage("standard_1020")
        chs= ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8',
              'A1','T3','C3','Cz','C4', 'T4', 'A2',
              'T5', 'P3', 'Pz','P4','T6','O1','O2']
    else:
        montage= mne.channels.make_standard_montage(name)
        chs = list(montage.get_positions()['ch_pos'].keys())
        print(chs)

    w.destroy()

    w2 = new_window('Channel selection', '500x300', x_pad=-8, y_pad=150)
    chlist = tk.Listbox(w2, selectmode=tk.EXTENDED)
    for c in chs:
        chlist.insert(tk.END, c)

    Confirm = ttk.Button(w2 ,text="Confirm", command=(lambda:select_ch(w2, modelframe, name, chlist,montage, Montagename)))

    chlist.pack()
    Confirm.pack()


def select_ch(w2, modelframe, name, chlist,montage, Montagename):
    
    ch_select = chlist.curselection()
    electrode = []
    for c in ch_select:
        electrode.append(chlist.get(c))
    print(electrode)

    #scheme_var.montage = montage
    #scheme_var.electrode= electrode
    Montagename.set(name)
    tk.Label(modelframe, textvariable= Montagename).grid(row=11, column=1, sticky=tk.W)
    w2.destroy()
    Spatial_kernel(montage, electrode)

def Spatial_kernel(montage, electrode):
     
    montage= montage.get_positions()['ch_pos']
    position= [montage[i] for i in electrode]
    position= np.asarray(position)
    pos_count = len(position)


    fig, axes = plt.subplots(5, int(np.ceil(pos_count/5)), figsize=(5, 5))
    for i in range(int(5*np.ceil(pos_count/5))):
        if i < pos_count:
            print(conv1[:i].squeeze().shape)
            mne.viz.plot_topomap(data=conv1[:,i].squeeze(),
                                pos=position[:,0:2],
                                axes= axes[int(i/5), i%5],
                                show=False,
                                mask=np.ones((pos_count,), dtype=bool),
                                mask_params= dict(marker='o', markerfacecolor='black', markersize=1.5))
            axes[int(i/5), i%5].set_title(f'Kernel {i+1}', fontweight='bold', fontsize=8)
        else:
            fig.delaxes(axes[int(i/5), i%5])

    fig.subplots_adjust(top=0.85)
    fig.suptitle("Spatial Pattern", fontsize=11, fontweight='bold')
    fig.tight_layout()

    plt.show()

                
def plot_mag():
    N = 12
    T = 1.0 / scheme_var.sf
    
    freq = np.unique(np.round(abs(fftfreq(N, d=T)),1)) 
    y = conv2                                                 
    y_pad = np.pad(y, pad_width = [(0,0),(0,1200-12)], mode='constant') # (440, 1100) 
    y_pad = np.log10(abs(fft(y_pad))**2)  
    y_pad = y_pad[y_pad.argmax(1).argsort()]                 
    y_pad = y_pad[:,0:int(y_pad.shape[1]/2)]                 

    fig= plt.figure()
    subplot = fig.add_subplot(111)
    subplot.set_xlabel('Frequency (Hz)')
    subplot.set_ylabel('Kernel')
    subplot.set_title(f'Temporal Pattern')
    ticks_location = [0, 100,200,300,400,500,599]
    subplot.set_xticks(ticks_location)
    subplot.set_xticklabels(freq)
    
    img= subplot.imshow(y_pad, vmin= None, vmax= None)
    fig.colorbar(img)
    fig.tight_layout()
    
    plt.show()


def Confusion_Matrix(w, y_true, y_pred):
    cm= confusion_matrix(y_true, y_pred, normalize='true')

    figure = Figure(figsize=(5,4))
    ax = figure.add_subplot(1, 1, 1)
    cm = cm.astype("float")/cm.sum(axis=1)[:,np.newaxis]

    im=ax.imshow(cm, cmap=plt.cm.Blues)
    ax.set_title("Confusion matrix")
    figure.colorbar(im)

    ax.set_xticks(np.arange(scheme_var.n_class))
    ax.set_yticks(np.arange(scheme_var.n_class))
    ax.set_ylim(len(cm) - 0.5, -0.5)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(x=j, y=i, s=("%.2f"%cm[i][j]), va='center', ha='center')

    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')

    canvas = FigureCanvasTkAgg(figure, w)
    canvas.get_tk_widget().pack(side=tk.RIGHT)