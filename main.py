from source import Chromosome, Population

edd = Chromosome("EDD", "data")
spt = Chromosome("SPT", "data")
lpt = Chromosome("LPT", "data")
fcfs = Chromosome("FCFS", "data")
random1 = Chromosome()
random2= Chromosome()
random3= Chromosome()
random4= Chromosome()
random5= Chromosome()
random6= Chromosome()

initial_population = Population()
initial_population.create_initial_population()
for nst in initial_population.population:
    print(nst)