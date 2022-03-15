#!python
import os
import glob
import time
import sys
import numpy

from imageIO import *
from rank_NEI import *
from imenh_lib import *
from imfilter_lib import *

def calcRankMetric(image):
	#Calculate ranks noise estimation index
	NEI_metric = rank_NEI(image)
	return NEI_metric

def enh_alphaTMean(im,alpha,n=5):
    img = numpy.zeros(im.shape,dtype=numpy.int16)
    
    v = (n-1)/2
    
    # Calculate the trim coefficient
    b = int((n*n)*(alpha))
    
	# Process the image
    for i in range(0,im.shape[0]):
        for j in range(0,im.shape[1]):
            # Extract the window area
            block = im[max(i-v,0):min(i+v+1,im.shape[0]), max(j-v,0):min(j+v+1,im.shape[1])]

            # Reshape the neighborhood into a vector by flattening the 2D block
            wB = block.flatten()
            
            # Sort the vector into ascending order
            wB = numpy.sort(wB)
            len = wB.size
            
            # Trim b elements from each end of the vector
            if (b != 0):
                nwB = wB[b:len-b]
    
            # Calculate the mean of the trimmed vector
            tMean = nwB.mean()

            # Assign the values
            if (tMean > 0):
                img[i][j] = int(tMean)
	return img

def alpha_filter(image,alpha):
	alpha = float(alpha)
	result_img = enh_alphaTMean(image,alpha,5)
	return result_img
	
def convertGray(image_path):
	img = imread_gray(image_path)
	return img


img_ext = sys.argv[1].find(".")
filter_type = sys.argv[2]
if(filter == "alpha"):
	if(sys.argv[3] == None):
		print "Must enter an integer number\nFormat: pic.ext alpha [1.41]"
		sys.exit()
	else:
		print "WE DID IT"
else:
	print "NOT ALPHA FILTER"

if(img_ext > 0 ):
	path = os.getcwd() #gets current directory
	img_path = path + '/'+ sys.argv[1] #appends image file to current directory
	img = convertGray(img_path) #reads gray scale image and returns 8bit 2d array
	before_rank = calcRankMetric(img)
	if(filter_type == "mode"):
		#method performs mode filtering
		print "\nPerforming mode filtering"
		mode_img = mode_filter(img)
		print "Rank before",before_rank
		after_rank = calcRankMetric(mode_img)
		print "Rank after",after_rank
		saveFile(mode_img,sys.argv[1],"mode")
	elif(filter_type == "hybrid"):
		print "\nPerforming hybrid filtering"
		#method performs hybrid filtering best with (Rayleigh images)
		hybrid_img = hybrid_filter(img)
		print "Rank before",before_rank
		after_rank = calcRankMetric(hybrid_img)
		print "Rank after",after_rank
		saveFile(hybrid_img,sys.argv[1],"hybrid")
	elif(filter_type == "alpha"):
		if(sys.argv[3] == None):
			print "Must enter an alpha number"
		else:
			print "\nPerforming alpha trim filtering"
			#method performs alpha trimmed filtering (best with Gaussian images)
			alpha_img = alpha_filter(img,sys.argv[3])
			#print "Rank before",before_rank
			after_rank = calcRankMetric(alpha_img)
			print "Rank after",after_rank
			path = sys.argv[3]+sys.argv[1]
			saveFile(alpha_img,path,"alpha")
	elif(filter_type == "gaussian"):
		print "\nPerforming gaussian filtering"
		if(sys.argv[3] == None and sys.argv[4] == None):
			print "Must enter an integer and a whole number"
		else:       
			#method performs Gaussian filtering (image smoothing)
			gaus_im = gaus_filter(img,sys.argv[3],sys.argv[4])
			print "Rank before",before_rank
			after_rank = calcRankMetric(gaus_im)
			print "Rank after",after_rank               
			path = sys.argv[4]+sys.argv[1]
			saveFile(gaus_im,path,"gaus")
	else:
		print "Incorrect argument for filter_type:\nOptions: alpha\nmode\nhybrid\ngaussian"

	dispHisto(img)	
else:
	print "Invalid extension: example(.tif, .png, .jpeg)"
