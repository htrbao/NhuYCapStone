import os
import heapq
import pandas as pd
from .chrom import Chromosome

class Population():
    def __init__(self, population_size: int = 10, ):
        self.population_size = population_size
        self.population = []
        self.generation = 0
        
    def create_initial_population(self, ):
        # Khởi tạo quần thể
        self.population.extend([Chromosome("EDD"), Chromosome("FCFS"), Chromosome("SPT"), Chromosome("LPT")])
        # Thêm 6 NST tạo ngẫu nhiên
        for _ in range(6):
            self.population.append(Chromosome())

        
        return self.population
    def acceptance_threshold_replacement(self, offspring):
        # Số lượng NST trong quần thể
        P = len(population)
        #Ngưỡng chấp nhận là NST thứ K
        k = P // 2

        # Tính hàm mục tiêu cho từng NST con
        offspring_objective = [objective(nst) for nst in offspring]# list[int]
        
        # Sắp xếp NST con theo hàm mục tiêu giảm dần
        sorted_offspring_indices = np.argsort(offspring_objective)[::-1]

        # Chọn NST thứ k trong quần thể hiện tại để so sánh
        kth_population_objective = objective(population[k - 1])

        # Thêm các NST con vào quần thể nếu hàm mục tiêu của NST con tốt hơn NST thứ k trong population 
        for i, nst_index in enumerate(sorted_offspring_indices):
            if objective(offspring[nst_index]) < kth_population_objective:
                population[k - 1] = offspring[nst_index]
                break
        #Loại bỏ các NST có hàm mục tiêu xấu nhất
        nst_remove = np.argmax([objective(nst) for nst in population])
        population.pop(nst_remove )
        self.generation += 1
        return population