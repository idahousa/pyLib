import os
#=============================================================#
#Modified: 2018-03-16
#Author: datnt
#Descriptions#
#Extract the extern of a file name.
#For example, file_name = 'abc/xyz.txt' => should return 'txt'
def file_extern(file_name):
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
#Modified: 2018-xx-xx
#Author: datnt
#Descriptions#
