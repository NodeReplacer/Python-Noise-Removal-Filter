#! python

import numpy as np
from skimage import color, data, restoration

from PIL import Image
img = color.rgb2gray(data.astronaut())
from scipy.signal import convolve2d
import scipy.misc

psf = np.ones((5, 5)) / 25
img = convolve2d(img, psf, 'same')
img += 0.1 * img.std() * np.random.standard_normal(img.shape)
deconvolved_img = restoration.wiener(img, psf, 1100)
scipy.misc.imsave('new.png',deconvolved_img)
