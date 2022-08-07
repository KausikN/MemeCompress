"""
Dataset Utils for Data_7000 Dataset

Expected Files in Dataset Folder:
    - data_7000/                    :  All images of codes are saved in this folder
    - data_7000.csv                 :  A list of all codes only
"""

# Imports
import os
import cv2
import zipfile
import functools
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt

# Main Vars
DATASET_PATH = "Data/Datasets/Data_7000/Data_7000/"
DATASET_ITEMPATHS = {
    "images": "data_7000/",
    "labels": "data_7000.csv"
}
DATASET_LABELS = {
    "ImageName": "path", # Keep this as "path" always
    # "Link": "link", "Text1": "text_1", "Text2": "text_2", 
    "FunnyLabel": "funny", "SarcasticCategory": "sarcastic", "OffenseCategory": "offensive", 
    "MotivationCategory": "motivation", "PositivityCategory": "positive"
}

# Main Functions
# Load Functions
def DatasetUtils_LoadCSV(path):
    '''
    DatasetUtils - Load CSV
    '''
    return pd.read_csv(path)

# Extract Functions
def DatasetUtils_ExtractZIPDataset(path, save_path=None, **params):
    '''
    DatasetUtils - Extract the Zipped Dataset
    '''
    # Set same dir if save_path is not specified
    if save_path is None:
        save_path = os.path.dirname(path)
    # Extract
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(save_path)

# Dataset Functions
def DatasetUtils_LoadDataset(path=DATASET_PATH, N=-1, **params):
    '''
    DatasetUtils - Load Dataset
    Pandas Dataframe with columns as in DATASET_LABELS
    '''
    # Get Dataset Labels
    dataset_info = DatasetUtils_LoadCSV(os.path.join(path, DATASET_ITEMPATHS["labels"]))
    # Take N range
    if type(N) == int:
        if N > 0: dataset_info = dataset_info.head(N)
    elif type(N) == list:
        if len(N) == 2: dataset_info = dataset_info.iloc[N[0]:N[1]]
    # Reset Columns
    dropCols = [c for c in dataset_info.columns if c not in DATASET_LABELS.keys()]
    dataset_info.drop(dropCols, axis=1, inplace=True)
    dataset_info.columns = [DATASET_LABELS[c] for c in dataset_info.columns]
    # Add Main Path
    dataset_info["path"] = dataset_info["path"].apply(lambda x: os.path.join(path, DATASET_ITEMPATHS["images"], x))

    return dataset_info

# Main Vars
DATASET_FUNCS = {
    "full": DatasetUtils_LoadDataset
}