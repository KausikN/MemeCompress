"""
Image Matchers - Correlation
"""

# Imports
from scipy.signal import correlate2d

from ..Utils import *

# Main Functions
def ImageMatch_Score_NormCorrelationAvg(
    I_query, I_ref, 
    resizeFunc="simple", 
    to_grayscale=False,

    visualise=False,
    **params
    ):
    '''
    ImageMatch - Score - Normalised Correlation Average

    Process:
        - Resize Images to same size
            - Convert to Grayscale if to_grayscale is True
        - Calculate Normalised Correlation between Images
            - Shape: (Corr_H, Corr_W, D)
            - Value: (0.0, 1.0)
        - Calculate Score (Average Correlation Value)
            - Shape: (1,)
            - Value: (0.0, 1.0)
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
        I = correlate2d(I_query[:, :, d], I_ref[:, :, d])
        I = I / (I_ref.shape[0] * I_ref.shape[1])
        Is.append(I)
    I_conv = np.stack(Is, axis=-1)
    score = np.sum(I_conv) / (np.prod(I_conv.shape))
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
IMAGEMATCH_FUNCS = {
    "Normalised Correlation Average": {
        "func": ImageMatch_Score_NormCorrelationAvg,
        "params": {
            "resizeFunc": "simple",
            "to_grayscale": True
        }
    }
}