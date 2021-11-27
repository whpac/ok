from load import loadData
from random import random, randint, shuffle
import sys
from time import time

# Konfiguracja algorytmu
AVG_GENE_MUTATIONS = 2              # Średnia liczba mutacji w rozwiązaniu, które mutuje
CHILDREN_IN_ITERATION = 50          # Liczba dzieci w iteracji algorytmu
MAX_DURATION = 300                  # Maksymalny czas pracy w sekundach
MAX_ITERATIONS = 50                 # Maksymalna liczba iteracji
POPULATION_SIZE = 100               # Rozmiar populacji
POPULATION_TO_CROSSOVER = 1         # Odsetek populacji, który się rozmnaża
RANDOM_SOLUTIONS = 0.5              # Odsetek losowych rozwiązań w pierwotnej populacji
SOLUTION_MUTATION_CHANCE = 0.5      # Prawdopodobieństwo, że w rozwiązaniu zajdzie mutacja

# Diagnostyka
PRINT_STATS_FREQ = 10               # Co ile iteracji wyświetlać status

# Zmienne związane z pracą programu
best_qualities = []
iterations = 0
start_time = 0.0

# Dane dla algorytmu
execution_times = []
processor_count = 0

# Punkt wejściowy algorytmu
def genetic(proc_count, exec_times):
    global best_qualities, iterations, start_time
    global execution_times, processor_count

    execution_times = exec_times
    processor_count = proc_count
    start_time = time()

    population = generateInitialSolutions(POPULATION_SIZE)
    sortPopulation(population)
    while canContinue():
        doGeneticIteration(population)
        best_qualities.append(measureSolutionQuality(population[0]))
        iterations += 1
        printStats()


# Sprawdza czas trwania, jakość rozwiązania i ew. inne metryki i decyduje czy kontynuować
def canContinue():
    global best_qualities, iterations, start_time
    duration = time() - start_time

    return (iterations < MAX_ITERATIONS
        and duration <= MAX_DURATION)


# Wykonuje iterację algorytmu genetycznego
def doGeneticIteration(population):
    initial_population_size = len(population)
    performCrossOvers(population)
    performMutations(population)
    sortPopulation(population)
    removeWorstSolutions(population, initial_population_size)


# Generuje zestaw początkowych rozwiązań
def generateInitialSolutions(population_size):
    global execution_times, processor_count
    process_count = len(execution_times)
    population = [None] * population_size
    for i in range(population_size):
        if i / population_size < RANDOM_SOLUTIONS:
            population[i] = [ randint(0, processor_count-1) for _ in range(process_count) ]
        else:
            population[i] = buildSolutionGreedy()
    return population


# Buduje rozwiązanie algorytmem zachłannym
def buildSolutionGreedy():
    global execution_times, processor_count
    solution = [0] * len(execution_times)
    processor_usage = [0] * processor_count
    order = list(range(len(execution_times)))
    shuffle(order)

    for i in order:
        proc_index_min = min(range(len(processor_usage)), key=processor_usage.__getitem__)
        processor_usage[proc_index_min] += execution_times[i]
        solution[i] = proc_index_min

    return solution


# Usuwa najgorsze rozwiązania z populacji, tak by przywrócić jej pierwotny rozmiar
def removeWorstSolutions(population, target_size):
    while len(population) > target_size:
        population.pop()


# Wybiera i rozmnaża rozwiązania, dodając je do populacji
def performCrossOvers(population):
    reproducible = int(POPULATION_SIZE * POPULATION_TO_CROSSOVER - 1e-9)
    for i in range(CHILDREN_IN_ITERATION):
        parent1 = randint(0, reproducible)
        parent2 = randint(0, reproducible - 1)
        # Dba o to, by rozwiązanie nie rozmnażało się z samym sobą
        parent2 += 1 if parent2 >= parent1 else 0
        child = crossOver(population[parent1], population[parent2])
        population.append(child)


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
def performMutations(population):
    global execution_times, processor_count
    for i in range(len(population)):
        if random() >= SOLUTION_MUTATION_CHANCE:
            continue
        new_solution = mutate(population[i])
        population.append(new_solution)
    pass


# Mutuje rozwiązanie i zwraca nową kopię
def mutate(solution):
    global execution_times, processor_count
    new_solution = solution.copy()
    for i in range(len(solution)):
        if random() < AVG_GENE_MUTATIONS / processor_count:
            new_solution[i] = randint(0, processor_count-1)
    return new_solution


# Sortuje populację od najlepszych rozwiązań
def sortPopulation(population):
    population.sort(key=lambda s: measureSolutionQuality(s))


# Mierzy jakość rozwiązania (im mniej tym lepiej)
def measureSolutionQuality(solution):
    global execution_times, processor_count
    processor_occupancy = [0] * processor_count
    for i in range(len(solution)):
        proc = solution[i]
        processor_occupancy[proc] += execution_times[i]
    return max(processor_occupancy)


# Wypisuje statystyki co określoną liczbę iteracji
def printStats():
    if iterations % PRINT_STATS_FREQ != 0:
        return
    duration = round(time() - start_time, 1)
    print(f'[{iterations: >3}]: {duration: >6}s elapsed, Cmax: {best_qualities[-1]}')


# Wypisuje końcowe statystyki
def printFinalStats():
    duration = time() - start_time
    duration = round(duration, 1)
    print('\nFinished job')
    print(f'    {iterations} iterations performed')
    print(f'    {duration} seconds')
    print(f'    {best_qualities[-1]} = Cmax')


def main():
    fname = 'data.txt'
    if len(sys.argv) >= 2:
        fname = sys.argv[1]

    data = loadData(fname)
    genetic(data['processors'], data['processes'])
    printFinalStats()

main()