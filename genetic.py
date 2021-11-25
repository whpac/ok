import time

# Konfiguracja algorytmu
MAX_DURATION = 300          # Maksymalny czas pracy w sekndach
MAX_ITERATIONS = 50         # Maksymalna liczba iteracji

# Zmienne związane z pracą programu
iterations = 0
start_time = 0.0

# Punkt wejściowy algorytmu
def genetic():
    global iterations, start_time
    start_time = time.time()

    population = generateInitialSolutions(None, None)
    sortPopulation(population)
    while canContinue():
        doGeneticIteration(population)
        iterations += 1


# Sprawdza czas trwania, jakość rozwiązania i ew. inne metryki i decyduje czy kontynuować
def canContinue():
    global iterations, start_time
    duration = time.time() - start_time

    cont = (iterations <= MAX_ITERATIONS
        and duration <= MAX_DURATION)
    
    if cont:
        duration = int(duration * 10) / 10
        print(f'Iteration #{iterations}: {duration}s elapsed.')
    
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
    return []


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