"""
Image Matching Functions
"""

# Imports
from scipy.signal import convolve2d
from .Utils import *

# Main Functions
def ImageMatch_Score_PixelWiseAvgDifference(
    I_query, I_ref, 
    resizeFunc="simple", 
    **params
    ):
    '''
    ImageMatch - Score - PixelWise Average Difference
    '''
    # Resize query image to fit reference image
    resizeFunc = resizeFunc if resizeFunc in RESIZE_FUNCS.keys() else RESIZE_FUNCS["simple"]
    I_query = RESIZE_FUNCS[resizeFunc](I_query, I_ref.shape)
    # Score
    n_vals = np.prod(I_ref.shape)
    score = 1.0 - (np.sum(np.abs(I_query - I_ref)) / n_vals)

    ScoreData = {
        "score": score
    }
    return ScoreData

def ImageMatch_Score_NormCorrelationAvg(
    I_query, I_ref, 
    resizeFunc="simple", 
    grayscale_correlation=True,
    **params
    ):
    '''
    ImageMatch - Score - Normalised Correlation Average
    '''
    # Resize query image to fit reference image
    resizeFunc = resizeFunc if resizeFunc in RESIZE_FUNCS.keys() else RESIZE_FUNCS["simple"]
    I_query = RESIZE_FUNCS[resizeFunc](I_query, I_ref.shape)
    if grayscale_correlation:
        I_query = np.mean(I_query, axis=-1)
        I_ref = np.mean(I_ref, axis=-1)
    # Reshape
    if I_query.ndim == 2: I_query = I_query.reshape((I_query.shape[0], I_query.shape[1], 1))
    if I_ref.ndim == 2: I_ref = I_ref.reshape((I_ref.shape[0], I_ref.shape[1], 1))
    # Score
    
    Is = []
    for d in range(I_ref.shape[2]):
        I_conv = convolve2d(I_query[:, :, d], I_ref[:, :, d], mode="same", boundary="symm")
        Is.append(I_conv)
    I_conv = np.stack(Is, axis=-1)
    n_vals = np.prod(I_conv.shape)
    score = (np.sum(np.abs(I_conv)) / n_vals)

    ScoreData = {
        "score": score
    }
    return ScoreData

# Main Vars
MATCHSCORE_FUNCS = {
    "Pixel-wise Average Difference": {
        "func": ImageMatch_Score_PixelWiseAvgDifference,
        "params": {
            "resizeFunc": "simple"
        }
    },
    "Normalised Correlation Average": {
        "func": ImageMatch_Score_NormCorrelationAvg,
        "params": {
            "resizeFunc": "simple"
        }
    }
}