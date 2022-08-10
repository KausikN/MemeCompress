"""
Image Matching Functions

Inputs:
    I_query - Query image
    I_ref - Reference image
    Any other parameters to be passed to the matching function

Outputs: Dict with the keys:
    score - Score of the match
    plots_graphs - Dict of lists of matplotlib figures to be plotted using plotly in streamlit
    plots_image - Dict of lists of matplotlib figures to be plotted using pyplot in streamlit
    data - Any other data to be recorded
"""

# Imports
from scipy.signal import correlate2d, convolve2d
from .Utils import *

# Main Functions
def ImageMatch_Score_PixelWiseAvgDifference(
    I_query, I_ref, 
    resizeFunc="simple", 
    to_grayscale=False,

    visualise=False,
    **params
    ):
    '''
    ImageMatch - Score - PixelWise Average Difference
    '''
    # Resize query image to fit reference image
    resizeFunc = resizeFunc if resizeFunc in RESIZE_FUNCS.keys() else RESIZE_FUNCS["simple"]
    I_query = RESIZE_FUNCS[resizeFunc](I_query, I_ref.shape)
    if I_ref.ndim == 3 and to_grayscale:
        I_query = np.mean(I_query, axis=-1)
        I_ref = np.mean(I_ref, axis=-1)
    # Score
    n_vals = np.prod(I_ref.shape)
    diff_map = np.abs(I_query - I_ref)
    score = 1.0 - (np.sum(diff_map) / n_vals)
    # Record
    ScoreData = {
        "score": score,
        "plots_plotly": {},
        "plots_pyplot": {},
        "data": {}
    }
    # Visualisation
    if visualise:
        # Images
        ScoreData["plots_pyplot"]["Images"] = []
        fig = plt.figure()
        plt.imshow(I_query, cmap="gray")
        plt.title(f"Query Image {I_query.shape}")
        ScoreData["plots_pyplot"]["Images"].append(fig)
        fig = plt.figure()
        plt.imshow(I_ref, cmap="gray")
        plt.title(f"Reference Image {I_ref.shape}")
        ScoreData["plots_pyplot"]["Images"].append(fig)
        # Difference Map
        fig = plt.figure()
        plt.imshow(diff_map, cmap="gray")
        plt.title("Difference Map")
        ScoreData["plots_pyplot"]["Maps"] = [fig]
    
    return ScoreData

def ImageMatch_Score_NormCorrelationAvg(
    I_query, I_ref, 
    resizeFunc="simple", 
    to_grayscale=False,

    visualise=False,
    **params
    ):
    '''
    ImageMatch - Score - Normalised Correlation Average
    '''
    # Resize query image to fit reference image
    resizeFunc = resizeFunc if resizeFunc in RESIZE_FUNCS.keys() else RESIZE_FUNCS["simple"]
    I_query = RESIZE_FUNCS[resizeFunc](I_query, I_ref.shape)
    if I_ref.ndim == 3 and to_grayscale:
        I_query = np.mean(I_query, axis=-1)
        I_ref = np.mean(I_ref, axis=-1)
    # Reshape
    if I_query.ndim == 2: I_query = I_query.reshape((I_query.shape[0], I_query.shape[1], 1))
    if I_ref.ndim == 2: I_ref = I_ref.reshape((I_ref.shape[0], I_ref.shape[1], 1))
    # Score
    Is = []
    for d in range(I_ref.shape[2]):
        I_conv = correlate2d(I_query[:, :, d], I_ref[:, :, d])
        Is.append(I_conv)
    I_conv = np.stack(Is, axis=-1)
    n_vals = np.prod(I_conv.shape)
    score = (np.sum(np.abs(I_conv)) / n_vals)
    # Record
    ScoreData = {
        "score": score,
        "plots_plotly": {},
        "plots_pyplot": {},
        "data": {}
    }
    # Visualisation
    if visualise:
        if I_ref.ndim == 2: I_conv = I_conv[:, :, 0]
        # Images
        ScoreData["plots_pyplot"]["Images"] = []
        fig = plt.figure()
        plt.imshow(I_query, cmap="gray")
        plt.title(f"Query Image {I_query.shape}")
        ScoreData["plots_pyplot"]["Images"].append(fig)
        fig = plt.figure()
        plt.imshow(I_ref, cmap="gray")
        plt.title(f"Reference Image {I_ref.shape}")
        ScoreData["plots_pyplot"]["Images"].append(fig)
        # Correlation Map
        fig = plt.figure()
        I_conv = NormaliseToRange(I_conv, val_range=(0.0, 1.0))
        plt.imshow(I_conv, cmap="gray")
        plt.title("Correlation Map")
        ScoreData["plots_pyplot"]["Maps"] = [fig]

    return ScoreData

def ImageMatch_Score_SpatialSplitHistogram(
    I_query, I_ref, 
    resizeFunc="simple", 
    to_grayscale=False,

    visualise=False,
    **params
    ):
    '''
    ImageMatch - Score - Histogram Similarity with Spatial Split
    '''
    # Resize query image to fit reference image
    resizeFunc = resizeFunc if resizeFunc in RESIZE_FUNCS.keys() else RESIZE_FUNCS["simple"]
    I_query = RESIZE_FUNCS[resizeFunc](I_query, I_ref.shape)
    if I_ref.ndim == 3 and to_grayscale:
        I_query = np.mean(I_query, axis=-1)
        I_ref = np.mean(I_ref, axis=-1)
    # Reshape
    if I_query.ndim == 2: I_query = I_query.reshape((I_query.shape[0], I_query.shape[1], 1))
    if I_ref.ndim == 2: I_ref = I_ref.reshape((I_ref.shape[0], I_ref.shape[1], 1))
    # Score
    Is = []
    for d in range(I_ref.shape[2]):
        I_conv = correlate2d(I_query[:, :, d], I_ref[:, :, d])
        Is.append(I_conv)
    I_conv = np.stack(Is, axis=-1)
    n_vals = np.prod(I_conv.shape)
    score = (np.sum(np.abs(I_conv)) / n_vals)
    # Record
    ScoreData = {
        "score": score,
        "plots_plotly": {},
        "plots_pyplot": {},
        "data": {}
    }
    # Visualisation
    if visualise:
        if I_ref.ndim == 2: I_conv = I_conv[:, :, 0]
        # Images
        ScoreData["plots_pyplot"]["Images"] = []
        fig = plt.figure()
        plt.imshow(I_query, cmap="gray")
        plt.title(f"Query Image {I_query.shape}")
        ScoreData["plots_pyplot"]["Images"].append(fig)
        fig = plt.figure()
        plt.imshow(I_ref, cmap="gray")
        plt.title(f"Reference Image {I_ref.shape}")
        ScoreData["plots_pyplot"]["Images"].append(fig)
        # Correlation Map
        fig = plt.figure()
        I_conv = NormaliseToRange(I_conv, val_range=(0.0, 1.0))
        plt.imshow(I_conv, cmap="gray")
        plt.title("Correlation Map")
        ScoreData["plots_pyplot"]["Maps"] = [fig]

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
            "resizeFunc": "simple",
            "to_grayscale": True
        }
    }
}