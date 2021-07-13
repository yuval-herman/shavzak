import random
from pprint import pprint
import matplotlib.pyplot as plt

import numpy
import shavzak
from helper import *

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from multiprocessing import Pool

gen=300
n=200
cxpb=0.5
mutpb=0.2
indpb=0.2

creator.create("FitnessMax", base.Fitness, weights=(-10.0, -1.0, 10.0)) #numOfPeople, hardWorkScore, jobScore
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", make_instructions, creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("original", make_shavzak, list)
#pprint(toolbox.original())
toolbox.register("map", Pool().map)
toolbox.register("evaluate", evalFit, orig=toolbox.original)
toolbox.register("mate", tools.cxOnePoint)
o=toolbox.original()
toolbox.register("mutate", mutate, indpb=indpb, r=[len(o), 0, len(o[0][1])])
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
	
	pop = toolbox.population(n=n)
	hof = tools.HallOfFame(1)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean, axis=0)
	stats.register("std", numpy.std, axis=0)
	stats.register("min", numpy.min, axis=0)
	stats.register("max", numpy.max, axis=0)

	pop, log = algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=gen,
								   stats=stats, halloffame=hof, verbose=True)
	
	return pop, log, hof

if __name__ == "__main__":
	_, log, hof = main()
	
	best=execute_instructions(hof[0], toolbox.original())
	pprint(best)
	print("are there duplicates?: {}".format(has_duplicates(best)))
	print("does it have everyone?: {}".format(has_everyone(best)))
	
	plt.plot(log.select('max'), label='max')
	plt.plot(log.select('min'), label='min')
	plt.plot(log.select('avg'), label='avg')
	plt.plot(log.select('std'), label='std')
	plt.legend()
	plt.xlabel('gen')
	plt.show()
