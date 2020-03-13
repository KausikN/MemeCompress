'''
Summary
Python Library for Meme Compression
'''
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from tqdm import tqdm

import Utils

# Utils


# Functions
def FindMemeFormat(Img, DBFormatPath, MemeFormatSize=(256, 256, 3), progressBar=True):
    I_c = Img.copy()
    I_c_r = np.zeros(MemeFormatSize)
    I_MemeFormat_r = np.zeros(MemeFormatSize)

    MemeFormatSize = (MemeFormatSize[0], MemeFormatSize[1])

    # Resize Image to MemeFormatSize
    for c in range(I_c.shape[2]):
        I_c_r[:, :, c] = cv2.resize(I_c[:, :, c], MemeFormatSize, interpolation=cv2.INTER_LINEAR)

    # Load DB
    ImagePaths = pickle.load(open(DBFormatPath, 'rb'))

    # Find Corr Vals for all images
    NormCorrVals = []
    if progressBar:
        for imgp in tqdm(ImagePaths):
            # Read and Resize MemeFormatImg
            I_MemeFormat = cv2.imread(imgp)
            if I_MemeFormat is None:
                print(imgp, "is not available.")
                continue

            for c in range(I_MemeFormat.shape[2]):
                I_MemeFormat_r[:, :, c] = cv2.resize(I_MemeFormat[:, :, c], MemeFormatSize, interpolation=cv2.INTER_LINEAR)

            # Find and Push NormCorr Value
            NormCorrVal = np.mean(np.array(Utils.NormalisedCorrelation(I_c_r, I_MemeFormat_r)))
            NormCorrVals.append(NormCorrVal)
    else:
        for imgp in ImagePaths:
            # Read and Resize MemeFormatImg
            I_MemeFormat = cv2.imread(imgp)
            if I_MemeFormat is None:
                print(imgp, "is not available.")
                continue

            for c in range(I_MemeFormat.shape[2]):
                I_MemeFormat_r[:, :, c] = cv2.resize(I_MemeFormat[:, :, c], MemeFormatSize, interpolation=cv2.INTER_LINEAR)

            # Find and Push NormCorr Value
            NormCorrVal = np.mean(np.array(Utils.NormalisedCorrelation(I_c_r, I_MemeFormat_r)))
            NormCorrVals.append(NormCorrVal)
        
    # Find Format with max NormCorrValue
    MaxCorrIndex = NormCorrVals.index(max(NormCorrVals))

    return cv2.imread(ImagePaths[MaxCorrIndex]), ImagePaths, NormCorrVals

def ClassifyMemes2Formats(DBImagePath='MemeImgsDB.p', DBFormatPath='PathDB.p', SavePath='MemeClassifications'):
    if os.path.exists(DBImagePath):
        Images = pickle.load(open(DBImagePath, 'rb'))
        for imgp in tqdm(Images):
            Img = cv2.imread(imgp)
            I_MemeFormat, ImagePaths, NormCorrVals = FindMemeFormat(Img, DBFormatPath, (256, 256, 3), progressBar=False)
            # Sort and display values
            ImagePaths_Sorted, NormCorrVals_Sorted = Utils.SortNormCorrVals(ImagePaths, NormCorrVals)
            nCols = 5
            DisplayTopMatches(Img, ImagePaths_Sorted, NormCorrVals_Sorted, nMatches=nMatches, nCols=nCols)
            savename = os.path.basename(os.path.splitext(imgp)[0]).replace('/', '--')
            plt.savefig(os.path.join(SavePath, savename) + '_Class' + '.png')
            plt.clf()


def DisplayTopMatches(Img, ImagePaths_Sorted, NormCorrVals_Sorted, nMatches=5, nCols=5):
    ax = plt.subplot((1 + Utils.ceil(nMatches/nCols)), nCols, 1)
    ax.title.set_text("Original Meme")
    plt.imshow(cv2.cvtColor(Img, cv2.COLOR_BGR2RGB))
    for i in range(nMatches):
        ax = plt.subplot((1 + Utils.ceil(nMatches/nCols)), nCols, (nCols+i) + 1)
        ax.title.set_text(str(i+1) + " - " + str(round(NormCorrVals_Sorted[-(i+1)], 2)))
        plt.imshow(cv2.cvtColor(cv2.imread(ImagePaths_Sorted[-(i+1)]), cv2.COLOR_BGR2RGB))


# Driver Code

# Parameters
DBImagePath = 'MemeImgsDB.p'
DBFormatPath = 'PathDB.p'
SavePath = 'MemeClassifications'
nMatches = 5

ClassifyMemes2Formats(DBImagePath, DBFormatPath, SavePath)
quit()
"""
# Parameters
imgPath = 'MemeImages/Drake_Text_2.png'
intermediate_imgPath = imgPath.replace('/', '--')

# Read img and find meme format
Img = cv2.imread(imgPath)
print(Img.shape)

# Check if intermediate stage exists
if os.path.exists('Intermediate_' + intermediate_imgPath + "_ImagePaths_Sorted.p") and os.path.exists('Intermediate_' + intermediate_imgPath + "_ImagePaths_Sorted.p"):
    ImagePaths_Sorted = pickle.load(open('Intermediate_' + intermediate_imgPath + '_ImagePaths_Sorted.p', 'rb'))
    NormCorrVals_Sorted = pickle.load(open('Intermediate_' + intermediate_imgPath + '_NormCorrVals_Sorted.p', 'rb'))

else:
    I_MemeFormat, ImagePaths, NormCorrVals = FindMemeFormat(Img, DBFormatPath, (128, 128, 3))

    # Sort and display values
    ImagePaths_Sorted, NormCorrVals_Sorted = Utils.SortNormCorrVals(ImagePaths, NormCorrVals)
    # print("Sorted Norm Corr Values:")
    # # Display Values
    # for p, v in zip(ImagePaths_Sorted, NormCorrVals_Sorted):
    #     print(p, ":", str(v))

    # Intermediate Stage Pickling
    pickle.dump(ImagePaths_Sorted, open('Intermediate_' + intermediate_imgPath + '_ImagePaths_Sorted.p', 'wb'))
    pickle.dump(NormCorrVals_Sorted, open('Intermediate_' + intermediate_imgPath + '_NormCorrVals_Sorted.p', 'wb'))

# Display
nCols = 5
DisplayTopMatches(Img, ImagePaths_Sorted, NormCorrVals_Sorted, nMatches=nMatches, nCols=nCols)
plt.show()
"""