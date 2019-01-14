"""
Preprocessed the microarray dataset
"""
from function import is_number
import numpy as np
def preprocess(dataset_path):
    read_file = open(dataset_path, 'r');
    write_file_population = open('Intermediate_Data/Initial_population.txt', 'w')
    write_file_population_id = open('Intermediate_Data/population_id.txt', 'w')
    file_content = read_file.read();
    read_file.close();

    # Contains all N population in a list
    all_data = file_content.splitlines()

    individual_list = []        # Contains all the gene
    individual_id_list = [];    # Contains gene id list
    individual_ref_id = [];     # contains the reference identifier

    for lines in all_data:
        individual = []             # contains the values of individual
        individual_id = [];         # contains the id values of individual
        values = lines.split()
        for i in values:
            if (is_number(i) == 1):
                int_i = float(i);   # convert string to integer
                individual.append(int_i)
            else:
                individual_id.append(i.upper())

        if (len(individual) > 0):
            individual_list.append(list(individual))  # Create a list that contains all the individual
        if (len(individual_id) > 0):
            individual_id_list.append(list(individual_id[0:1]))
            individual_ref_id.append(list(individual_id[1:2]))

    individual_length = len(individual_list[1])
    #print individual_length

    for item in individual_list:
        write_file_population.write("%s \n" % item)

    individual_id_list1 = []
    individual_ref_id_list = []
    for item in individual_ref_id:
        for x in item:
            individual_ref_id_list.append(x)
    for item in individual_id_list:
        for x in item:
            individual_id_list1.append(x)
            write_file_population_id.write("%s \n" % x)

    #print individual_ref_id_list
    #print len(individual_ref_id_list) , len(individual_id_list1)
    return individual_length, individual_list, individual_id_list1, individual_ref_id_list


def preprocess_fcm_datamatrix(individual_len, individual_list):
    datapnts_list = []
    normalized_datapnts_list = []
    #print individual_len
    for list in range(individual_len):  # create list of list that contains 21 list to contain all 21 dimension datpoints
        datapnts_list.append([])
        normalized_datapnts_list.append([])

    '''
    Generate 2D matrix that can be fed to FCM algorithm
    '''
    all_normalized_data = []
    all_data = []
    for cols in range(individual_len):
        for rows in individual_list:
            datapnts_list[cols] = np.hstack((datapnts_list[cols], rows[cols]))
        #print datapnts_list[cols]
        max_num = max(datapnts_list[cols])
        min_num = min(datapnts_list[cols])
        #print max_num , min_num
        normalized_datapnts_list[cols] = [(x - min_num) / (max_num - min_num) for x in datapnts_list[cols]]
        all_data.append(datapnts_list[cols])
        all_normalized_data.append(normalized_datapnts_list[cols])
    all_data_matrix = np.vstack((all_data))
    all_normalized_data_matrix = np.vstack((all_normalized_data))
    np.savetxt('Intermediate_Data/matrix_data.txt', all_data_matrix, fmt='%-7.2f')
    np.savetxt('Intermediate_Data/matrix_normalized_data.txt', all_normalized_data_matrix, fmt='%-7.2f')
    return all_data_matrix, all_normalized_data_matrix


def AnnotatedClustering(individual_id_list):
    #print individual_id_list
    read_file = open('Input_data/Full_annotated_clustering.txt', 'r')
    write_annotated_gene_list = open('Intermediate_Data/Annotated_Clustering/annotated_gene_list.txt', 'w')
    file_content = read_file.read()

    # Splitting into cluster
    all_cluster = file_content.split("\n\n")
    no_of_annotated_cluster = len(all_cluster)
    data_matrix = np.zeros((no_of_annotated_cluster, len(individual_id_list)))
    annotated_cluster_lists = [[] for i in range(no_of_annotated_cluster)]

    for i in range(no_of_annotated_cluster):
        f = open("Intermediate_Data/Annotated_Clustering/annotated_cluster" + str(i) + ".txt", "w")
        lines = all_cluster[i].splitlines()
        contents = lines[2].split('\t')
        gene_ids = contents[5].split(', ')
        for k in gene_ids:
            annotated_cluster_lists[i].append(k)
            data_matrix[i][individual_id_list.index(k)] = 1

        for items in annotated_cluster_lists[i]:
            f.write("%s \n" % items)
        f.close()

    np.savetxt('data_matrix.txt', data_matrix, fmt='%d')
    cooccurance_matrix = np.dot(data_matrix.transpose(), data_matrix)
    np.savetxt('cooccurance_matrix.txt', cooccurance_matrix, fmt='%d')
    annotated_gene_list = list(set.union(*map(set, annotated_cluster_lists)))
    #print len(annotated_gene_list)
    for item in annotated_gene_list:
        write_annotated_gene_list.write("%s \n" % item)

    return no_of_annotated_cluster, annotated_cluster_lists ,annotated_gene_list, cooccurance_matrix


def Confidence_Score_Matrix():
    bad_words = ['NA', 'NA\n']
    with open('Input_data/network_scored.tsv') as oldfile, open('Intermediate_Data/pp_ntwrk_scored.txt', 'w') as newfile:
        for line in oldfile:
            words = line.split('\t')

            if not any(bad_word in words for bad_word in bad_words):
                newfile.write(line)

    read_file = open('Intermediate_Data/pp_ntwrk_scored.txt', 'r');
    file_content = read_file.read()
    all_lines = file_content.split('\n')

    vertical_list = []
    for i in range(3):
        vertical_list.append([])

    for i in all_lines:
        split_lines = i.split('\t')
        #print split_lines, len(split_lines)
        if (len(split_lines) == 3):
            for j in range(3):
                if j == 2:
                    vertical_list[j].append(float(split_lines[j]))
                else:
                    vertical_list[j].append(split_lines[j])

    #print len(vertical_list[2]), len(vertical_list[0]), len(vertical_list[1])
    unique_ptn1 = set(vertical_list[0])
    unique_ptn2 = set(vertical_list[1])
    # print len(unique_ptn1) , len(unique_ptn2)
    unique_protein = list(unique_ptn1.union(unique_ptn2))

    interaction_score_matrix = np.zeros([len(unique_protein), len(unique_protein)])
    #print vertical_list[2]
    # print vertical_list[0]
    normalized_intscore = []
    max_num = max(vertical_list[2])
    min_num = min(vertical_list[2])
    for x in vertical_list[2]:
        norm_x = (x - min_num) / (max_num - min_num)
        normalized_intscore.append(norm_x)

    for i, (j, k) in enumerate(zip(vertical_list[0], vertical_list[1])):
        interaction_score_matrix[unique_protein.index(j)][unique_protein.index(k)] = normalized_intscore[i]

    return unique_protein , interaction_score_matrix