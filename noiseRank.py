#!python
import os
import glob
import time
import sys
import numpy as np
import math
import cv2

from scipy.signal import convolve2d

def estimate_noise(I):

  H, W = I.shape

  M = [[1, -2, 1],
       [-2, 4, -2],
       [1, -2, 1]]

  sigma = np.sum(np.sum(np.absolute(convolve2d(I, M))))
  sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (W-2) * (H-2))
  
  return sigma
	
path = os.getcwd() #gets current directory
img_path = path + '/'+ sys.argv[1] #appends image file to current directory

img = cv2.imread(img_path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
noise = estimate_noise(img_gray)

noiseEstimate = estimate_noise(img_gray)
print 'noise is', noiseEstimate
