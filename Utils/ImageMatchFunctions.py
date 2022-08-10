"""
Image Matching Functions

Inputs:
    I_query - Query image
    I_ref - Reference image
    Any other parameters to be passed to the matching function

Outputs: Dict with the keys:
    score - Score of the match
    plots_plotly - Dict of lists of matplotlib figures to be plotted using plotly in streamlit
    plots_pyplot - Dict of lists of matplotlib figures to be plotted using pyplot in streamlit
    data - Any other data to be recorded
"""

# Imports
from .Utils import *
# Matchers Imports
from .ImageMatchLibrary import ImageMatcher_Basic
from .ImageMatchLibrary import ImageMatcher_Correlation
from .ImageMatchLibrary import ImageMatcher_Histogram

# Main Functions


# Main Vars
MATCHER_MODULES = {
    "Basic": ImageMatcher_Basic,
    "Correlation": ImageMatcher_Correlation,
    "Histogram": ImageMatcher_Histogram
}
IMAGEMATCH_FUNCS = {}
for mk in MATCHER_MODULES.keys(): IMAGEMATCH_FUNCS.update(MATCHER_MODULES[mk].IMAGEMATCH_FUNCS)