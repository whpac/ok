from math import log10
from load import loadData
from random import random, randint, shuffle
import sys
from time import time
from typing import List, Tuple

#
# Populacja przechowywana jest jako lista par. Pierwszy element pary
# to Cmax rozwiązania, a drugi - tablica przypisująca zadanie do procesora.
# Ta realizacja pozwala na oszczędność w czasie działania i jest o ok. 70% szybsza
# niż przechowywanie poszczególnych rozwiązań jako obiektów klasy Solution.
#
# Jakość a Cmax. Cmax jest chwilą, w której zakończy się ostatnie zadanie. Wobec
# tego, pożądana jest minimalizacja tej wielkości. Jednak na potrzeby algorytmu
# konieczne było wprowadzenie miary jakości, którą należy zmaksymalizować.
# Dlatego za jakość przyjęto 1/Cmax
#

# Konfiguracja algorytmu
GENE_MUTATION_CHANCE = 0.03         # Prawdopodobieństwo mutacji genu w rozwiązaniu, które mutuje
CHILDREN_IN_ITERATION = 50          # Liczba dzieci w iteracji algorytmu
MAX_DURATION = 300                  # Maksymalny czas pracy w sekundach
MAX_ITERATIONS = 500                # Maksymalna liczba iteracji
POPULATION_SIZE = 100               # Rozmiar populacji
POPULATION_TO_DIE = 0.2             # Odsetek populacji, który zginie w iteracji
RANDOM_SOLUTIONS = 0.5              # Odsetek losowych rozwiązań w pierwotnej populacji
SOLUTION_MUTATION_CHANCE = 1        # Prawdopodobieństwo, że w rozwiązaniu zajdzie mutacja

# Diagnostyka
PRINT_STATS_FREQ = 10               # Co ile iteracji wyświetlać status

# Zmienne związane z pracą programu
best_cmaxes = []
iterations = 0
start_time = 0.0

# Dane dla algorytmu
execution_times = []
processor_count = 0

# Punkt wejściowy algorytmu
def genetic(proc_count: int, exec_times: List[int]) -> None:
    global best_cmaxes, iterations, start_time
    global execution_times, processor_count

    execution_times = exec_times
    processor_count = proc_count
    start_time = time()

    population = generateInitialSolutions(POPULATION_SIZE)
    sortPopulation(population)
    while canContinue():
        population = doGeneticIteration(population)
        best_cmaxes.append(population[0][0])
        iterations += 1
        printStats()


# Sprawdza czas trwania, Cmax rozwiązania i ew. inne metryki i decyduje czy kontynuować
def canContinue() -> bool:
    global best_cmaxes, iterations, start_time
    global MAX_DURATION, MAX_ITERATIONS
    duration = time() - start_time

    # Po zakończeniu wykonywania programu można podnieść limity
    if iterations >= MAX_ITERATIONS:
        print('[?] Iteration limit reached. Continue for next 50? [y/N]? ', end='')
        answer = input()
        if answer.lower() == 'y':
            MAX_ITERATIONS += 50
    
    if duration >= MAX_DURATION:
        print('[?] Time limit reached. Continue for next 60 seconds? [y/N]? ', end='')
        answer = input()
        if answer.lower() == 'y':
            MAX_DURATION = (time() + 60) - start_time

    return (iterations < MAX_ITERATIONS
        and duration <= MAX_DURATION)


# Wykonuje iterację algorytmu genetycznego
def doGeneticIteration(population: List[Tuple[int, List[int]]]) -> List[Tuple[int, List[int]]]:
    population = performCrossOvers(population)
    performMutations(population)
    sortPopulation(population)
    return population


# Generuje zestaw początkowych rozwiązań
def generateInitialSolutions(population_size: int) -> List[Tuple[int, List[int]]]:
    global execution_times, processor_count
    process_count = len(execution_times)
    population = [None] * population_size
    for i in range(population_size):
        if i / population_size < RANDOM_SOLUTIONS:
            solution = [ randint(0, processor_count-1) for _ in range(process_count) ]
        else:
            solution = buildSolutionGreedy()
        cmax = measureSolutionCmax(solution)
        population[i] = (cmax, solution)
    return population


# Buduje rozwiązanie algorytmem zachłannym
def buildSolutionGreedy() -> List[int]:
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


