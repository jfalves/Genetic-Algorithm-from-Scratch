from ga import Population, DNA
import string
import numpy as np


target = 'ser ou nao ser eis a questao'
population_size = 100
mutation_rate = 0.01

#Gera uma população inicial aleatória.
population = Population(population_size, target)

while population.is_running():

    #Fase de calculo da adaptação dos indivíduos.
    for idx in range(population.size):
        population.individuals[idx].fitness(population.target)

    #Mostra o indivíduo mais adapatado da população.
    print(population.best_individual())

    #Seleciona os indivíduos que irão se reproduzir.
    mating_pool = population.mate_selection()

    #Fase de Reprodução.
    for idx in range(population.size):
        parent_a = mating_pool.random_individual()
        parent_b = mating_pool.random_individual()

        child = parent_a.crossover(parent_b)
        child.mutation(mutation_rate)

        population.replace_individual(idx,child)

    population.increase_generation()
