from __future__ import division
import math, os
import numpy as np
import itertools

from sklearn.metrics import *
from scipy.spatial import distance
from nsga2 import seq
from nsga2.problems.problem_definitions import ProblemDefinitions


ki=0
class ZDT3Definitions(ProblemDefinitions):

    def __init__(self, individual_list,individual_id_list,individual_ref_id_list,unique_protein_ref,
                 no_of_annotated_cluster,annotated_cluster_list,annotated_gene_list,
                 cooccurance_matrix, interaction_score_matrix):
        self.individual_list = individual_list
        self.individual_id_list = individual_id_list
        self.no_of_annotated_cluster = no_of_annotated_cluster
        self.annotated_cluster_list = annotated_cluster_list
        self.annotated_gene_list = annotated_gene_list
        self.cooccurance_matrix = cooccurance_matrix
        self.unique_protein_ref = unique_protein_ref
        self.individual_ref_id_list = individual_ref_id_list
        self.interaction_score_matrix = interaction_score_matrix

    """
    Compute Silhoutte Score of final population
    """
    def silhoutte(self, individual):
        #write_file_silhouette = open('silhouette.txt', 'a+')
        labels = np.argmax(individual.partition_matrix, axis=0)
        # print labels
        all_data_columnmatrix = np.vstack(self.individual_list)
        silhouette_avg = silhouette_score(all_data_columnmatrix, labels)
        #print silhouette_avg
        #write_file_silhouette.write("Average Silhouette Score of chromosome is :"+str(silhouette_avg)+"\n")
        #print "The average silhouette_score for chromosome is :", silhouette_avg
        return silhouette_avg


    """
    Compute Fuzzy Partition Coefficient as f1
    """
    def f1(self, individual):
        return individual.fpc
    """
    Compute PBM Score of each choromosome as f2
    """
    def f2(self, individual):
        individual_features = individual.features
        individual_length= int(len(individual_features)/individual.no_of_Cluster)
        centers = [individual_features[i:(i + individual_length)] for i in range(0, len(individual_features), individual_length)]
        distance_list = []
        for a, b in itertools.combinations(centers, 2):
            d1 = distance.euclidean(a, b)
            distance_list.append(d1)
        Dc = max(distance_list)
        Ec = np.sum(individual.partition_matrix * individual.distance_matrix)
        PBM_index = math.pow((Dc / (individual.no_of_Cluster * Ec)), 2)
        #print "PBM : ", PBM_index
        return PBM_index

    """
        Compute BHI Score of each choromosome as f3
    """
    def f3(self, individual):
        labels = np.argmax(individual.partition_matrix, axis=0)
        set_annotated_gene_list = set(self.annotated_gene_list)
        # print labels
        gene_data_matrix = np.zeros((individual.no_of_Cluster, len(self.individual_id_list)))
        c = [[] for i in range(individual.no_of_Cluster)]
        for i, (j, k) in enumerate(zip(labels, self.individual_id_list)):
            gene_data_matrix[j][i] = 1
            c[j].append(k)
        np.savetxt('gene_data_matrix.txt', gene_data_matrix, fmt='%d')
        gene_cooccurance_matrix = np.dot(gene_data_matrix.transpose(), gene_data_matrix)
        # exit()
        """
        for i in range(individual.no_of_Cluster):
            f = open(cluster_path + "cluster_" + str(i) + ".txt", "w+")
            for items in c[i]:
                f.write("%s \n" % items)
            f.close()
        """
        #print "test"
        d = []
        for i in range(individual.no_of_Cluster):
            set_cluster = set(c[i])
            n = len(set_cluster.intersection(set_annotated_gene_list))
            similarity = 0
            for subset in itertools.combinations(c[i], 2):
                if ((gene_cooccurance_matrix[self.individual_id_list.index(subset[0])]
                     [self.individual_id_list.index(subset[1])] != 0) and
                        (self.cooccurance_matrix[self.individual_id_list.index(subset[0])][self.individual_id_list.index(subset[1])] != 0)):
                    similarity += 1
            if (similarity != 0):
                d.append((1 / (n * (n - 1))) * similarity)
                # print "similatity " , similarity
                # print "intersection ", n
                # print "d[",i,"]", d
        summation_d = sum(d)
        BHI = (1 / individual.no_of_Cluster) * summation_d
        #print "BHI", BHI
        return BHI

    """
        Compute PPI interaction score as f4
    """
    def f4(self, individual):
        labels = np.argmax(individual.partition_matrix, axis=0)
        c = [[] for i in range(individual.no_of_Cluster)]
        for i, (j, k) in enumerate(zip(labels, self.individual_ref_id_list)):
            c[j].append(k)
        """
            for i in range(self.no_of_cluster):
                f = open(cluster_path + "cluster_" + str(i) + ".txt", "w+")
                for items in c[i]:
                    f.write("%s \n" % items)
                f.close()
        """
        d = []
        for i in range(individual.no_of_Cluster):
            set_cluster = set(c[i])
            for subset in itertools.combinations(set_cluster, 2):
                if ((subset[0] in self.unique_protein_ref) & (subset[1] in self.unique_protein_ref)):
                    x = self.unique_protein_ref.index(subset[0])
                    y = self.unique_protein_ref.index(subset[1])
                    # print x , y, self.interaction_score_matrix[x][y], self.interaction_score_matrix[y][x]
                    d.extend((float(self.interaction_score_matrix[x][y]), float(self.interaction_score_matrix[y][x])))

        int_score = sum(d)
        # print "Interaction Score", int_score
        return int_score