# Wybiera rozwiązania do rozmnożenia i tworzy nową populację
# Jeśli dzieci jest mniej niż rodziców, to nowa populacja jest
# uzupełniana starą
def performCrossOvers(population: List[Tuple[int, List[int]]]) -> List[Tuple[int, List[int]]]:
    cross_overs = len(population) * POPULATION_TO_DIE
    children = [None] * len(population)
    pop_quality_sum = sumQualities(population)

    # Wypełnij tablicę dziećmi
    idx = 0
    while len(children) < cross_overs:
        # Wybierz dwa różne rozwiązania do rozmnożenia
        parent1 = select(population, pop_quality_sum)
        parent2 = select(population, pop_quality_sum)
        while parent1 == parent2:
            parent2 = select(population, pop_quality_sum)
        
        child = crossOver(population[parent1], population[parent2])
        children[idx] = child
        idx += 1

    # Uzupełnij populację osobnikami z poprzedniej
    parents_to_survive = set()
    while idx < len(children):
        parent = select(population, pop_quality_sum)
        if parent in parents_to_survive:
            continue
        parents_to_survive.add(parent)
        children[idx] = population[parent]
        idx += 1

    return children


# Rozmnaża rozwiązania
def crossOver(parent1: Tuple[int, List[int]], parent2: Tuple[int, List[int]]) -> Tuple[int, List[int]]:
    solution1 = parent1[1]
    solution2 = parent2[1]
    offspring = [0] * len(solution1)
    for i in range(len(solution1)):
        if solution1[i] == solution2[i]:
            offspring[i] = solution1[i]
        else:
            offspring[i] = solution1[i] if random() < 0.5 else solution2[i]
    return (measureSolutionCmax(offspring), offspring)


# Wybiera rozwiązania i dokonuje mutacji
def performMutations(population: List[Tuple[int, List[int]]]) -> None:
    global execution_times, processor_count
    for i in range(len(population)):
        if random() >= SOLUTION_MUTATION_CHANCE:
            continue
        population[i] = mutate(population[i])
        #new_solution = mutate(population[i])
        # population.append(new_solution)


# Mutuje rozwiązanie i zwraca nową kopię
def mutate(solution: Tuple[int, List[int]]) -> Tuple[int, List[int]]:
    global execution_times, processor_count
    new_solution = solution[1].copy()
    for i in range(len(solution)):
        if random() < GENE_MUTATION_CHANCE:
            new_solution[i] = randint(0, processor_count-1)
    return (measureSolutionCmax(new_solution), new_solution)


# Sortuje populację od najlepszych rozwiązań
def sortPopulation(population: List[Tuple[int, List[int]]]) -> None:
    population.sort(key=lambda s: s[0])


# Mierzy Cmax rozwiązania (im mniej tym lepiej)
def measureSolutionCmax(solution: List[int]) -> None:
    global execution_times, processor_count
    processor_occupancy = [0] * processor_count
    for i in range(len(solution)):
        proc = solution[i]
        processor_occupancy[proc] += execution_times[i]
    return max(processor_occupancy)


# Sumuje jakości rozwiązań w populacji
def sumQualities(population: List[Tuple[int, List[int]]]) -> float:
    quality_sum = 0
    for (cmax, _) in population:
        quality_sum += 1 / cmax
    return quality_sum


# Zwraca indeks rozwiązania z puli
def select(population: List[Tuple[int, List[int]]], quality_sum: float) -> int:
    r = random() * quality_sum
    for i in range(len(population)):
        cmax = population[i][0]
        r -= 1 / cmax
        if r <= 0:
            return i

    return len(population) - 1


# Wypisuje statystyki co określoną liczbę iteracji
def printStats() -> None:
    if iterations % PRINT_STATS_FREQ != 0:
        return
    duration = round(time() - start_time, 1)
    digits = int(log10(MAX_ITERATIONS)) + 1
    print(f'[{iterations: >{digits}}]: {duration: >6}s elapsed, Cmax: {best_cmaxes[-1]}')


# Wypisuje końcowe statystyki
def printFinalStats() -> None:
    global best_cmaxes, iterations, start_time
    global execution_times, processor_count
    optimum = round(sum(execution_times) / processor_count, 1)

    duration = time() - start_time
    duration = round(duration, 1)
    print('\nFinished job')
    print(f'    {iterations} iterations performed')
    print(f'    {duration} seconds')
    print(f'    \033[1;32m{best_cmaxes[-1]} = Cmax\033[0m')
    print(f'    {optimum} = Cmax* <divisible tasks>')
    print(f'    {best_cmaxes[0]} -> {best_cmaxes[-1]} genetic progress')


def main() -> None:
    fname = 'data.txt'
    if len(sys.argv) >= 2:
        fname = sys.argv[1]

    data = loadData(fname)
    genetic(data['processors'], data['processes'])
    printFinalStats()

main()