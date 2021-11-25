from load import loadData
from random import random, randint
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
def genetic(processor_count, execution_times):
    global best_qualities, iterations, start_time
    start_time = time()

    population = generateInitialSolutions(POPULATION_SIZE, processor_count, len(execution_times))
    sortPopulation(population, processor_count, execution_times)
    while canContinue():
        doGeneticIteration(population, processor_count, execution_times)
        best_qualities.append(measureSolutionQuality(population[0], processor_count, execution_times))
        iterations += 1


# Sprawdza czas trwania, jakość rozwiązania i ew. inne metryki i decyduje czy kontynuować
def canContinue():
    global best_qualities, iterations, start_time
    duration = time() - start_time

    if iterations > 0:
        duration = int(duration * 10) / 10
        print(f'Iteration #{iterations}: {duration}s elapsed, Cmax: {best_qualities[-1]}.')
    
    return (iterations < MAX_ITERATIONS
        and duration <= MAX_DURATION)


# Wykonuje iterację algorytmu genetycznego
def doGeneticIteration(population, processor_count, execution_times):
    initial_population_size = len(population)
    performCrossOvers(population)
    performMutations(population, processor_count)
    sortPopulation(population, processor_count, execution_times)
    removeWorstSolutions(population, initial_population_size)


# Generuje zestaw początkowych rozwiązań
def generateInitialSolutions(population_size, processor_count, process_count):
    population = [
        [ randint(0, processor_count-1) for _ in range(process_count) ] for _ in range(population_size)
    ]
    return population


# Usuwa najgorsze rozwiązania z populacji, tak by przywrócić jej pierwotny rozmiar
def removeWorstSolutions(population, target_size):
    while len(population) > target_size:
        population.pop()


# Wybiera i rozmnaża rozwiązania, dodając je do populacji
def performCrossOvers(population):
    # TODO
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
    # TODO
    return population


# Mutuje rozwiązanie i zwraca nową kopię
def mutate(solution, processor_count):
    # TODO
    return solution


# Sortuje populację od najlepszych rozwiązań
def sortPopulation(population, processor_count, execution_times):
    population.sort(key=lambda s: measureSolutionQuality(s, processor_count, execution_times))


# Mierzy jakość rozwiązania (im mniej tym lepiej)
def measureSolutionQuality(solution, processor_count, execution_times):
    processor_occupancy = [0] * processor_count
    for i in range(len(solution)):
        proc = solution[i]
        processor_occupancy[proc] += execution_times[i]
    return max(processor_occupancy)


def main():
    fname = 'data.txt'
    if len(sys.argv) >= 2:
        fname = sys.argv[1]

    data = loadData(fname)
    genetic(data['processors'], data['processes'])

main()