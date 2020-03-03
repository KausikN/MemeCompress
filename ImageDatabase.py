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

def SaveDatabase(DatabaseLocations=['MemeImgs'], DBSaveFilePath='PathDB.p'):
    global Images

    print("Started Indexing Image files...")
    for DatabaseLocation in tqdm(DatabaseLocations):
        for dirpath, dirnames, filenames in os.walk(DatabaseLocation):
            for filename in filenames:
                Images.append(os.path.join(dirpath, filename))
    print("Finished Indexing Image files.")
    
    print("Starting Saving DB...")
    pickle.dump(Images, open(DBSaveFilePath, 'wb'))
    print("Finished Saving DB.")

def ReadDatabase(DBSaveFilePath='PathDB.p'):
    global Images
    Images = pickle.load(open(DBSaveFilePath, 'rb'))
    return Images

# Driver Code
DatabaseLocations = ['MemeImgs']
DBSaveFilePath = 'PathDB.p'

SaveDatabase(DatabaseLocations, DBSaveFilePath)
print(ReadDatabase(DBSaveFilePath))