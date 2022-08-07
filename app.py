"""
Stream lit GUI for hosting MemeCompress
"""

# Imports
import os
import streamlit as st
import json

from MemeCompress import *

# Main Vars
config = json.load(open("./StreamLitGUI/UIConfig.json", "r"))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    "Choose one of the following",
        tuple(
            [config["PROJECT_NAME"]] + 
            config["PROJECT_MODES"]
        )
    )
    
    if selected_box == config["PROJECT_NAME"]:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(" ", "_").lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config["PROJECT_NAME"])
    st.markdown("Github Repo: " + "[" + config["PROJECT_LINK"] + "](" + config["PROJECT_LINK"] + ")")
    st.markdown(config["PROJECT_DESC"])

    # st.write(open(config["PROJECT_README"], "r").read())

#############################################################################################################################
# Repo Based Vars
CACHE_PATH = "StreamLitGUI/CacheData/Cache.json"
PATHS = {
    "temp": "StreamLitGUI/TempData/", 
    "meme_formats": "Data/MemeFormats/",
    "examples": "Data/TestImgs/"
}

# Util Vars
CACHE = {}

# Util Functions
def LoadCache():
    global CACHE
    CACHE = json.load(open(CACHE_PATH, "r"))

def SaveCache():
    global CACHE
    json.dump(CACHE, open(CACHE_PATH, "w"), indent=4)

def ProgressObj_Streamlit(data):
    '''
    Streamlit Progress Bar for loops
    '''
    progressObj = st.progress(0.0)
    for i, d in enumerate(data):
        progressObj.progress((i+1)/len(data))
        yield d

# Main Functions


# UI Functions
def UI_LoadFormats():
    '''
    Load Formats
    '''
    global PATHS

    PATHS["meme_formats"] = st.sidebar.text_input("Meme Formats Dir", value="Data/MemeFormats/")
    format_paths = [os.path.join(PATHS["meme_formats"], f) for f in os.listdir(PATHS["meme_formats"])]
    st.sidebar.markdown(f"Found {len(format_paths)} Meme Formats")
    
    return format_paths

def UI_LoadDataset():
    '''
    Load Dataset
    '''
    st.markdown("## Load Dataset")
    # Select Dataset
    USERINPUT_Dataset = st.selectbox("Select Dataset", list(DATASETS.keys()))
    DATASET_MODULE = DATASETS[USERINPUT_Dataset]
    # Load Dataset
    DATASET = DATASET_MODULE.DATASET_FUNCS["full"]()
    # Remove NaN
    DATASET.dropna(inplace=True)
    DATASET.reset_index(drop=True, inplace=True)

    return DATASET

def UI_SelectDatasetSample(DATASET):
    '''
    Select Sample from Dataset
    '''
    # Display Top N Images
    N = DATASET.shape[0]
    USERINPUT_ViewSampleIndex = st.slider(f"Select Meme ({N} Memes)", 0, N-1, 0, 1)
    I = np.array(cv2.imread(DATASET["path"][USERINPUT_ViewSampleIndex]), dtype=np.uint8)
    st.image(
        DATASET["path"][USERINPUT_ViewSampleIndex], 
        caption=f"Image: {USERINPUT_ViewSampleIndex} {I.shape}", 
        use_column_width=True
    )

    return USERINPUT_ViewSampleIndex

def UI_LoadMeme():
    '''
    Load Meme Image
    '''
    st.markdown("## Load Meme")
    USERINPUT_LoadType = st.selectbox("Load Type", ["Examples", "Upload", "Datasets"])
    if USERINPUT_LoadType == "Examples":
        EXAMPLES_DIR = PATHS["examples"]
        EXAMPLE_FILES = os.listdir(EXAMPLES_DIR)
        USERINPUT_ImagePath = st.selectbox("Select Example File", EXAMPLE_FILES)
        USERINPUT_ImagePath = os.path.join(EXAMPLES_DIR, USERINPUT_ImagePath)
        I_meme = Dataset_LoadImage(USERINPUT_ImagePath)
        st.image(I_meme, caption=f"Image: {I_meme.shape}", use_column_width=True)
    elif USERINPUT_LoadType == "Upload":
        USERINPUT_ImagePath = os.path.join(PATHS["temp"], "UploadedMeme.png")
        I_meme_data = st.file_uploader("Upload Image", type=["jpg", "png", "PNG", "jpeg", "bmp"])
        if I_meme_data is None: USERINPUT_ImagePath = os.path.join(PATHS["examples"], os.listdir(PATHS["examples"])[0])
        else: open(USERINPUT_ImagePath, "wb").write(I_meme_data)
        I_meme = Dataset_LoadImage(USERINPUT_ImagePath)
        st.image(I_meme, caption=f"Image: {I_meme.shape}", use_column_width=True)
    else:
        DATASET = UI_LoadDataset()
        USERINPUT_SampleIndex = UI_SelectDatasetSample(DATASET)
        USERINPUT_ImagePath = DATASET["path"][USERINPUT_SampleIndex]
        I_meme = Dataset_LoadImage(USERINPUT_ImagePath)

    return I_meme

