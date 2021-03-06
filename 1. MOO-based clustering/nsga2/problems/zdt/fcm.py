import numpy as np
import os, math 
import skfuzzy as fuzz
import random

i = 0 ;
class FCM(object):

    def __init__(self,  all_data_matrix,individual_no):
        self.all_data_matrix = all_data_matrix
        self.individual_no = individual_no

    def FuzzyCMeans(self):
        print len(self.all_data_matrix[0])
        max_no_cluster = int(math.sqrt(len(self.all_data_matrix[0]))) 
        x = random.randint(2, max_no_cluster)
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(self.all_data_matrix, x , 2, error=0.005, maxiter=10, init=None)
        label = np.argmax(u, axis=0)
        label_list= []
        for j in label:
            label_list.append(j)
        global i
        if (i<self.individual_no):
            folder_path = "Output_data/Individual" + str(i)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            np.savetxt((str(folder_path + '/choromosome.txt')), cntr, fmt='%-7.2f')
            np.savetxt((str(folder_path + '/final_partition_matrix.txt')), u, fmt='%-7.2f')
            np.savetxt((str(folder_path + '/initial_partition_matrix.txt')), u0, fmt='%-7.2f')
            np.savetxt((str(folder_path + '/euclidean_distance_matrix.txt')), d, fmt='%-7.2f')

            #print "fpc", fpc
            i +=1
        return cntr,u,d, fpc,x, label_list


        #print individual.features
