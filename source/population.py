import os
import heapq
import pandas as pd
from .chrom import Chromosome

class Population():
    def __init__(self, population_size: int = 10, ):
        self.population_size = population_size
        self.population = []
        
    def create_initial_population(self, ):
        # Khởi tạo quần thể
        self.population.extend([Chromosome("EDD"), Chromosome("EDD"), Chromosome("EDD"), Chromosome("EDD")])
        # Thêm 6 NST tạo ngẫu nhiên
        for _ in range(6):
            self.population.append(self.create_chrom())

        
        return self.population