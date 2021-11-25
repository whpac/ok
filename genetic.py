from time import time
from random import random

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
def genetic():
    global best_qualities, iterations, start_time
    start_time = time()

    population = generateInitialSolutions(POPULATION_SIZE, None)
    sortPopulation(population)
    while canContinue():
        doGeneticIteration(population)
        best_qualities.append(measureSolutionQuality(population[0], None))
        iterations += 1


# Sprawdza czas trwania, jakość rozwiązania i ew. inne metryki i decyduje czy kontynuować
def canContinue():
    global best_qualities, iterations, start_time
    duration = time() - start_time

    cont = (iterations <= MAX_ITERATIONS
        and duration <= MAX_DURATION)
    
    if cont:
        duration = int(duration * 10) / 10
        print(f'Iteration #{iterations}: {duration}s elapsed, Cmax: {best_qualities[-1]}.')
    
    return cont


# Wykonuje iterację algorytmu genetycznego
def doGeneticIteration(population):
    initial_population_size = len(population)
    performCrossOvers(population)
    performMutations(population, None)
    sortPopulation(population)
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
def sortPopulation(population):
    population.sort(key=lambda s: measureSolutionQuality(s, None))


# Mierzy jakość rozwiązania (im mniej tym lepiej)
def measureSolutionQuality(solution, execution_times):
    return -1


def main():
    genetic()

main()