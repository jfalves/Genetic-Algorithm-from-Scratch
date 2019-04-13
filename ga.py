import string
import numpy as np
from numpy import random


class Population():

    size = int()
    target = ''
    individuals = list()

    generation = int()
    best_score = int()
    avg_score = int()

    def __init__(self, size, target, *args, **kwargs):

        self.size = size
        self.target = target.lower()

        population_list = list()
        population_arg = 'population'

        if population_arg in kwargs:
            population_list = kwargs.get(population_arg, None)
        else:
            target_size = len(self.target)
            population_list = [DNA(target_size) for idx in range(self.size)]

        self.individuals = population_list

    def __str__(self):

        attributes = {'size':self.size,
                      'target':self.target,
                      'individuals':self.individuals,
                      'generation':self.generation,
                      'best_score':self.best_score,
                      'avg_score':self.avg_score}

        return 'generation:\t{generation}\n\
                bst score:\t{best_score}\n\
                avg score:\t{avg_score}'.format(**attributes)

    def mate_selection(self):

        mates = list()

        for idx in range(self.size):
            individual = self.individuals[idx]

            #Normaliza a pontuação dos indivíduos para uma escala de 0 à 1.
            normalized_score = np.interp(individual.score, (0,self.best_score), (0,1))
            #Probabilidade do indivíduo ser escolhido.
            probability = int(normalized_score * 100)

            for n in range(probability):
                mates.append(individual)

        mates_size = len(mates)

        return Population(mates_size, self.target, population=mates)

    def random_individual(self):
        return self.individuals[random.randint(self.size)]

    def replace_individual(self, index, individual):
        self.individuals[index] = individual

    def best_individual(self):

        best_individual = list()
        sum_score = 0

        for idx in range(self.size):

            individual = self.individuals[idx]
            sum_score += individual.score

            if individual.score >= self.best_score:

                best_individual = individual
                self.best_score = individual.score

        self.avg_score = sum_score/self.size

        return best_individual

    def increase_generation(self):
        self.generation+=1

    def is_running(self):

        is_running = bool()

        if self.best_score == 2**len(self.target):
            is_running = False
        else:
            is_running = True

        return is_running

class DNA():

    genes_sample_space = list(string.whitespace[0] + string.ascii_lowercase)
    genes = ''
    size = int()
    score = float()

    def __init__(self, size):

        self.size = size
        self.genes = random.choice(self.genes_sample_space, self.size)

    def __str__(self):

        attributes = {'genes':''.join(self.genes),
                      'size':self.size,
                      'score':self.score}

        return '{genes}'.format(**attributes)

    def fitness(self, target):

        self.score = 0

        for idx in range(self.size):
            if self.genes[idx] == target[idx]:
                self.score += 1

        self.score = 2**self.score

    def crossover(self, partner):

        child = DNA(self.size)
        midpoint = random.randint(self.size)

        for idx in range(self.size):
            if idx > midpoint:
                child.genes[idx] = self.genes[idx]
            else:
                child.genes[idx] = partner.genes[idx]

        return child

    def mutation(self, mutation_rate):

        for idx in range(self.size):
            if mutation_rate >= random.random():
                self.genes[idx] = random.choice(self.genes_sample_space, 1)[0]
