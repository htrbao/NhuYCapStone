import random
from source import Chromosome, Population

# Hàm chạy thuật toán di truyền
def genetic_algorithm(num_generations = 50, population_size = 50, crossover_probability = 0.8, mutation_probability = 0.2):
    population = Population(population_size)
    population.create_initial_population()
    for generation in range(num_generations):
        elite_list = population.roulette_wheel_selection()
        offspring = Population()
        for parent1, parent2 in zip(elite_list[::2], elite_list[1::2]):
            if random.random() < crossover_probability:
                child1, child2 = parent1.crossover(parent2)
                offspring.add_chromosome(child1)
                offspring.add_chromosome(child2)
        for chrom in offspring.population:
            if random.random() < mutation_probability:
                chrom.mutation()
                offspring.add_chromosome(chrom)
        population.acceptance_threshold_replacement(offspring)
        
        best_nst = population.get_best_chrom()
        if population.is_need_to_terminate():
            return best_nst
        print(f"Generation {generation + 1}, Best Objective: {best_nst.objective()}")
# Gọi hàm chạy thuật toán di truyền
solution = genetic_algorithm()
print(solution)
print(solution.data)
