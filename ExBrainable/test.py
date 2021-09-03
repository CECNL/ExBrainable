from GUI import main
from datautil import xy

import mne
import numpy as np 
import scipy.io

if __name__ == '__main__':
    x_train= scipy.io.loadmat('G:\我的雲端硬碟/109_2 course/Project/visSCC/GUI/xydata/xtrain.mat')
    y_train= scipy.io.loadmat('G:\我的雲端硬碟/109_2 course/Project/visSCC/GUI/xydata/ytrain.mat')
    x_test= scipy.io.loadmat('G:\我的雲端硬碟/109_2 course/Project/visSCC/GUI/xydata/xtest.mat')
    y_test= scipy.io.loadmat('G:\我的雲端硬碟/109_2 course/Project/visSCC/GUI/xydata/ytest.mat')
    
    x_train= x_train['x_train']
    y_train= y_train['y_train']
    x_test= x_test['x_test']
    y_test= y_test['y_test']
    # epochs = mne.io.read_epochs_eeglab('G:/我的雲端硬碟/109_2 course/BCI/lab3/Day 2_SSVEP.set')
    # x_train=epochs._data
    # y_train = np.ones((100,1))
    # print(x_train.shape, y_train.shape)
    # x_test=epochs._data
    # y_test = np.ones((100,1))

    X_train, Y_train, X_test, Y_test = xy.confirm_xy_size(x_train, y_train, x_test, y_test)

    main(X_train, Y_train, X_test, Y_test)  
