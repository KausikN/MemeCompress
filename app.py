"""
Stream lit GUI for hosting {FEATUREDATA_PROJECT_NAME}
"""

# Imports
import os
import streamlit as st
import json

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

# Util Vars
CACHE = {}

# Util Functions
def LoadCache():
    global CACHE
    CACHE = json.load(open(CACHE_PATH, "r"))

def SaveCache():
    global CACHE
    json.dump(CACHE, open(CACHE_PATH, "w"), indent=4)

# Main Functions


# UI Functions


# Repo Based Functions
# * Function for a page should be named as follows
# * Page Name mentioned in UIConfig.json => {PageName}
# * Make {PageName} all lower case => {PageName} = {PageName}.lower()
# * Convert spaces to underscores => {PageName} = {PageName}.replace(" ", "_")
# * Resulting string should be the name of the function which will be called when that page is opened in Streamlit GUI
def example_page():
    # Title
    st.header("HEADER TEXT")

    # Prereq Loaders

    # Load Inputs
    

    # Process Inputs

    # Display Outputs

    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()