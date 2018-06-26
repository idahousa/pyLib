import os
#=============================================================#
#Modified: 2018-03-16
#Author: datnt
#Descriptions#
#Extract the extern of a file name.
#For example, file_name = 'abc/xyz.txt' => should return 'txt'
def get_file_extern(file_name):
    file_len = len(file_name)
    index = 0
    for i in range(1,file_len):
        if(file_name[-i]=='.'):
            index = -i+1
            break
    if index ==0:
        return 'error'
    else:
        return file_name[index:file_len]
#=============================================================#
#Modified: 2018-03-16
#Author: datnt
#Descriptions#
#List all the files in a given directory.
#Example: directory_path = 'data'. And you put some files in this directory
def list_files_in_directory(directory_path):
    return os.listdir(directory_path)
#=============================================================#
#Modified: 2018-03-16
#Author: datnt
#Descriptions#
#Make a list of all image files in a given directory#
def list_image_files(directory_path):
    rtn_list = []
    file_extern_list = ['bmp','BMP','jpg','JPG','jpeg','JPEG','tiff','TIFF','PNG','png','gif','GIF']
    all_file_list = list_files_in_directory(directory_path)
    for file_name in all_file_list:
        file_extern = get_file_extern(file_name)
        if file_extern in file_extern_list:
            rtn_list.append(file_name)
            
    return rtn_list
#=============================================================#
#Modified: 2018-03-16
#Author: datnt
#Descriptions#
#Make a list of all image files in a given directory#
#The extern of image file is "file_extern".
#Example: list_image_files_with_given_extern('data','jpg') => list all jpeg file in 'data' directory.
def list_files_with_given_extern(directory_path, file_extern):
    rtn_list = []
    file_extern_list = [file_extern]
    all_file_list = list_files_in_directory(directory_path)
    for file_name in all_file_list:
        file_extern = get_file_extern(file_name)
        if file_extern in file_extern_list:
            rtn_list.append(file_name)
    return rtn_list
#=============================================================#
# Modified: 2018-03-19
# Author: datnt
# Descriptions#
#Write a list of string to file#
def write_list_of_string_to_file(input_list,dest_path):
    file = open(dest_path,'w')
    for item in input_list:
        file.write("%s\n"%item)
    file.close()
    return
#=============================================================#
# Modified: 2018-06-26
# Author: datnt
# Descriptions#
# read a image in a directory specified by path_to_image_file
# return a TENSOR of image data.
def read_image_data(path_to_image_file):
    contents = tf.read_file(path_to_image_file)
    file_extern = get_file_extern(path_to_image_file)
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
    image_list = list_image_files(path_to_dataset)
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
    
    
