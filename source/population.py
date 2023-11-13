import os
import random
import heapq
import pandas as pd
import numpy as np
from typing_extensions import Self

from .chrom import Chromosome

class Population():
    def __init__(self):
        self.population: list[Chromosome] = []
        self.generation = 0
        self.consecutive_same_objective_count = 0
        self.max_consecutive_same_objective = 10 
        
    @property
    def population_size(self):
        return len(self.population)


    def create_initial_population(self, ):
        # Khởi tạo quần thể
        self.population.extend([Chromosome("EDD"), Chromosome("FCFS"), Chromosome("SPT"), Chromosome("LPT")])
        # Thêm 6 NST tạo ngẫu nhiên
        for _ in range(6):
            self.population.append(Chromosome())
        
        return self.population
    

    def acceptance_threshold_replacement(self, offspring: Self):
        # Số lượng NST trong quần thể
        P = len(self.population)
        #Ngưỡng chấp nhận là NST thứ K
        k = P // 2

        # Tính hàm mục tiêu cho từng NST con
        offspring_objective = [chrom.objective() for chrom in offspring.population]# list[int]
        
        # Sắp xếp NST con theo hàm mục tiêu giảm dần
        sorted_offspring_indices = np.argsort(offspring_objective)[::-1]

        # Chọn NST thứ k trong quần thể hiện tại để so sánh
        kth_population_objective = self.population[k - 1].objective()

        # Thêm các NST con vào quần thể nếu hàm mục tiêu của NST con tốt hơn NST thứ k trong population 
        for i, nst_index in enumerate(sorted_offspring_indices):
            if offspring.population[nst_index].objective() < kth_population_objective:
                self.population[k - 1] = offspring.population[nst_index]
                break
        #Loại bỏ các NST có hàm mục tiêu xấu nhất
        nst_remove = np.argmax([nst.objective() for nst in self.population])
        self.population.pop(nst_remove)
        self.generation += 1
    
        # Kiểm tra điều kiện dừng
        # Lấy tất cả các giá trị hàm mục tiêu của quần thể
        current_objectives = [chrom.objective() for chrom in self.population]

        # Lấy giá trị hàm mục tiêu nhỏ nhất trong quần thể
        current_best_objective = min(current_objectives)
        if self.is_consecutive_same_objective(current_best_objective):
            self.consecutive_same_objective_count += 1
        else:
            self.consecutive_same_objective_count = 0

        
    def is_need_to_terminate(self):
        return self.consecutive_same_objective_count >= self.max_consecutive_same_objective


    def is_consecutive_same_objective(self, current_best_objective):
        # Check if the current objective is the same as the previous one
        if hasattr(self, 'previous_objective'):
            if current_best_objective == self.previous_objective:
                return True
        self.previous_objective = current_best_objective
        return False


    def roulette_wheel_selection(self) -> list[Chromosome]:
        max_objective = max([chrom.objective() for chrom in self.population])
        
        fitness_values = [chrom.fitness(max_objective) for chrom in self.population]
        
        total_fitness = sum(fitness_values)
        
        probabilities = [fit / total_fitness for fit in fitness_values]
        
        probabilities_prefix:list[float] = []
        for i in range(len(probabilities)):
            probabilities_prefix.append(probabilities[i] + (probabilities_prefix[-1] if i != 0 else 0))
        
        random_list = [random.random() for _ in range(len(self.population))]
        elite_population: list[Chromosome]  = [self.population[i] for i in np.searchsorted(probabilities_prefix, random_list, side='right')]

        return elite_population
    

    def add_chromosome(self, chrom: Chromosome):
        """
        Arg:
            chrom: Chromosome sẽ được thêm vào Quần thể này
        """
        self.population.append(chrom)


    def remove_chromosome(self, index: int):
        """
        Arg:
            index: Vị trí của Chromosome sẽ bị remove
        """
        self.population.pop(index)
    
    
    def get_best_chrom(self):
        objective_list = [chrom.objective() for chrom in self.population]
        index = np.argmin(objective_list)
        return self.population[index]
