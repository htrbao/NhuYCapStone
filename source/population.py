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
        self.consecutive_same_objective_count = 0
        self.max_consecutive_same_objective = 10 
        
    
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
    
        # Kiểm tra điều kiện dừng
        # Lấy tất cả các giá trị hàm mục tiêu của quần thể
        current_objectives = [chrom.objective() for chrom in self.population]

        # Lấy giá trị hàm mục tiêu nhỏ nhất trong quần thể
        current_best_objective = min(current_objectives)
        if self.is_consecutive_same_objective(current_best_objective):
            self.consecutive_same_objective_count += 1
        else:
            self.consecutive_same_objective_count = 0

        if self.consecutive_same_objective_count >= self.max_consecutive_same_objective:
            print(f"Terminating after {self.max_consecutive_same_objective} consecutive same objectives.")
            
            return True

        return False

    def is_consecutive_same_objective(self, current_best_objective):
        # Check if the current objective is the same as the previous one
        if hasattr(self, 'previous_objective'):
            if current_best_objective == self.previous_objective:
                return True
        self.previous_objective = current_best_objective
        return False