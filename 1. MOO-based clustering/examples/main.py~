import os, sys


from preprocessing.preprocessing import preprocess, preprocess_fcm_datamatrix,AnnotatedClustering , Confidence_Score_Matrix
sys.path.append('../')
from nsga2.evolution import Evolution
from nsga2.problems.zdt import ZDT
from nsga2.problems.zdt.zdt3_definitions import ZDT3Definitions
from plotter import Plotter


def print_generation(population, generation_num):
    print("Generation:- {}".format(generation_num))


"""
    #individual_list = list that contains all gene(individual) expression values
    #individual_id_list = contains all UNIQUE GENE ID that is used for calculating BHI
    #individual_ref_id_list = contains all GENE reference id that is used for calculating PPI Interaction Score
    #all_datamatrix, all_normalized_data_matrix = preprocessed the gene expression values that is fed to FCM
    #no_of_annotated_cluster: Number of annotated cluster that we get from DAVID tool
    #annotated_cluster_list: Basically it is a list of list that contains all gene id which are belongs to annotated cluster
    #annotated_gene_list: Set of all annotated gene id
    #annotated_gene_cooccurance_matrix(n X n where n = no of total gene(individual)) : represent if any two gene are
                                                                                    belong to same annotated cluster or not
    #unique_protein_ref: Contains unique Gene refernce ID
    #interaction_score_matrix(n X n where n = number of unique protein reference): contains the interaction score of any
                                                                interaction of two proteins
"""
individual_list = []
individual_length, individual_list , individual_id_list , individual_ref_id_list = preprocess('<path_to_input_dataset>')
No_of_genes = len(individual_list)
all_data_matrix , all_normalized_data_matrix = preprocess_fcm_datamatrix( individual_length,individual_list)
gene_id_list = tuple(open('Intermediate_Data/population_id.txt','r'))
no_of_annotated_cluster , annotated_cluster_list , annotated_gene_list, annotated_gene_cooccurance_matrix = AnnotatedClustering(individual_id_list)
unique_protein_ref , interaction_score_matrix = Confidence_Score_Matrix()


"""
Input from user
"""
chromosome_number = int(sys.argv[1])       # Enter the number of chromosome(individual) you want to generate
generation_number = int(sys.argv[2])       # Enter the maximum number of generation  

zdt_definitions = ZDT3Definitions(individual_list,individual_id_list,individual_ref_id_list, unique_protein_ref,
                                  no_of_annotated_cluster,annotated_cluster_list,annotated_gene_list,
                                  annotated_gene_cooccurance_matrix,interaction_score_matrix)
#zdt_definitions.perfect_pareto_front()
plotter = Plotter(zdt_definitions)
problem = ZDT(zdt_definitions, all_normalized_data_matrix,chromosome_number )
evolution = Evolution(problem, generation_number, chromosome_number, individual_list, individual_length)
evolution.register_on_new_generation(plotter.plot_population_best_front)
evolution.register_on_new_generation(print_generation)
#evolution.register_on_new_generation(print_metrics)
#evolution.register_on_new_generation(collect_metrics)
pareto_front = evolution.evolve()
#plotter.plot_x_y(collected_metrics.keys(), map(lambda (hv, hvr): hvr, collected_metrics.values()), 'generation', 'HVR', 'HVR metric for ZDT3 problem', 'hvr-zdt3')
