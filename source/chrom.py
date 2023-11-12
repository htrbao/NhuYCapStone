import os
import heapq
import random
import pandas as pd
from typing_extensions import Self

class Chromosome():
    chrom_types = {
        "EDD": "Due date (h)",
        "FCFS": "Jobs",
        "LPT": "P trải",
        "SPT": "P trải",
        "Genetic": "",
    }
    def __init__(self, type:str = "random", data_path:str = "data"):
        self.type = type
        self.data_path = data_path

        self.gene = None
        self.data = None
        if self.type != "Genetic":
            self.create_chrom()


    def __len__(self):
        return len(self.data.index) * 2


    def create_chrom(self) -> pd.DataFrame:
        data = pd.read_excel(os.path.join(self.data_path, 'Data.xlsx'), sheet_name=0, index_col=0)
        data = data.reset_index()
        data['Start time 1'] = 0
        data['Finish time 1'] = 0
        data['Máy trải'] = 0
        data['Máy cắt'] = 0
        data['Start time 2'] = 0.0
        data['Finish time 2'] = 0.0
        data['Độ trễ (phút)'] = 0

        # Sắp xếp công việc theo thời gian tới hạn (due date) tăng dần
        if self.type == "random":
            sorted_jobs = data.sample(frac=1).values
        else:
            sorted_jobs = data.sort_values(by=self.chrom_types[self.type], ascending=True if self.type != "LPT" else False).values

        # Khởi tạo hàng đợi ưu tiên (min heap) để theo dõi thời gian hoàn thành trên từng máy
        machines_heap = [(0, machine_id) for machine_id in range(8)]

        # Lập lịch công việc
        for job in sorted_jobs:
            processing_time, machine_id = heapq.heappop(machines_heap)
            start_time = max(processing_time, 0)
            finish_time = start_time + job[5]
            data.at[int(job[0]) - 1, 'Start time 1'] = start_time
            data.at[int(job[0]) - 1, 'Finish time 1'] = finish_time
            data.at[int(job[0]) - 1, 'Máy trải'] = machine_id + 1
            heapq.heappush(machines_heap, (finish_time, machine_id))

        # Gán việc cho máy cắt
        cutting_machine = []
        for ind in data.index:
            cutting_machine.append((data['Máy trải'][ind] + 1) // 2)
        data['Máy cắt'] = cutting_machine
        data = data.sort_values(by=['Finish time 1', 'Máy cắt'])

        # Tính thời gian cho trạm cắt
        num_cutting_machine = 4
        cur_cutting_time = [data[data['Máy cắt'] == idx + 1].iloc[0, 8] for idx in range(num_cutting_machine)]

        for ind in data.index:
            cutting_idx = data.at[ind, 'Máy cắt'] - 1
            data.at[ind, 'Start time 2'] = max(cur_cutting_time[cutting_idx], data.at[ind, 'Finish time 1'])
            data.at[ind, 'Finish time 2'] = data['Start time 2'][ind] + data['P cắt'][ind]
            data.at[ind, 'Độ trễ (phút)'] = max(0, data.at[ind, 'Finish time 2'] - (data.at[ind, 'Due date (h)'] * 60))
            cur_cutting_time[cutting_idx] = data.at[ind, 'Finish time 2']

        self.data:pd.DataFrame = data
        self.encode_chrom()


    def encode_chrom(self) -> list[int]:
        self.gene:list[int] = self.data["Jobs"].to_list()
        self.gene.extend(self.data.sort_values(by="Start time 2")["Jobs"].to_list())

    
    def crossover(self, another:Self) -> tuple[Self, Self]:
        crossover_point = random.randint(0, len(another) - 20)

        child1 = Chromosome("Genetic")
        child2 = Chromosome("Genetic")

        # # Áp dụng POX
        # child1[:crossover_point] = parent2[:crossover_point]
        # child2[:crossover_point] = parent1[:crossover_point]
        return child1, child2

    
    def objective(self) -> float:
        column_count = 'Độ trễ (phút)'
        num_tardiness = (self.data[column_count] > 0).sum()
        sum_tardiness = self.data['Độ trễ (phút)'].sum()
        return sum_tardiness
    

    def fitness(self, max_objective) -> float:
        sum_tardiness = self.data['Độ trễ (phút)'].sum()
        return max_objective - sum_tardiness
    

    def __repr__(self) -> str:
        gene = ""
        for i in range(len(self.gene)):
            gene += str(self.gene[i]) + ("  -|-  " if i == 19 else " ")
        return f"""Name: {self.type};\nGene: {gene}"""