from function import is_number
import numpy as np
def preprocess(dataset_path):
    read_file = open(dataset_path, 'r');
    write_file_population = open('Intermediate_Data/Initial_population.txt', 'w')
    write_file_population_id = open('Intermediate_Data/population_labels.txt', 'w')
    file_content = read_file.read();
    read_file.close();

    # Contains all N population in a list
    all_data = file_content.splitlines();

    individual_list = []  # Contains all the gene
    individual_labels_list = [];  # Contains gene id list

    for lines in all_data:
        individual = []  # contains the values of individual
        individual_labels = [];  # contains the id values of individual
        values = lines.split()
        check = 0
        for i in values:
            if(is_number(i) == 1):
                int_i = float(i);  # convert string to integer
                check += 1
                if (check<=2):
                    individual.append(int_i)
                else:
                    individual_labels.append(int_i)

        if (len(individual) > 0):
            individual_list.append(list(individual))  # Create a list that contains all the individual
        if (len(individual_labels)>0):
            individual_labels_list.append(list(individual_labels))

    for item in individual_list:
        write_file_population.write("\n %s" % item)

    for item in individual_labels_list:
        write_file_population_id.write("\n %s" % item)

    return individual_list

def preprocess_fcm_datamatrix(individual_list):
    datapnts_list = []
    for list in range(2):  # create list of list that contains 2 list to contain all 2 dimension datpoints
        datapnts_list.append([])

    '''
    Generate 2D matrix that can be fed to FCM algorithm
    '''
    all_data = []
    for cols in range(2):
        for rows in individual_list:
            datapnts_list[cols] = np.hstack((datapnts_list[cols], rows[cols]))
        # print datapnts_list[cols]
        all_data.append(datapnts_list[cols])
    all_data_matrix = np.vstack((all_data))
    np.savetxt('Intermediate_Data/matrix_data.txt', all_data_matrix, fmt='%-7.2f')
    return all_data_matrix
