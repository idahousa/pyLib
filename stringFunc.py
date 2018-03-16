#=============================================================#
#Modified: 2018-03-16
#Author: datnt
#Descriptions#
#Extract the extern of a file name.
#For example, abc/xyz.txt => should return 'txt'
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