def UI_SelectFormatMatchFunc():
    '''
    Select Format Match Function
    '''
    cols = st.columns((1, 3))
    # Load Func
    USERINPUT_FormatMatchFunc = cols[0].selectbox("Select Format Match Function", list(MATCHSCORE_FUNCS.keys()))
    # Load Params
    USERINPUT_FormatMatchFuncParams = MATCHSCORE_FUNCS[USERINPUT_FormatMatchFunc]["params"]
    USERINPUT_FormatMatchFuncParams_str = cols[1].text_area("Format Match Function Params", value=json.dumps(USERINPUT_FormatMatchFuncParams, indent=4))
    USERINPUT_FormatMatchFuncParams = json.loads(USERINPUT_FormatMatchFuncParams_str)

    USERINPUT_FormatMatchFunc = {
        "func": MATCHSCORE_FUNCS[USERINPUT_FormatMatchFunc]["func"],
        "params": USERINPUT_FormatMatchFuncParams
    }
    return USERINPUT_FormatMatchFunc

# Repo Based Functions
def meme_analysis():
    # Title
    st.header("Meme Analysis")

    # Prereq Loaders

    # Load Inputs
    FORMAT_PATHS = UI_LoadFormats()
    I_meme = UI_LoadMeme()
    USERINPUT_FormatMatchFunc = UI_SelectFormatMatchFunc()

    # Process Inputs
    ScoresData = MemeCompress_ClassifyMemeFormat(
        I_meme, FORMAT_PATHS, USERINPUT_FormatMatchFunc, 
        progressObj=ProgressObj_Streamlit
    )
    # Display Outputs
    st.markdown("## Meme Format Match Scores")
    N = ScoresData["scores"].shape[0]
    USERINPUT_ViewScoreIndex = st.slider(f"View Matched Format ({N} Matches)", 0, N-1, 0, 1)
    cols = st.columns((1, 4))
    cols[0].markdown(f"Meme {USERINPUT_ViewScoreIndex}")
    cols[1].markdown(f"```\n{ScoresData['paths'][USERINPUT_ViewScoreIndex]}\n```")
    cols = st.columns((1, 4))
    cols[0].markdown("Score")
    cols[1].markdown(f"```\n{ScoresData['scores'][USERINPUT_ViewScoreIndex]}\n```")
    I = np.array(cv2.imread(ScoresData["paths"][USERINPUT_ViewScoreIndex]), dtype=np.uint8)
    st.image(
        ScoresData["paths"][USERINPUT_ViewScoreIndex], 
        caption=f"Format: {USERINPUT_ViewScoreIndex} {I.shape}", 
        use_column_width=True
    )

def meme_formats():
    global PATHS
    # Title
    st.header("Meme Formats")

    # Prereq Loaders

    # Load Inputs
    FORMAT_PATHS = UI_LoadFormats()
    DATASET = pd.DataFrame({"path": FORMAT_PATHS})
    USERINPUT_SampleIndex = UI_SelectDatasetSample(DATASET)

    # Process Inputs

    # Display Outputs

def meme_datasets():
    # Title
    st.header("Meme Datasets")

    # Prereq Loaders

    # Load Inputs
    DATASET = UI_LoadDataset()
    # Display Top N Images
    N = DATASET.shape[0]
    USERINPUT_ViewSampleIndex = st.slider(f"View Sample ({N} Samples)", 0, N-1, 0, 1)
    I = np.array(cv2.imread(DATASET["path"][USERINPUT_ViewSampleIndex]), dtype=np.uint8)
    st.image(
        DATASET["path"][USERINPUT_ViewSampleIndex], 
        caption=f"Image: {USERINPUT_ViewSampleIndex} {I.shape}", 
        use_column_width=True
    )

    # Process Inputs

    # Display Outputs

    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()