import os
#=========================================================================================================================================#
# Date-Of-Code: 2018 - xx - xx
# Authors: datnt
# Descriptions:
# data is a 2-d array that need to be write to file
#==========================================================================================================================================#
def save_ndarray_to_text_file(data, dest_path):
  if len(data.shape) != 2:
    return False
  height, width = data.shape[0], data.shape[1]
  file = open(dest_path,'w')
  for r in range(height):
    for c in range(width):
      file.write("%f\t"%data[r,c])
    file.write("\n")
 file.close()
 return True
#=========================================================================================================================================#
