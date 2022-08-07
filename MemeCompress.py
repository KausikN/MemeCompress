"""
Meme Compress
"""

# Imports
from Utils.Dataset import *
from Utils.ImageMatchFunctions import *

from Data.Datasets.Data_7000 import DatasetUtils as Data_7000_Utils

# Main Vars
DATASETS = {
    "Data 7000": Data_7000_Utils
}

# Main Functions
def MemeCompress_ClassifyMemeFormat(
    I, format_paths, 
    MatchScoreFunc=MATCHSCORE_FUNCS["Pixel-wise Average Difference"], 
    progressObj=tqdm, 
    **params
    ):
    '''
    MemeCompress - Classify Meme to a existing Format
    '''
    # Init
    I = I.copy()
    # Find Scores for each format
    scores = []
    for p in progressObj(format_paths):
        # Load Format Image
        I_format = Dataset_LoadImage(p)
        # Score
        ScoreData = MatchScoreFunc["func"](I, I_format, **MatchScoreFunc["params"])
        score = ScoreData["score"]
        # Record
        scores.append(score)
    # Sort Scores and Paths
    scores = np.array(scores)
    format_paths = np.array(format_paths)
    sorted_order = list(np.argsort(scores)[::-1])
    scores_sort = scores[sorted_order]
    format_paths_sort = format_paths[sorted_order]

    ScoresData = {
        "paths": format_paths_sort,
        "scores": scores_sort
    }
    return ScoresData

# RunCode