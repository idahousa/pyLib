from skimage import io
from skimage import data
from skimage import measure
from skimage import transform
from skimage.feature import local_binary_pattern
import numpy as np
import cv2
#=======================================================================================================================================#
#Date-of-code: 2018-03-19
#Author: datnt
#Description:
#Accumulate the histogram of an gray-scale image or 2-d array
#The data-type of input_image must be integer values
#=======================================================================================================================================#
def accumulate_histogram_features(image):
    max_val = image.max() + 1
    if max_val < 2:
        #Maximum input value is 1 => Wrong input data
        return -1
    hist, bins = np.histogram(image.ravel(), int(max_val))
    return hist, bins
#=======================================================================================================================================#
#Date-of-code: 2018-03-19
#Author: datnt
#Description:
#Extract the uniform and non-uniform rotation invariant lbp features for a gray-scale image by dividing
#the input image into (M,N) sub-block.
#If num_blk_height=1 and num_blk_with = 1 => Extract features for entire image
#Parameters
# image      : input gray-scale image
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
#=======================================================================================================================================#
def lbp_riu_global_lobal_features(image, resolution, radius, method='default', num_blk_height=1, num_blk_width=1, overlapped_ratio=0):
    height, width = image.shape
    if (overlapped_ratio <0 or overlapped_ratio >=1 or num_blk_height <=0 or num_blk_width <=0):
        return -1
    lbp_image = local_binary_pattern(image, resolution, radius, method=method)
    blk_width = int(width / num_blk_width) + 1
    blk_height = int(height / num_blk_height) + 1
    overlapped_height = int(blk_height * overlapped_ratio)
    overlapped_width = int(blk_width * overlapped_ratio)
    index = 0
    for r in range(0, height, blk_height):
        for c in range(0, width, blk_width):
            x_start = c - overlapped_width
            y_start = r - overlapped_height
            x_end = x_start + blk_width + 2*overlapped_width
            y_end = y_start + blk_height + 2*overlapped_height
            if x_start<0:x_start=0
            if y_start<0:y_start=0
            if x_end>=width:x_end = width - 1
            if y_end>=height:y_end = height - 1
            sub_lbp_image = lbp_image[y_start:y_end, x_start:x_end]
            sub_hist, sub_bins = accumulate_histogram_features(sub_lbp_image)
            if index ==0:
                hist = sub_hist
            else:
                hist = np.concatenate((hist,sub_hist), axis=0)
            index +=1
            #<For Debug Purpose>
            #dst_path = 'data_files/test_{}.bmp'.format(index)
            #cv2.imwrite(dst_path,sub_lbp_image)
    return hist  
#=======================================================================================================================================#
#Date-of-code: 2018-03-20
#Author: datnt
#Description:
#Object labelling of binarized image
#image : an 2-d binarized image that has two value of 0 (background) and 255 (objects- foreground)
#Output: the labeled image, the number of object and corresponding size
#This function performs same action as the object_labelling in the c code in my previous studies
def object_labelling(image):
    if len(image.shape) != 2:
        return -1
    label_image = measure.label(image)
    num_objects = label_image.max()
    objects_size = []
    for i in range(1, num_objects + 1):
        obj_size = np.sum(label_image == i)
        objects_size.append(obj_size)
    return label_image, num_objects, objects_size
#=======================================================================================================================================#
#Date-of-code: 2018-03-20
#Author: datnt
#Description:
#Rotate an image arround an center. This function is same as the skimage.transform.rotate() function
#However, this function additionally return the transformation function that can be futher used
#to calculate the new locations of some landmark points
#Reference: https://github.com/scikit-image/scikit-image/blob/master/skimage/transform/_warps.py#L285
#Please import the transform module by using "from skimage import transform" statement
def rotate_image(image, angle, resize=False, center=None, order=1, mode='constant', cval=0, clip=True, preserve_range=False):
    rows, cols = image.shape[0], image.shape[1]
    # rotation around center
    if center is None:
        center = np.array((cols, rows)) / 2. - 0.5
    else:
        center = np.asarray(center)
    tform1 = transform.SimilarityTransform(translation=center)
    tform2 = transform.SimilarityTransform(rotation=np.deg2rad(angle))
    tform3 = transform.SimilarityTransform(translation=-center)
    tform = tform3 + tform2 + tform1
    output_shape = None
    if resize:
        # determine shape of output image
        corners = np.array([[0, 0],
                            [0, rows - 1],
                            [cols - 1, rows - 1],
                            [cols - 1, 0]])
        corners = tform.inverse(corners)
        minc = corners[:, 0].min()
        minr = corners[:, 1].min()
        maxc = corners[:, 0].max()
        maxr = corners[:, 1].max()
        out_rows = maxr - minr + 1
        out_cols = maxc - minc + 1
        output_shape = np.ceil((out_rows, out_cols))

        # fit output image in new shape
        translation = (minc, minr)
        tform4 = transform.SimilarityTransform(translation=translation)
        tform = tform4 + tform
    r_image = transform.warp(image, tform, output_shape=output_shape, order=order,mode=mode, cval=cval, clip=clip, preserve_range=preserve_range)
    return r_image, tform
#=======================================================================================================================================#
#Date-of-code: 2018-03-20
#Author: datnt
#Description:
#This function is used after the use of rotate_image() function above to calculate the new coordinate of a given pixel
#of original images in the rotated image.
#A given pixel is in format of [row, column].
"""
Example:
>> image = data.camera()
>> image[ 210:220, 400:410] = 255
>> ri_image, tform = rotate_image(image,-10,resize=True)
>> new_coordinate = cal_coordinate_of_pixel_in_rotated_image(tform=tform,pixel_coordinate = [215, 405])
>> print(new_coordinate)
>> io.imshow(ri_image)
>> io.show()
"""
def cal_coordinate_of_pixel_in_rotated_image(tform, pixel_coordinate):
    point_array = np.array([[pixel_coordinate[1], pixel_coordinate[0]]])
    return tform.inverse(point_array)
#=======================================================================================================================================#














