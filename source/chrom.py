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
    def __init__(self, type:str = "random"):
        self.type = type
        self.data = None
        if self.chrom_types[self.type] != "":
            self.create_chrom()

    def encode_chrom(self):
        pass

    def create_chrom(self, data_path:str = "../data"):
        data = pd.read_excel(os.path.join(data_path, 'Data.xlsx'), sheet_name=0, index_col=0)
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
            sorted_jobs = data.sort_values(by=self.self.types[self.type], ascending=True if self.type != "LPT" else False).values

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

        self.data = data

    def crossover(self, another:Self) -> tuple[Self, Self]:
        # crossover_point = random.randint(0, len(parent1) - 20)

        # child1 = Chromosome()
        # child2:Self = parent2.copy()

        # # Áp dụng POX
        # child1[:crossover_point] = parent2[:crossover_point]
        # child2[:crossover_point] = parent1[:crossover_point]
        pass

    def objective(self):
        column_count = 'Độ trễ (phút)'
        num_tardiness = (self.data[column_count] > 0).sum()
        sum_tardiness = self.data['Độ trễ (phút)'].sum()
        return sum_tardiness
    # Hàm tính độ thích nghi của mỗi NST
    def fitness(self, max_objective):
        sum_tardiness = self.data['Độ trễ (phút)'].sum()
        return max_objective - sum_tardiness