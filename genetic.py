from load import loadData
from random import random
import sys
from time import time

# Konfiguracja algorytmu
MAX_DURATION = 300          # Maksymalny czas pracy w sekundach
MAX_ITERATIONS = 50         # Maksymalna liczba iteracji
POPULATION_SIZE = 100       # Rozmiar populacji
POPULATION_TO_CROSSOVER = 0.2       # Odsetek populacji, który się rozmnaża

# Zmienne związane z pracą programu
best_qualities = []
iterations = 0
start_time = 0.0

# Punkt wejściowy algorytmu
def genetic(data):
    global best_qualities, iterations, start_time
    start_time = time()

    population = generateInitialSolutions(POPULATION_SIZE, data)
    sortPopulation(population, data['processes'])
    while canContinue():
        doGeneticIteration(population, data['processors'], data['processes'])
        best_qualities.append(measureSolutionQuality(population[0], data['processes']))
        iterations += 1


# Sprawdza czas trwania, jakość rozwiązania i ew. inne metryki i decyduje czy kontynuować
def canContinue():
    global best_qualities, iterations, start_time
    duration = time() - start_time

    cont = (iterations <= MAX_ITERATIONS
        and duration <= MAX_DURATION)
    
    if cont:
        duration = int(duration * 10) / 10
        best = best_qualities[-1] if len(best_qualities) > 0 else '+Infinity'
        print(f'Iteration #{iterations}: {duration}s elapsed, Cmax: {best}.')
    
    return cont


# Wykonuje iterację algorytmu genetycznego
def doGeneticIteration(population, processor_count, execution_times):
    initial_population_size = len(population)
    performCrossOvers(population)
    performMutations(population, processor_count)
    sortPopulation(population, execution_times)
    removeWorstSolutions(population, initial_population_size)


# Generuje zestaw początkowych rozwiązań
def generateInitialSolutions(population_size, constraints):
    return []


# Usuwa najgorsze rozwiązania z populacji, tak by przywrócić jej pierwotny rozmiar
def removeWorstSolutions(population, target_size):
    while len(population) > target_size:
        population.pop()


# Wybiera i rozmnaża rozwiązania, dodając je do populacji
def performCrossOvers(population):
    return population


# Rozmnaża rozwiązania
def crossOver(solution1, solution2):
    offspring = [0] * len(solution1)
    for i in range(len(solution1)):
        if solution1[i] == solution2[i]:
            offspring[i] = solution1[i]
        else:
            offspring[i] = solution1[i] if random() < 0.5 else solution2[i]
    return offspring


# Wybiera rozwiązania i dokonuje mutacji
def performMutations(population, processor_count):
    return population


# Mutuje rozwiązanie i zwraca nową kopię
def mutate(solution, processor_count):
    return solution


# Sortuje populację od najlepszych rozwiązań
def sortPopulation(population, execution_times):
    population.sort(key=lambda s: measureSolutionQuality(s, execution_times))


# Mierzy jakość rozwiązania (im mniej tym lepiej)
def measureSolutionQuality(solution, execution_times):
    return -1


def main():
    fname = 'data.txt'
    if len(sys.argv) >= 2:
        fname = sys.argv[1]

    data = loadData(fname)
    genetic(data)

main()