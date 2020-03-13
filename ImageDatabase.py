'''
Summary
This script is to organise the image database from which fill Images are taken
Add Image
Delete Image
Update FillImgs JSON Files / Refresh Database
Generate Basic FillImages
'''

import pickle
import os
from tqdm import tqdm

Images = []
ExtNames = ['.jpg', '.jpeg', '.png', '.pneg', '.bmp', '.tiff']

def SaveDatabase(DatabaseLocations=['MemeFormats'], DBSaveFilePath='PathDB.p'):
    global Images

    # Clean Database Dirs
    CleanDatabaseImages(DatabaseLocations)

    print("Started Indexing Image files...")
    for DatabaseLocation in tqdm(DatabaseLocations):
        for dirpath, dirnames, filenames in os.walk(DatabaseLocation):
            for filename in filenames:
                # Check extension
                extname = os.path.splitext(filename)[-1]
                if extname.lower() in ExtNames:
                    Images.append(os.path.join(dirpath, filename))
    print("Finished Indexing Image files.")
    
    print("Starting Saving DB...")
    pickle.dump(Images, open(DBSaveFilePath, 'wb'))
    print("Finished Saving DB.")

def ReadDatabase(DBSaveFilePath='PathDB.p'):
    global Images
    Images = pickle.load(open(DBSaveFilePath, 'rb'))
    return Images

def CleanDatabaseImages(DatabaseLocations=['MemeImages']):
    # Clean Image Name -
    print("Started Cleaning Image files...")
    for DatabaseLocation in tqdm(DatabaseLocations):
        for dirpath, dirnames, filenames in os.walk(DatabaseLocation):
            # print(dirpath)
            # print(dirnames)
            # print(filenames)
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                # 1) Remove '.' in names
                splitpath = os.path.splitext(filename)
                newfilepath = os.path.join(dirpath, splitpath[0].replace('.', '') + splitpath[1])
                if os.path.exists(filepath):
                    os.rename(filepath, newfilepath)
                else:
                    print("Doesnt exist", filepath)
    print("Finished Cleaning Image files.")


# Driver Code
DatabaseLocations = ['MemeFormats']
DBSaveFilePath = 'PathDB.p'

SaveDatabase(DatabaseLocations, DBSaveFilePath)
print("Saved", len(ReadDatabase(DBSaveFilePath)), "Images")

# SaveDatabase(['MemeImages'], 'MemeImgsDB.p')
# print("Saved", len(ReadDatabase('MemeImgsDB.p')), "Images")