import skimage
from skimage import io
from skimage import local_binary_pattern
from skimage import data
import numpy as np
#===================================================================================================#
#Date-of-code: 2018-xx-xx
#Author: datnt
#Description:
#Accumulate the histogram of an gray-scale image
#===================================================================================================#
def histogram_features(input_image):
  max_val = input_image.max() + 1
  hist, bins = np.histogram(input_image.ravel(), bins = max_val)
  return hist
#===================================================================================================#
#Date-of-code: 2018-xx-xx
#Author: datnt
#Description:
#Extract the uniform and non-uniform rotation invariant lbp features for a gray-scale image by dividing
#the input image into (M,N) sub-block.
#If num_blk_height=1 and num_blk_with = 1 => Extract features for entire image
#Parameters-----------------------------------------------------------------------------------------
# input_image: input gray-scale image
# resolution : number of surrounding pixels of lbp operator
# radius     : the radius of lbp circle
# method     : method to be used for extracting lbp features.
#              => Use 'uniform" for uniform and non-uniform rotation invariant lbp features
#              => Use 'nri_uniform" for uniform and non-uniform lbp features
#              => Use 'default' for conventional lbp features
#              => Use 'ror' for conventional rotation invariant lbp features
# num_blk_height: number of sub-blocks in vertical direction
# num_blk_width : number of sub-blocks in horizontal direction
# overlapped_ratio: A value from 0 to 1 that indicates the overlapped ratio of sub-blocks.
#===================================================================================================#
def lbp_riu_global_lobal_hist_features(input_image, resolution, radius, method = 'default', num_blk_height, num_blk_width,overlapped_ratio = 0):
  
  


  
  



