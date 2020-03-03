'''
Summary
This script acts as the frontend to app
'''

import PixelBreak
import ImageDatabase

import os
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

from tqdm import tqdm
import json
import cv2

curRow = 0
MainLabelText_PB = None
NFilesLabelText_PB = None
FileLabels_PB = []
OutputDirText = None
OutputDir = ''
C_JSON_Text = None
G_JSON_Text = None

C_JSON_Path = ''
G_JSON_Path = ''

OpenedImagesPaths = []

# Utils
imgExtns = ['.bmp', '.png', '.jpg', '.jpeg']

# TKinter Window
def CreateWindow():
    global curRow
    global MainLabelText_PB
    global NFilesLabelText_PB
    global OutputDirText
    global C_JSON_Text
    global G_JSON_Text

    Button(root, text="Select Image File", command=SelectFileDialogBox_PB).grid(row=curRow, column=0)
    Button(root, text="Select Output Dir", command=SelectDirDialogBox).grid(row=curRow, column=1)
    Button(root, text="Break Images", command=BreakImages).grid(row=curRow, column=2)
    Button(root, text="Remove Last File", command=RemoveLastFile_PB).grid(row=curRow, column=3)
    curRow += 1
    Button(root, text="Select Color JSON", command=SelectFileDialogBox_C_JSON).grid(row=curRow, column=0)
    Button(root, text="Select Gray JSON", command=SelectFileDialogBox_G_JSON).grid(row=curRow, column=1)
    curRow += 1
    C_JSON_Text = tk.StringVar()
    C_JSON_Text.set("No Files Added")
    C_JSON_Label = Label(root, textvariable=C_JSON_Text)
    C_JSON_Label.grid(row=curRow, column=0)
    curRow += 1
    G_JSON_Text = tk.StringVar()
    G_JSON_Text.set("No Files Added")
    G_JSON_Label = Label(root, textvariable=G_JSON_Text)
    G_JSON_Label.grid(row=curRow, column=0)
    curRow += 1
    MainLabelText_PB = tk.StringVar()
    MainLabelText_PB.set("")
    MainLabel_PB = Label(root, textvariable=MainLabelText_PB)
    MainLabel_PB.grid(row=curRow, column=0)
    curRow += 1
    OutputDirText = tk.StringVar()
    OutputDirText.set("")
    OutputDir_Label = Label(root, textvariable=OutputDirText)
    OutputDir_Label.grid(row=curRow, column=0)
    curRow += 1
    NFilesLabelText_PB = tk.StringVar()
    NFilesLabelText_PB.set("No Files Added")
    NFilesLabel_PB = Label(root, textvariable=NFilesLabelText_PB)
    NFilesLabel_PB.grid(row=curRow, column=0)
    curRow += 1

def SelectFileDialogBox_PB():
    global curRow
    global FileLabels_PB
    global MainLabelText_PB
    global NFilesLabelText_PB
    global OpenedImagesPaths

    # Create File Dialog Box
    root.filenames = filedialog.askopenfilenames(initialdir='./', title="Select Image Files")

    MainLabelText_PB.set("")
    for filename in root.filenames:
        print(filename, os.path.splitext(filename)[-1])
        if not os.path.splitext(filename)[-1] in imgExtns: # Check if selected file is image file
            MainLabelText_PB.set("Please select a proper Image File to break.")
            return
        else:
            if not filename in OpenedImagesPaths:
                OpenedImagesPaths.append(filename)
                NFilesLabelText_PB.set("Added " + str(len(OpenedImagesPaths)) + " Files")
                newfilelabel = Label(root, text=filename)
                newfilelabel.grid(row=curRow, column=0)
                FileLabels_PB.append(newfilelabel)
                curRow += 1
            else:
                MainLabelText_PB.set("File already added.")

def SelectDirDialogBox():
    global curRow
    global OutputDirText
    global OutputDir

    # Create Dir Dialog Box
    root.dirname = filedialog.askdirectory(initialdir='./', title="Select Output Dir")

    OutputDirText.set('Output Dir: ' + root.dirname)
    OutputDir = root.dirname

def SelectFileDialogBox_C_JSON():
    global curRow
    global C_JSON_Path
    global C_JSON_Text
    global MainLabelText_PB

    # Create File Dialog Box
    root.filename = filedialog.askopenfilename(initialdir='./', title="Select Color JSON File")

    MainLabelText_PB.set("")

    if not os.path.splitext(root.filename)[-1] == '.json': # Check if selected file is json
        MainLabelText_PB.set("Please select a proper JSON File.")
        return
    else:
        C_JSON_Text.set('Color JSON: ' + root.filename)
        C_JSON_Path = root.filename

def SelectFileDialogBox_G_JSON():
    global curRow
    global G_JSON_Path
    global G_JSON_Text
    global MainLabelText_PB

    # Create File Dialog Box
    root.filename = filedialog.askopenfilename(initialdir='./', title="Select Grayscale JSON File")

    MainLabelText_PB.set("")

    if not os.path.splitext(root.filename)[-1] == '.json': # Check if selected file is json
        MainLabelText_PB.set("Please select a proper JSON File.")
        return
    else:
        G_JSON_Text.set('Gray JSON: ' + root.filename)
        G_JSON_Path = root.filename

def RemoveLastFile_PB():
    global OpenedImagesPaths
    global FileLabels_PB
    global NFilesLabelText_PB

    if len(OpenedImagesPaths) > 0:
        OpenedImagesPaths.pop()
        FileLabels_PB[-1].grid_forget()
        FileLabels_PB.pop()
        if len(OpenedImagesPaths) > 0:
            NFilesLabelText_PB.set("Added " + str(len(OpenedImagesPaths)) + " Files")
        else:
            NFilesLabelText_PB.set("No Files Added")

def BreakImages():
    global MainLabelText_PB
    global OutputDir
    global OpenedImagesPaths
    global C_JSON_Path
    global G_JSON_Path

    MainLabelText_PB.set("Started Breaking Images")

    # Setup
    PixelBreak.LoadFillImagesData(G_JSON=G_JSON_Path, C_JSON=C_JSON_Path)
    ImagePath = 'test.jpg'
    GrayScaleInput = False

    window_size = (10, 10)
    match_mode = 'avg'
    fillImageSize=(10, 10)

    roundRange = 1
    if GrayScaleInput:
        G_Dict = {}
        with open(G_JSON_Path) as fgr:
            G_Dict = json.load(fgr)
        roundRange = G_Dict['roundrange']
    else:
        C_Dict = {}
        with open(C_JSON_Path) as fgr:
            C_Dict = json.load(fgr)
        roundRange = C_Dict['roundrange']

    nextImageMode = 'random'
    
    for imgp in tqdm(OpenedImagesPaths):
        splitImgSavePath = os.path.join(OutputDir, str(os.path.split(imgp)[-1]) + "_Broken" + ".png")
        I = None
        if GrayScaleInput:
            I = cv2.imread(imgp, 0)
        else:
            I = cv2.imread(imgp)
        splitImage = PixelBreak.ImageBreak(I, window_size, match_mode, fillImageSize, nextImageMode=nextImageMode, roundRange=roundRange, DisplayIntermiateSteps=False)
        cv2.imwrite(splitImgSavePath, splitImage)

    MainLabelText_PB.set("Finished Breaking Images")

# Main Code

# Init Root
print('Creating Window...')
root = Tk()
root.title('Devotee App')

# Create Window
CreateWindow()
print('Created Window')

root.mainloop()