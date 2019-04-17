import string
import numpy as np
from numpy import random


#Calcula o score de cada indivíduo
def fitness(individual, target, size):

    score = 0

    for idx in range(size):
        if individual[idx] == target[idx]:
            score += 1

    return 2**score

#Seleciona os índividuos que irão se reproduzir
def mate_selection(population_list, population_fitness, population_size, best_score):

    mates = list()

    for idx in range(population_size):
        individual = population_list[idx]

        #Normaliza a pontuação dos indivíduos para uma escala de 0 à 1.
        normalized_score = np.interp(population_fitness[idx], (0,best_score), (0,1))
        #Probabilidade do indivíduo ser escolhido.
        probability = int(normalized_score * 100)

        for n in range(probability):
            mates.append(individual)

    return mates

#Realiza o cruazamento dos genes
def crossover(parent_a, parent_b, target_size):

    child = list()
    midpoint = random.randint(target_size)

    for idx in range(target_size):
        if idx > midpoint:
            child.append(parent_a[idx])
        else:
            child.append(parent_b[idx])

    return child

#Realiza a mutação dos genes
def mutation(child, target_size, mutation_rate):

    for idx in range(target_size):
        if mutation_rate >= random.random():
            child[idx] = random.choice(genes_sample_space, 1)[0]

    return child


#Realiza o setup inicial dos dados necessários para começar utilizar o algoritmo
target = 'ser ou nao ser eis a questao'
population_size = 100
mutation_rate = 0.01
genes_sample_space = list(string.whitespace[0] + string.ascii_lowercase)

#Gera uma população inicial aleatória.
target_size = len(target)
population_list = list()

for n in range(population_size):
  individual = random.choice(genes_sample_space, target_size)
  population_list.append(individual)


while True:

    #Calcula a adaptação dos indivíduos.
    population_fitness = list()
    for idx in range(population_size):
        population_fitness.append(fitness(population_list[idx], target, target_size))

    #calcula o melhor score de toda população
    best_score = np.amax(population_fitness)

    #1. Seleciona os indivíduos que irão se reproduzir.
    mating_pool = mate_selection(population_list, population_fitness, population_size, best_score)
    mating_pool_size = len(mating_pool)

    #2. Fase de Reprodução.
    for idx in range(population_size):
        parent_a = mating_pool[random.randint(mating_pool_size)]
        parent_b = mating_pool[random.randint(mating_pool_size)]

        #2.1 Reproduz-se
        child = crossover(parent_a, parent_b, target_size)
        #3. Ocorre uma mutação.
        child = mutation(child, target_size, mutation_rate)

        #4. Substituimos a população pelo filho gerado.
        population_list[idx] = child

        print(''.join(population_list[idx]))
