"""
Dataset
"""

# Imports
from .Utils import *
from .DatasetUtils import *

# Main Vars
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".pneg", ".bmp", ".tiff"]

# Main Functions
# Load Functions
def Dataset_LoadImage(path):
    '''
    Dataset - Load Image from path in dataset
    '''
    try:
        # Load Image
        I = cv2.imread(path)
        I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
        I = np.array(I, dtype=float)
        # Convert range to [0, 1]
        I = I / 255.0
    except Exception as e:
        I = None

    return I

# Dataset Generator Functions
def DatasetGenerator_Simple(dataset, batch_size=1, **params):
    '''
    DatasetGenerator - Simple
    '''
    N = dataset.shape[0]
    for i in range(0, N, batch_size):
        start, end = i, min(i+batch_size, N)
        dataset_subset = dataset.iloc[start:end, :]
        dataset_Is = dataset_subset["path"].apply(Dataset_LoadImage)
        yield dataset_Is, dataset_subset
        
# Dataset Functions
def Dataset_LoadSamples(
    path=DATASET_PATH, N=-1, 
    batch_size=1,
    **params
    ):
    '''
    Dataset - Load Dataset Samples
    '''
    # Load Dataset
    dataset_labels = DATASET_FUNCS["full"](path=path, N=N, **params)
    # Create Generator
    dataset_generator = DatasetGenerator_Simple(dataset_labels, batch_size=batch_size)

    return dataset_generator