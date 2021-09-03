import numpy as np

# x,y from mne input -> use xy_data function retrun correct format xy data -> main( xy data )
def confirm_xy_size(x_train, y_train, x_test, y_test): #numpy array (n_trials, n_chs, n_times) (n_trials,1)
    #xy 
    if not ((len(x_train.shape)==3) and (len(y_train.shape)==2)) and ((len(x_test.shape)==3) and (len(y_test.shape)==2)):
        raise ValueError ('shape of x or y is not correct.')

    if not (x_train.shape[0]== y_train.shape[0]) and (x_test.shape[0]== y_test.shape[0]) :
        raise ValueError (f'numbers of trials of x and y have to be the same length.')
    
    #train test 
    text=['trials', 'channels', 'timepoints']
    for i, j in enumerate(text): 
        if not (x_train.shape[i]== x_test.shape[i]) :
         raise ValueError (f'Numbers of {j} of x and y have to be the same length.')

    return x_train, y_train, x_test, y_test