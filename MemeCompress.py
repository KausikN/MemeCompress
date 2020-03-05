'''
Summary
Python Library for Meme Compression
'''
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pickle
from tqdm import tqdm

import Utils

# Utils


# Functions
def FindMemeFormat(Img, DBFilePath, MemeFormatSize=(256, 256, 3)):
    I_c = Img.copy()
    I_c_r = np.zeros(MemeFormatSize)
    I_MemeFormat_r = np.zeros(MemeFormatSize)

    MemeFormatSize = (MemeFormatSize[0], MemeFormatSize[1])

    # Resize Image to MemeFormatSize
    for c in range(I_c.shape[2]):
        I_c_r[:, :, c] = cv2.resize(I_c[:, :, c], MemeFormatSize, interpolation=cv2.INTER_LINEAR)

    # Load DB
    ImagePaths = pickle.load(open(DBFilePath, 'rb'))

    # Find Corr Vals for all images
    NormCorrVals = []
    for imgp in tqdm(ImagePaths):
        # Read and Resize MemeFormatImg
        I_MemeFormat = cv2.imread(imgp)
        
        for c in range(I_MemeFormat.shape[2]):
            I_MemeFormat_r[:, :, c] = cv2.resize(I_MemeFormat[:, :, c], MemeFormatSize, interpolation=cv2.INTER_LINEAR)

        # Find and Push NormCorr Value
        NormCorrVal = np.mean(np.array(Utils.NormalisedCorrelation(I_c_r, I_MemeFormat_r)))
        NormCorrVals.append(NormCorrVal)
        
    # Find Format with max NormCorrValue
    MaxCorrIndex = NormCorrVals.index(max(NormCorrVals))

    return cv2.imread(ImagePaths[MaxCorrIndex]), ImagePaths, NormCorrVals

# Driver Code

# Parameters
imgPath = 'MemeImages/Drake_Text_2.png'
DBFilePath = 'PathDB.p'

# Read img and find meme format
Img = cv2.imread(imgPath)
print(Img.shape)
I_MemeFormat, ImagePaths, NormCorrVals = FindMemeFormat(Img, DBFilePath, (128, 128, 3))

# Sort and display values
ImagePaths_Sorted, NormCorrVals_Sorted = Utils.SortNormCorrVals(ImagePaths, NormCorrVals)
print("Sorted Norm Corr Values:")
# Display Values
for p, v in zip(ImagePaths_Sorted, NormCorrVals_Sorted):
    print(p, ":", str(v))

# Display
ax = plt.subplot(2, 1, 1)
ax.title.set_text("Original Meme")
plt.imshow(cv2.cvtColor(Img, cv2.COLOR_BGR2RGB))
ax = plt.subplot(2, 1, 2)
ax.title.set_text("Meme Format")
plt.imshow(cv2.cvtColor(I_MemeFormat, cv2.COLOR_BGR2RGB))
plt.show()