"""
Image Matchers - Basic
"""

# Imports
from ..Utils import *

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
    
    Process:
        - Resize Images to same size
            - Convert to Grayscale if to_grayscale is True
        - Calculate Absolute Pixel-wise Difference
            - Shape: (H, W, D)
            - Value: (0.0, 1.0)
        - Calculate Average Difference
            - Shape: (1,)
            - Value: (0.0, 1.0)
        - Calculate Score (1.0 - Average Difference)
            - Shape: (1,)
            - Value: (0.0, 1.0)
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

# Main Vars
IMAGEMATCH_FUNCS = {
    "Pixel-wise Average Difference": {
        "func": ImageMatch_Score_PixelWiseAvgDifference,
        "params": {
            "resizeFunc": "simple"
        }
    }
}