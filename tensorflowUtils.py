import tensorflow as tf
import numpy as np
import stringUtils
import os
#=============================================================#
# Modified: 2018-06-26
# Author: datnt
# Descriptions#
# read a image in a directory specified by path_to_image_file
# return a TENSOR of image data.
def read_image_data(path_to_image_file):
    contents = tf.read_file(path_to_image_file)
    file_extern = stringUtils.get_file_extern(path_to_image_file)
    if file_extern == 'jpg':
        return tf.image.decode_jpeg(contents=contents)
    elif file_extern == 'png':
        return tf.image.decode_png(contents=contents)
    elif file_extern == 'bmp':
        return tf.image.decode_bmp(contents=contents)
    elif file_extern == 'gif':
        return tf.image.decode_gif(contents=contents)
    else:
        return False
#=============================================================#
# Modified: 2018-06-26
# Author: datnt
# Descriptions#
# read all image in a directory specified by path_to_dataset
# return a list of image data ndarray.
def read_image_dataset(path_to_dataset):
    image_list = stringUtils.list_image_files(path_to_dataset)
    num_image = len(image_list)
    if num_image >0:
        dataset = []
        for i in range(num_image):
            path_to_image_file = os.path.join(path_to_dataset, image_list[i])
            image_data = read_image_data(path_to_image_file=path_to_image_file)
            dataset.append(image_data)
        return dataset
    else:
        return False
#=============================================================#
# Modified: 2018-06-27
# Author: datnt
# Descriptions#
# Input a tensor flow dataset
# Return the number of elements in the dataset
def get_dataset_size(dataset):
    """Measure the number of elements in a tensorflow dataset"""
    dataset_iterator = dataset.make_one_shot_iterator()
    get_next_element = dataset_iterator.get_next()
    num_element = 0
    with tf.Session() as sess:
        while True:
            try:
                sess.run(get_next_element)
                num_element = num_element + 1
            except tf.errors.OutOfRangeError:
                print('End of elements in dataset')
                return num_element
#=============================================================#
# Modified: 2018-06-27
# Author: datnt
# Descriptions#
