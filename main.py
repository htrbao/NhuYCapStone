from source import Chromosome, Population

edd = Chromosome("EDD", "data")
spt = Chromosome("SPT", "data")
lpt = Chromosome("LPT", "data")
fcfs = Chromosome("FCFS", "data")

print(edd)
print(spt)
print(edd.crossover(spt))