import sklearn
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#=========================================================================================================================================#
#Date-Of-Code: 2018 - xx - xx
#Author:
#Descriptions:
#Perform a principal component analysis on input data
#=> Find the new coordinate system by which the data are best represented by maximizing the variance of each data classes in the new system
# data is the table of data. DO NOT need to be normalized before using PCA
# Ref: http://scikit-learn.org/stable/auto_examples/decomposition/plot_pca_vs_lda.html#sphx-glr-auto-examples-decomposition-plot-pca-vs-lda-py
#=========================================================================================================================================#
def perform_pca(data, num_components):
  pca = PCA(n_components = num_components)
  pca.fit(data)
  return pca

def pca_transform(data, pca_kernel):
  return pca_kernel.transform(data)
#=========================================================================================================================================#
#Date-Of-Code: 2018 - xx - xx
#Author:
#Descriptions:
#Perform a linear discriminant analysis on input data
#=> Find the new coordinate system by which the data are best represented and the data of classeses are largestly separated
# data is the table of data. DO NOT need to be normalized before using LDA
# Ref: http://scikit-learn.org/stable/auto_examples/decomposition/plot_pca_vs_lda.html#sphx-glr-auto-examples-decomposition-plot-pca-vs-lda-py
#=========================================================================================================================================#
def perform_ldb(data, groundtruth_label, num_components):
  lda = LinearDiscriminantAnalysis(n_components = num_components)
  lda.fit(data,groundtruth_label)
  return lda

def lda_transform(data, lda_kernel):
  return lda_kernel.transform(data)
#=========================================================================================================================================#
#Date-Of-Code: 2018 - xx - xx
#Author:
#Descriptions:
#=========================================================================================================================================#
