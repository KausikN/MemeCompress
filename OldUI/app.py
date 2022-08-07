'''
Summary
This script acts as the frontend to app
'''

import MemeCompress
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
MainLabelText = None
NDirsLabelText = None
nMatchesTextField = None
DirLabels = []
OutputDirText = None
FormatDBText = None
MemeFormatDBPath = ''
OutputDir = ''

OpenedImageDBPaths = []

# Utils
imgExtns = ['.bmp', '.png', '.jpg', '.jpeg']

# TKinter Window
def CreateWindow():
    global curRow
    global FormatDBText
    global MainLabelText
    global NDirsLabelText
    global OutputDirText
    global nMatchesTextField

    Button(root, text="Select Image Dirs", command=SelectImageDirDialogBox).grid(row=curRow, column=0)
    Button(root, text="Select Output Dir", command=SelectDirDialogBox).grid(row=curRow, column=1)
    Button(root, text="Select Format DB File", command=SelectDBDialogBox).grid(row=curRow, column=2)
    Button(root, text="Classify Images", command=ClassifyImages).grid(row=curRow, column=3)
    Button(root, text="Remove Last Dir", command=RemoveLastFile).grid(row=curRow, column=4)
    
    curRow += 1
    MainLabelText = tk.StringVar()
    MainLabelText.set("")
    MainLabel = Label(root, textvariable=MainLabelText)
    MainLabel.grid(row=curRow, column=0)
    curRow += 1
    FormatDBText = tk.StringVar()
    FormatDBText.set("")
    FormatDB_Label = Label(root, textvariable=FormatDBText)
    FormatDB_Label.grid(row=curRow, column=0)
    curRow += 1
    OutputDirText = tk.StringVar()
    OutputDirText.set("")
    OutputDir_Label = Label(root, textvariable=OutputDirText)
    OutputDir_Label.grid(row=curRow, column=0)
    curRow += 1
    nMatchesLabel = Label(root, text="N Matches: ")
    nMatchesLabel.grid(row=curRow, column=0)
    nMatchesTextField = Entry(root)
    nMatchesTextField.grid(row=curRow, column=1)
    curRow += 1
    NDirsLabelText = tk.StringVar()
    NDirsLabelText.set("No Files Added")
    NFilesLabel = Label(root, textvariable=NDirsLabelText)
    NFilesLabel.grid(row=curRow, column=0)
    curRow += 1

def SelectImageDirDialogBox():
    global curRow
    global DirLabels
    global MainLabelText
    global NDirsLabelText
    global OpenedImageDBPaths

    # Create File Dialog Box
    root.filename = filedialog.askdirectory(initialdir='./', title="Select Image Dirs")

    MainLabelText.set("")

    print(root.filename, os.path.splitext(root.filename)[-1])
    if not root.filename in OpenedImageDBPaths:
        OpenedImageDBPaths.append(root.filename)
        NDirsLabelText.set("Added " + str(len(OpenedImageDBPaths)) + " Dirs")
        newdirlabel = Label(root, text=root.filename)
        newdirlabel.grid(row=curRow, column=0)
        DirLabels.append(newdirlabel)
        curRow += 1
    else:
        MainLabelText.set("Dir already added.")

def SelectDirDialogBox():
    global curRow
    global OutputDirText
    global OutputDir

    # Create Dir Dialog Box
    root.dirname = filedialog.askdirectory(initialdir='./', title="Select Output Dir")

    OutputDirText.set('Output Dir: ' + root.dirname)
    OutputDir = root.dirname

def SelectDBDialogBox():
    global curRow
    global MemeFormatDBPath
    global FormatDBText

    # Create Dir Dialog Box
    root.filename = filedialog.askopenfilename(initialdir='./', title="Select Format DB File")

    FormatDBText.set('Format DB: ' + root.filename)
    MemeFormatDBPath = root.filename

def RemoveLastFile():
    global OpenedImageDBPaths
    global DirLabels
    global NDirsLabelText

    if len(OpenedImageDBPaths) > 0:
        OpenedImageDBPaths.pop()
        DirLabels[-1].grid_forget()
        DirLabels.pop()
        if len(OpenedImageDBPaths) > 0:
            NDirsLabelText.set("Added " + str(len(OpenedImageDBPaths)) + " Files")
        else:
            NDirsLabelText.set("No Files Added")

def ClassifyImages():
    global MainLabelText
    global OutputDir
    global MemeFormatDBPath
    global OpenedImageDBPaths
    global nMatchesTextField

    MainLabelText.set("Started Classifying Images")

    # Setup
    DBFormatPath = MemeFormatDBPath
    SavePath = OutputDir
    nMatches = int(nMatchesTextField.get())

    # Create a Image DB for required files
    ImageDatabase.SaveDatabase(OpenedImageDBPaths, 'ImagesToClassifyDB.p')

    # Classify
    MemeCompress.ClassifyMemes2Formats('ImagesToClassifyDB.p', DBFormatPath, SavePath, nMatches=nMatches, nCols=5)

    print("Finished Classifying Images")
    MainLabelText.set("Finished Classifying Images")

# Main Code

# Init Root
print('Creating Window...')
root = Tk()
root.title('Devotee App')

# Create Window
CreateWindow()
print('Created Window')

root.mainloop()