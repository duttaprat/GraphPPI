from __future__ import division
import math, os
import numpy as np
import itertools

from sklearn.metrics import *
from scipy.spatial import distance

"""
    Compute Silhoutte Score of final population
"""
def silhoutte(self, individual):
    write_file_silhouette = open('silhouette.txt', 'a+')
    labels = np.argmax(individual.partition_matrix, axis=0)
    # print labels
    all_data_columnmatrix = np.vstack(self.individual_list)
    silhouette_avg = silhouette_score(all_data_columnmatrix, labels)
    #print silhouette_avg
    write_file_silhouette.write("Average Silhouette Score of chromosome is :"+str(silhouette_avg)+"\n")
    #print "The average silhouette_score for chromosome is :", silhouette_avg
    return silhouette_avg

