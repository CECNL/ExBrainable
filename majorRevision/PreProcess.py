from contextlib import nullcontext
import json
import string
import tkinter as tk
from tkinter.constants import ANCHOR
import tkinter.ttk as ttk
from tkinter import filedialog
from typing_extensions import IntVar
import numpy as np
import scipy.io
import mne

from LoadData import database

def reference(dataset, base):
    try:
        if isinstance(base, str) and base == 'average': # reference by average
            for key,value in dataset:
                value._data.set_eeg_reference()
        elif isinstance(base, list) and isinstance(base[0], str): # reference by channel names
            for key,value in dataset:
                value._data.set_eeg_reference(base)
        elif isinstance(base, list) and base==[]:
            return
        else:
            raise ValueError('Desired reference should be \'average\' or list of channels')
    except ValueError as e:
        print(repr(e))

def filter(hf=0, lf=0):

    return

def epoching():
    return


# mne.Epochs.crop
# 



