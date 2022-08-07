"""
Utils
"""

# Imports
import os
import cv2
import pickle
import numpy as np
from math import ceil
import matplotlib.pyplot as plt
from tqdm import tqdm
    
# Main Functions
# Normalise Functions
def NormaliseToRange(I, val_range=(0, 255)):
    '''
    Normalise - Normalise an image to a specified range
    '''
    # Init
    I = I.copy()
    # Normalise to [0, 1]
    I = (I - I.min()) / (I.max() - I.min())
    # Normalise to val_range
    I = I * (val_range[1] - val_range[0]) + val_range[0]

    return I

# Resize Functions
def Resize_Simple(I, size):
    '''
    Resize - Simple CV2 Resizing
    '''
    # Resize
    I = cv2.resize(I, tuple(size[:2][::-1]))

    return I

def Resize_Pad(I, size, pad_value=0.0):
    '''
    Resize - Resize preserving original aspect ratio then pad to fit given size
    '''
    # Resize (preserving original aspect ratio)
    aspect_ratio_I = I.shape[1] / I.shape[0]
    aspect_ratio_size = size[1] / size[0]
    size_ar = [0, 0]
    if aspect_ratio_I > aspect_ratio_size:
        size_ar[1] = size[1]
        size_ar[0] = ceil(size[1] / aspect_ratio_I)
    else:
        size_ar[0] = size[0]
        size_ar[1] = ceil(size[0] * aspect_ratio_I)
    I_resized = cv2.resize(I, tuple(size_ar)[::-1])
    # Pad
    I_padded = np.ones(size, dtype=float) * pad_value
    I_padded[:I_resized.shape[0], :I_resized.shape[1]] = I_resized

    return I_padded

# Main Vars
RESIZE_FUNCS = {
    "simple": Resize_Simple,
    "pad": Resize_Pad
}