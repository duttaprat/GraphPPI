"""NSGA-II related functions"""

import functools
from nsga2.population import Population
import random, math

class NSGA2Utils(object):
    def __init__(self, problem, num_of_individual, individual_list,individual_length, mutation_strength = 0.2, num_of_tour_particips=2):
        self.problem = problem
        self.num_of_individuals = num_of_individual
        self.individual_list = individual_list
        self.mutation_strength = mutation_strength
        self.num_of_tour_particips = num_of_tour_particips
        self.individual_length= individual_length

        
    def fast_nondominated_sort(self, population):
        population.fronts = []
        population.fronts.append([]) 
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()

            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.add(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)
                    
    def __sort_objective(self, val1, val2, m):
        return cmp(val1.objectives[m], val2.objectives[m])
    
    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0
            
            for m in range(len(front[0].objectives)):
                front = sorted(front, cmp=functools.partial(self.__sort_objective, m=m))
                front[0].crowding_distance = self.problem.max_objectives[m]
                front[solutions_num-1].crowding_distance = self.problem.max_objectives[m]
                for index, value in enumerate(front[1:solutions_num-1]):
                    front[index].crowding_distance = (front[index+1].crowding_distance - front[index-1].crowding_distance) / (self.problem.max_objectives[m] - self.problem.min_objectives[m])
                
    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1
    
    def create_initial_population(self):
        population = Population()
        for i in range(self.num_of_individuals):
            print "Individual", i
            individual = self.problem.generateIndividual()
            #self.problem.calculate_objectives(individual)
            population.population.append(individual)
        return population
    
    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1.features == parent2.features:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1)
            self.__mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)
        return children
    
    def __crossover(self, individual1, individual2):
        child1 = self.problem.generateIndividual()
        child2 = self.problem.generateIndividual()
        min_gene_length = min(len(child1.features),len(child2.features))
        min_individual_length = min (len(individual1.features) , len(individual2.features))
        #print "individual length", len(individual1.features) , len(individual2.features), min_individual_length
        #print "child length",len(child1.features),  len(child2.features), min_gene_length
        min_choromosome = min(min_individual_length, min_gene_length)
        genes_indexes = range(min_choromosome)
        half_genes_indexes = random.sample(genes_indexes, 1)
        #print "Random point", half_genes_indexes
        for i in genes_indexes:
            #print i
            if i in half_genes_indexes:
                child1.features[i] = individual2.features[i]
                child2.features[i] = individual1.features[i]
            else:
                child1.features[i] = individual1.features[i]
                child2.features[i] = individual2.features[i]
        return child1, child2

    def __mutate(self, child):
        child_center = child.no_of_Cluster
        #print len(self.individual_list)
        max_no_cluster = int(math.sqrt(len(self.individual_list))) 
        #print max_no_cluster
        if (child_center > 2 and child_center < max_no_cluster):
            mutation_parameter = random.random()
        else:
            mutation_parameter = 0.5
            
                 
        if (mutation_parameter<0.7): #Normal Mutation
            number_of_genes_to_mutate = int(len(child.features)/4)
            genes_to_mutate = random.sample(range(0, len(child.features)), number_of_genes_to_mutate)
            for gene in genes_to_mutate:
                child.features[gene] = child.features[gene] - self.mutation_strength/2 + random.random() * self.mutation_strength
                if child.features[gene] < 0:
                    child.features[gene] = 0
                elif child.features[gene] > 1:
                    child.features[gene] = 1
        elif (mutation_parameter >= 0.7  and mutation_parameter < 0.85): #Increase Mutation
            x = random.randint(0,len(self.individual_list))
            for i in self.individual_list[x]:
                child.features.append(i)
            child.no_of_Cluster = child.no_of_Cluster+1
        elif (mutation_parameter >= 0.85 and mutation_parameter <=1 ): #Deletion Mutation
            del child.features[-self.individual_length:]
            child.no_of_Cluster = child.no_of_Cluster-1


        
    def __tournament(self, population):
        #print "tournament"
        participants = random.sample(population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or self.crowding_operator(participant, best) == 1:
                best = participant
        return best
