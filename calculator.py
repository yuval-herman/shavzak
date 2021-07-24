import random
from pprint import pprint
#import matplotlib.pyplot as plt

import numpy
import shavzak
from helper import *

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from multiprocessing import Pool
from sys import argv

try:
	n=int(argv[1])
	mu=int(argv[2])
	lambda_=int(argv[3])
	cxpb=float(argv[4])
	mutpb=float(argv[5])
	indpb=float(argv[6])
	gen=int(argv[7])
except: pass

p, m = shavzak.parseFile('sadac.json')

creator.create("FitnessMax", base.Fitness, weights=(-1.0, -1.0, 1.0)) #numOfPeople, hardWorkScore, jobScore
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", make_instructions, creator.Individual, p, m)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("original", make_shavzak, list)
#pprint(execute_instructions(toolbox.individual()))
#exit()
toolbox.register("map", Pool().map)
toolbox.register("evaluate", evalFit, pip=p, mis=m)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mutate, indpb=indpb, r=[len(m), len(p)])
toolbox.register("select", tools.selNSGA2)

#print(toolbox.mutate(toolbox.individual()))

def main():
	
	pop = toolbox.population(n=n)
	hof = tools.HallOfFame(1)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean, axis=0)
	#stats.register("std", numpy.std, axis=0)
	stats.register("min", numpy.min, axis=0)
	stats.register("max", numpy.max, axis=0)

	pop, log = algorithms.eaMuPlusLambda(pop, toolbox, mu=mu, lambda_=lambda_, cxpb=cxpb, mutpb=mutpb, ngen=gen,
								   stats=stats, halloffame=hof, verbose=False)
	
	return pop, log, hof

if __name__ == "__main__":
	_, log, hof = main()
	
	print(hof[0].fitness.values)
	'''
	best=execute_instructions(hof[0], p, m)
	pprint(best)
	print("are there duplicates?: {}".format(has_duplicates(best)))
	print("does it have everyone?: {}".format(has_everyone(best)))
	print("are all the missions full?: {}".format(missions_complete(best)))
	plt.plot(log.select('max'), label='max')
	plt.plot(log.select('min'), label='min')
	plt.plot(log.select('avg'), label='avg')
	plt.plot(log.select('std'), label='std')
	plt.legend()
	plt.xlabel('gen')
	plt.show()'''
