'''
Summary
Util Functions
'''
import numpy as np
from tqdm import tqdm
    


def NormalisedCorrelation(I, W):
    I_c = I.copy().astype(float)
    I_Corr = [0.0, 0.0, 0.0]

    if I.ndim == 2:
        I_c = np.reshape(I_c, (I_c.shape[0], I_c.shape[1], 1))

    I_bar = np.sum(np.sum(I_c, axis=1), axis=0) / (I_c.shape[0]*I_c.shape[1])
    W_bar = np.sum(np.sum(W, axis=1), axis=0) / (W.shape[0]*W.shape[1])
    SDProd = [1.0, 1.0, 1.0]
    for c in range(I.shape[2]):
        SDProd[c] = np.sum(np.sum((I_c[:, :, c] - I_bar[c])**2, axis=1), axis=0) ** (1/2)
        SDProd[c] *= np.sum(np.sum((W[:, :, c] - W_bar[c])**2, axis=1), axis=0) ** (1/2)

    for c in range(I_c.shape[2]):
        I_val = I_c[:, :, c] - I_bar[c]
        W_val = W[:, :, c] - W_bar[c]
        I_Corr[c] = np.sum(np.sum(np.multiply(I_val, W_val), axis=1), axis=0) / SDProd[c]

    return I_Corr

def NormaliseToRange(I, Range=(0, 255)):
    I_g = I.copy()
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1], 1))
    
    maxVal = np.max(np.max(I_g, axis=1), axis=0)
    minVal = np.min(np.min(I_g, axis=1), axis=0)

    minmaxRange = maxVal - minVal

    for i in range(I_g.shape[0]):
        for j in range(I_g.shape[1]):
            for c in range(I_g.shape[2]):
                I_g[i, j, c] = (((I_g[i, j, c] - minVal[c]) / minmaxRange) * (Range[1] - Range[0])) + Range[0]

    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))

    return I_g

def SortNormCorrVals(ImagePaths, NormCorrVals):
    NormCorrVals_c = NormCorrVals.copy()
    ImagePaths_c = ImagePaths.copy()
    n = len(NormCorrVals_c) 
  
    # Traverse through all array elements 
    for i in range(n): 
  
        # Last i elements are already in place 
        for j in range(0, n-i-1): 
  
            # traverse the array from 0 to n-i-1 
            # Swap if the element found is greater 
            # than the next element 
            if NormCorrVals_c[j] > NormCorrVals_c[j+1] : 
                NormCorrVals_c[j], NormCorrVals_c[j+1] = NormCorrVals_c[j+1], NormCorrVals_c[j]
                ImagePaths_c[j], ImagePaths_c[j+1] = ImagePaths_c[j+1], ImagePaths_c[j]
    return ImagePaths_c, NormCorrVals_c