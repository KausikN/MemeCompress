'''
Summary
This script acts as the frontend to database app
'''

import ImageDatabase

import os
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

curRow = 0
MainLabelText_DB = None
NFilesLabelText_DB = None
FileLabels_DB = []
DBFile_Text = None

DBFile_Path = ''


# Utils


# TKinter Window
def CreateWindow():
    global curRow
    global MainLabelText_DB
    global NFilesLabelText_DB
    global DBFile_Text

    Button(root, text="Select Dir", command=SelectFileDialogBox_DBDir).grid(row=curRow, column=0)
    Button(root, text="Add to Database", command=Add2DB).grid(row=curRow, column=1)
    Button(root, text="Remove Last Dir", command=RemoveLastFile_DB).grid(row=curRow, column=2)
    curRow += 1
    Button(root, text="Select DB File", command=SelectFileDialogBox_DBFile).grid(row=curRow, column=0)
    Button(root, text="Create DB File", command=SelectFileDialogBox_CreateDBFile).grid(row=curRow, column=1)
    curRow += 1
    MainLabelText_DB = tk.StringVar()
    MainLabelText_DB.set("")
    MainLabel_DB = Label(root, textvariable=MainLabelText_DB)
    MainLabel_DB.grid(row=curRow, column=0)
    curRow += 1
    NFilesLabelText_DB = tk.StringVar()
    NFilesLabelText_DB.set("No Files Added")
    NFilesLabel_DB = Label(root, textvariable=NFilesLabelText_DB)
    NFilesLabel_DB.grid(row=curRow, column=0)
    curRow += 1
    DBFile_Text = tk.StringVar()
    DBFile_Text.set("No Files Added")
    DBFile_Label = Label(root, textvariable=DBFile_Text)
    DBFile_Label.grid(row=curRow, column=0)
    curRow += 1

def SelectFileDialogBox_DBDir():
    global curRow
    global FileLabels_DB
    global MainLabelText_DB
    global NFilesLabelText_DB
    global OpenedDirs

    # Create File Dialog Box
    root.directoryname = filedialog.askdirectory(initialdir='./', title="Select Directory")

    MainLabelText_DB.set("")

    if not root.directoryname in OpenedDirs:
        OpenedDirs.append(root.directoryname)
        NFilesLabelText_DB.set("Added " + str(len(OpenedDirs)) + " Directories")
        newfilelabel = Label(root, text=root.directoryname)
        newfilelabel.grid(row=curRow, column=1)
        FileLabels_DB.append(newfilelabel)
        curRow += 1
    else:
        MainLabelText_DB.set("Dir already added.")

def SelectFileDialogBox_DBFile():
    global curRow
    global DBFile_Path
    global DBFile_Text
    global MainLabelText_DB

    # Create File Dialog Box
    root.filename = filedialog.askopenfilename(initialdir='./', title="Select DB File")

    MainLabelText_DB.set("")

    if not os.path.splitext(root.filename)[-1] == '.p': # Check if selected file is json
        MainLabelText_DB.set("Please select a proper pickle File.")
        return
    else:
        DBFile_Text.set('DB File: ' + root.filename)
        DBFile_Path = root.filename

def SelectFileDialogBox_CreateDBFile():
    global curRow
    global DBFile_Path
    global DBFile_Text
    global MainLabelText_DB

    # Create File Dialog Box
    root.dirname = filedialog.askdirectory(initialdir='./', title="Select DB File Dir")

    MainLabelText_DB.set("")

    DBFile_Path = os.path.join(root.dirname, 'PathDB.p')

    open(DBFile_Path, 'wb')

    DBFile_Text.set('DB File: ' + DBFile_Path)

    MainLabelText_DB.set("Created DBFile PathDB.p at " + root.dirname)    

def Add2DB():
    global OpenedDirs
    global DBFile_Path

    if not len(OpenedDirs) == 0:
        MainLabelText_DB.set("Adding Images...")
        ImageDatabase.SaveDatabase(DatabaseLocations=OpenedDirs, DBSaveFilePath=DBFile_Path)
        MainLabelText_DB.set("Finished Adding Images")
    else:
        MainLabelText_DB.set("Please select atleast one valid Image file to upload.")

def RemoveLastFile_DB():
    global OpenedDirs
    global FileLabels_DB
    global NFilesLabelText_DB

    if len(OpenedDirs) > 0:
        OpenedDirs.pop()
        FileLabels_DB[-1].grid_forget()
        FileLabels_DB.pop()
        if len(OpenedDirs) > 0:
            NFilesLabelText_DB.set("Added " + str(len(OpenedDirs)) + " Directories")
        else:
            NFilesLabelText_DB.set("No Dir Added")



# Main Code

# Details
OpenedDirs = []

# Init Root
print('Creating Window...')
root = Tk()
root.title('MemeCompress Database App')

# Create Window
CreateWindow()
print('Created Window')

root.mainloop()