import os
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import style
style.use("seaborn-darkgrid")
write_file_objective = open('non_dominated_solutions.txt', 'w+')


class Plotter():
    def __init__(self, problem):
        self.directory = 'plots'
        self.problem = problem

    def plot_population_best_front(self, population, generation_number):
        if generation_number % 1 == 0:
            print generation_number
            write_file_objective.write("\n\nGeneration Number:- %s \n" % generation_number)
            filename = "{}/generation{}.png".format(self.directory, str(generation_number))
            self.__create_directory_if_not_exists()
            computed_pareto_front = population.fronts[0]
            self.__plot_front(computed_pareto_front, filename)

    def plot_x_y(self, x, y, x_label, y_label, title, filename):
        filename = "{}/{}.png".format(self.directory, filename)
        self.__create_directory_if_not_exists()
        figure = pyplot.figure()
        axes = figure.add_subplot(111)
        axes.plot(x, y, 'r')
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        axes.set_title(title)
        pyplot.savefig(filename)
        pyplot.close(figure)

    def __create_directory_if_not_exists(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def __plot_front(self, front, filename):
        figure = pyplot.figure(figsize=[16, 9], dpi=100)
        axes = figure.add_subplot(111)
        No_of_cluster = map(lambda individual: individual.no_of_Cluster, front)
        labels = map(lambda individual: individual.labels,front)
        computed_f1 = map(lambda individual: individual.objectives[0], front)
        computed_f2 = map(lambda individual: individual.objectives[1], front)
        computed_f3 = map(lambda individual: individual.objectives[2], front)
        computed_f4 = map(lambda individual: individual.objectives[3], front)
        computed_silhoutte = map(lambda individual: individual.silhoutte_score, front)
        write_file_objective.write("No of Cluster %s \n" % No_of_cluster)
        write_file_objective.write("labels %s \n" % labels)
        write_file_objective.write("FPC %s \n" % computed_f1)
        write_file_objective.write("PBM Index %s \n" % computed_f2)
        write_file_objective.write("BHI Score %s \n" % computed_f3)
        write_file_objective.write("PPI Interaction Score %s \n" % computed_f4)
        write_file_objective.write("Silhoutte Score %s \n" % computed_silhoutte)
        print computed_silhoutte
        print max(computed_silhoutte), max(computed_f3)

        axes = figure.add_subplot(221, projection='3d')
        pyplot.plot(computed_f1, computed_f2, computed_f3, 'g.')
        axes.set_xlabel('FPC')
        axes.set_ylabel('PBM Index')
        axes.set_zlabel('BHI Score')

        axes = figure.add_subplot(222, projection='3d')
        pyplot.plot(computed_f1, computed_f2, computed_f4,  'b.')
        axes.set_xlabel('FPC')
        axes.set_ylabel('PBM Index')
        axes.set_zlabel('PPI IntScore')

        axes = figure.add_subplot(223, projection='3d')
        pyplot.plot(computed_f1, computed_f3, computed_f4, 'y.')
        axes.set_xlabel('FPC')
        axes.set_ylabel('BHI Score')
        axes.set_zlabel('PPI IntScore')

        axes = figure.add_subplot(224, projection='3d')
        pyplot.plot(computed_f2, computed_f3, computed_f4, 'r.')
        axes.set_xlabel('PBM Index')
        axes.set_ylabel('BHI Score')
        axes.set_zlabel('PPI IntScore')
        pyplot.tight_layout()
        pyplot.savefig(filename)
        # pyplot.show()
        pyplot.close(figure)
