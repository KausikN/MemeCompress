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
def NormaliseToRange(I, val_range=(0, 255)):
    '''
    Normalise an image to a specified range
    '''
    # Init
    I = I.copy()
    # Normalise to [0, 1]
    I = (I - I.min()) / (I.max() - I.min())
    # Normalise to val_range
    I = I * (val_range[1] - val_range[0]) + val_range[0]

    return I