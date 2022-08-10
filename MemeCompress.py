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
def MemeCompress_ImagesSimilarity(
    I_query, I_ref, 
    MatchScoreFunc=IMAGEMATCH_FUNCS["Pixel-wise Average Difference"], 
    visualise=False,
    **params
    ):
    '''
    MemeCompress - Find Similarity between Query and Reference Image
    '''
    # Score
    MatchScoreFunc["params"]["visualise"] = visualise
    ScoreData = MatchScoreFunc["func"](I_query, I_ref, **MatchScoreFunc["params"])
    
    return ScoreData

def MemeCompress_ClassifyMemeFormat(
    I, format_paths, 
    MatchScoreFunc=IMAGEMATCH_FUNCS["Pixel-wise Average Difference"], FormatMaxSize=4096, 
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
    score_datas = []
    for p in progressObj(format_paths):
        # Load Format Image
        I_format = Dataset_LoadImage(p)
        # Resize Format Image
        I_format = Resize_MaxSizeARPreserved(I_format, FormatMaxSize, always_resize=False)
        # Score
        ScoreData = MatchScoreFunc["func"](I, I_format, **MatchScoreFunc["params"])
        score = ScoreData["score"]
        # Record
        score_datas.append(ScoreData)
        scores.append(score)
    # Sort Scores and Paths
    scores = np.array(scores)
    format_paths = np.array(format_paths)
    sorted_order = list(np.argsort(scores)[::-1])
    scores_sort = scores[sorted_order]
    score_datas_sort = [score_datas[i] for i in sorted_order]
    format_paths_sort = format_paths[sorted_order]

    ScoresData = {
        "paths": format_paths_sort,
        "scores": scores_sort,
        "data": score_datas_sort
    }
    return ScoresData

# RunCode