import random
from music21 import *

# Define parameters
NUM_CHORDS = 16
TOURNAMENT_SIZE = 5
MUTATION_RATE = 0.05

all_notes = ['C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4']

# Initialize the population with random chromosomes
# Each chromosome is a list of random chords. Each chord is a list of 3 notes
def init_population(size):
    population = []
    for i in range(size):
        chromosome = []
        for j in range(NUM_CHORDS):
            new_chord = [random.choice(all_notes), random.choice(all_notes), random.choice(all_notes)]
            chromosome.append(new_chord)
        population.append(chromosome)
    
    return population

# fitness function
def fitness(chromosome, melody):
    # Peform the following 3 times:
        # - analyze key of 3 notes in melody --> goal key
        # - check if each note in the chord is in the goal key
        # - tally the points to create a fitness function
    tally = 0
    for i in range(NUM_CHORDS):
        mel_key = melody[i].analyze('key')
        mel_scale = mel_key.getScale('major')
        for j in range(3):
            if mel_scale.getScaleDegreeFromPitch(chromosome[i][j]): 
                tally += 1
    return tally

# Implementation of tournament selection to choose a parent
def tournament_selection(population, melody):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    return max(tournament, key=lambda ind: fitness(ind, melody))

# Implementation of the 1 point crossover genetic operator
# Only crosses over each chord - so changes the chord order not the notes
def crossover(parent1, parent2):
    point = random.randint(0, NUM_CHORDS-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Implementation of the mutate genetic operator
# At a rate of MUTATION_RATE, increments or decrements 
# a given note in the chromosome
def mutate(chromosome):
    rand_num = random.random()
    if rand_num < 0.33:
        chromosome = inc_or_dec(chromosome)
    elif rand_num < 0.66:
        chromosome = first_inversion(chromosome)
    else:
        chromosome = second_inversion(chromosome)
            
    return chromosome

# At a rate of MUTATION_RATE, increments or decrements a note in the chromosome
def inc_or_dec(chromosome):
    for i in range(NUM_CHORDS):
        for j in range(3):
            note = chromosome[i][j]
            if random.random() < MUTATION_RATE:
                if random.random() < 0.5:
                    chromosome[i][j] = all_notes[(all_notes.index(note) + 1) % 12]
                else:
                    chromosome[i][j] = all_notes[(all_notes.index(note) - 1) % 12]
    return chromosome

# At a rate of MUTATION_RATE, performs a first triad inversion 
# on each chord in the given chromosome
def first_inversion(chromosome):
    temp_chrom = []
    for i in range(NUM_CHORDS):
        if random.random() < MUTATION_RATE:
            temp_chrom.append(chromosome[i][1])
            temp_chrom.append(chromosome[i][2])
            temp_chrom.append(chromosome[i][0])
            chromosome[i] = temp_chrom
            temp_chrom = []

    return chromosome

# At a rate of MUTATION_RATE, performs a second triad inversion 
# on each chord in the given chromosome
def second_inversion(chromosome):
    temp_chrom = []
    for i in range(NUM_CHORDS):
        if random.random() < MUTATION_RATE:
            temp_chrom.append(chromosome[i][2])
            temp_chrom.append(chromosome[i][0])
            temp_chrom.append(chromosome[i][1])
            chromosome[i] = temp_chrom
            temp_chrom = []

    return chromosome

# culls the population by 50%
def cull_population(population, pop_size, melody):
    new_pop = sorted(population, reverse=True, key=lambda ind: fitness(ind, melody))
    new_pop = new_pop[:pop_size // 2]
    return new_pop

# implementation of the genetic algorithm
def genetic_algorithm(population, num_generations, population_size, melody):
    overall_fittest_fitness = 0
    overall_fittest = []
    for generation in range(num_generations):

        # cull the populaion by 50%
        new_population = cull_population(population, population_size, melody)

        #replenish the population using crossover and mutation
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, melody)
            parent2 = tournament_selection(population, melody)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < population_size:
                new_population.append(mutate(child2))
        
        population = new_population

        # determine the fittest individual
        fittest_individual = max(population, key=lambda ind: fitness(ind, melody))
        best_fitness = fitness(fittest_individual, melody)
        if((overall_fittest_fitness < best_fitness)):
            overall_fittest = fittest_individual
            overall_fittest_fitness = best_fitness

        print("Generation ", generation+1, ", Best Fitness = ", best_fitness)
    
    print("Final winner's fitness", overall_fittest_fitness)
    return overall_fittest

def get_harmony(melody, num_generations, population_size):
    # ask user for desired number of generations and population size
    population = init_population(population_size)

    # launch the genetic algorithm, find the optimal solution
    winner = genetic_algorithm(population, num_generations, population_size, melody)

    return winner