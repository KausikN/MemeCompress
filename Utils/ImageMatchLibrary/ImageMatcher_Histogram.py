"""
Image Matchers - Histogram
"""

# Imports
from ..Utils import *

# Main Functions
def ImageMatch_Score_SpatialSplitHistogram(
    I_query, I_ref, 
    to_grayscale=False,

    n_splits=3,
    n_bins=256,

    visualise=False,
    **params
    ):
    '''
    ImageMatch - Score - Histogram Similarity with Spatial Splitting

    Process:
        - Convert Images to Grayscale if to_grayscale is True
        - Split Images into (n_splits x n_splits) regions
            - Shape: (n_splits, n_splits, Region_Query_H, Region_Query_W, D), (n_splits, n_splits, Region_Ref_H, Region_Ref_W, D)
            - Value: (0.0, 1.0)
        - Calculate Histograms (Normalised) for each region in both Images
            - Shape: (n_splits, n_splits, D, n_bins), (n_splits, n_splits, D, n_bins)
            - Value: (0.0, 1.0)
        - Calculate Sum of Absolute Histogram Differences between Image Histograms for each region
            - Shape: (n_splits, n_splits, D)
            - Value: (0.0, 2.0)
                - In perfect difference, there is no overlap and hence sum of absolute differences is 1 + 1 = 2
        - Average over depths, Normalise value to fit to [0, 1], Invert difference to get final similarities for each region
            - Shape: (n_splits, n_splits) 
            - Value: (0.0, 1.0)
        - Calculate Score (Average Similarity Value)
            - Shape: (1,)
            - Value: (0.0, 1.0)
    '''
    # Init
    if I_ref.ndim == 3 and to_grayscale:
        I_query = np.mean(I_query, axis=-1)
        I_ref = np.mean(I_ref, axis=-1)
    # Reshape
    if I_query.ndim == 2: I_query = I_query.reshape((I_query.shape[0], I_query.shape[1], 1))
    if I_ref.ndim == 2: I_ref = I_ref.reshape((I_ref.shape[0], I_ref.shape[1], 1))
    # Score
    Hists_query = np.zeros((n_splits, n_splits, I_ref.shape[2], n_bins))
    Hists_ref = np.zeros((n_splits, n_splits, I_ref.shape[2], n_bins))
    HistDiffs = np.zeros((n_splits, n_splits))
    for d in range(I_ref.shape[2]):
        for i in range(n_splits):
            rowRange_query = (int(i * I_query.shape[0] / n_splits), min(ceil((i + 1) * I_query.shape[0] / n_splits), I_query.shape[0]))
            rowRange_ref = (int(i * I_ref.shape[0] / n_splits), min(ceil((i + 1) * I_ref.shape[0] / n_splits), I_ref.shape[0]))
            for j in range(n_splits):
                colRange_query = (int(j * I_query.shape[1] / n_splits), min(ceil((j + 1) * I_query.shape[1] / n_splits), I_query.shape[1]))
                colRange_ref = (int(j * I_ref.shape[1] / n_splits), min(ceil((j + 1) * I_ref.shape[1] / n_splits), I_ref.shape[1]))
                I_query_split = I_query[rowRange_query[0]:rowRange_query[1], colRange_query[0]:colRange_query[1], d]
                I_ref_split = I_ref[rowRange_ref[0]:rowRange_ref[1], colRange_ref[0]:colRange_ref[1], d]
                # Histogram Similarity
                I_query_hist, bin_edges = np.histogram(I_query_split, bins=n_bins, range=(0.0, 1.0))
                I_ref_hist, bin_edges = np.histogram(I_ref_split, bins=n_bins, range=(0.0, 1.0))
                I_query_hist = I_query_hist / np.sum(I_query_hist) # (0, 1) and sums to 1
                I_ref_hist = I_ref_hist / np.sum(I_ref_hist) # (0, 1) and sums to 1
                HistDiffs[i, j] += np.sum(np.abs(I_query_hist - I_ref_hist)) # (0, 2) as in perfect difference, no overlap, abs sum = 2
                # Record
                Hists_query[i, j, d] = I_query_hist
                Hists_ref[i, j, d] = I_ref_hist
    # Norm HistDiffs ((0, 2d) -> (0, 1)) and Invert to get HistSimilarity
    HistSimilarities = 1.0 - (HistDiffs / (I_ref.shape[2] * 2.0))
    # Overall Score
    score = np.sum(HistSimilarities) / np.prod(HistSimilarities.shape)
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
        # Split Images
        I_query_display = I_query.copy()
        I_ref_display = I_ref.copy()
        for i in range(n_splits):
            rowRange_query = (int(i * I_query.shape[0] / n_splits), min(ceil((i + 1) * I_query.shape[0] / n_splits), I_query.shape[0]))
            rowRange_ref = (int(i * I_ref.shape[0] / n_splits), min(ceil((i + 1) * I_ref.shape[0] / n_splits), I_ref.shape[0]))
            colRange_query = (int(i * I_query.shape[1] / n_splits), min(ceil((i + 1) * I_query.shape[1] / n_splits), I_query.shape[1]))
            colRange_ref = (int(i * I_ref.shape[1] / n_splits), min(ceil((i + 1) * I_ref.shape[1] / n_splits), I_ref.shape[1]))
            I_query_display[:, colRange_query[0]] = 0.0
            I_query_display[:, colRange_query[1]-1] = 0.0
            I_query_display[rowRange_query[0], :] = 0.0
            I_query_display[rowRange_query[1]-1, :] = 0.0
            I_ref_display[:, colRange_ref[0]] = 0.0
            I_ref_display[:, colRange_ref[1]-1] = 0.0
            I_ref_display[rowRange_ref[0], :] = 0.0
            I_ref_display[rowRange_ref[1]-1, :] = 0.0
        ScoreData["plots_pyplot"]["Images Split"] = []
        fig = plt.figure()
        plt.imshow(I_query_display, cmap="gray")
        plt.title(f"Query Image Split {I_query.shape}")
        ScoreData["plots_pyplot"]["Images Split"].append(fig)
        fig = plt.figure()
        plt.imshow(I_ref_display, cmap="gray")
        plt.title(f"Reference Image Split {I_ref.shape}")
        ScoreData["plots_pyplot"]["Images Split"].append(fig)
        # Histogram Similarity Map
        fig = plt.figure()
        plt.imshow(HistSimilarities, cmap="gray")
        plt.title("Histogram Similarity Map")
        ScoreData["plots_pyplot"]["Maps"] = [fig]
        # Histogram Plots
        for d in range(I_ref.shape[2]):
            hk = f"Histogram (Channel {d})"
            ScoreData["plots_pyplot"][hk] = []
            fig = plt.figure()
            for i in range(n_splits):
                for j in range(n_splits):
                    plt.subplot(n_splits, n_splits, i * n_splits + j + 1)
                    plt.bar(bin_edges[:-1], Hists_query[i, j, d], width=bin_edges[1] - bin_edges[0], color="blue")
                    plt.axis("off")
            ScoreData["plots_pyplot"][hk].append(fig)
            fig = plt.figure()
            for i in range(n_splits):
                for j in range(n_splits):
                    plt.subplot(n_splits, n_splits, i * n_splits + j + 1)
                    plt.bar(bin_edges[:-1], Hists_ref[i, j, d], width=bin_edges[1] - bin_edges[0], color="blue")
                    plt.axis("off")
            ScoreData["plots_pyplot"][hk].append(fig)

    return ScoreData

# Main Vars
IMAGEMATCH_FUNCS = {
    "Spatial Split Histogram": {
        "func": ImageMatch_Score_SpatialSplitHistogram,
        "params": {
            "to_grayscale": True,
            "n_splits": 3,
            "n_bins": 256
        }
    }
}