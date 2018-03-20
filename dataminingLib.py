import sklearn
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#=========================================================================================================================================#
#Date-Of-Code: 2018 - xx - xx
#Author:
#Descriptions:
#Perform a principal component analysis on input data
#=> Find the new coordinate system by which the data are best represented by maximizing the variance of each data classes in the new system
#=========================================================================================================================================#
def perform_pca(data, num_components):
  

  

#=========================================================================================================================================#
#Date-Of-Code: 2018 - xx - xx
#Author:
#Descriptions:
#Perform a linear discriminant analysis on input data
#=> Find the new coordinate system by which the data are best represented and the data of classeses are largestly separated
#=========================================================================================================================================#
def perform_ldb(data, groundtruth_label, num_components):
