import os
import heapq
import pandas as pd
import numpy as np
from typing_extensions import Self

from .chrom import Chromosome

class Population():
    def __init__(self, population_size: int = 10, ):
        self.population_size = population_size
        self.population: list[Chromosome] = []
        self.generation = 0
        
    
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
                self.population[k - 1] = offspring[nst_index]
                break
        #Loại bỏ các NST có hàm mục tiêu xấu nhất
        nst_remove = np.argmax([nst.objective() for nst in self.population])
        self.population.pop(nst_remove)
        self.generation += 1