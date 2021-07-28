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
import argparse

parser = argparse.ArgumentParser(description='Calculate shavzak')

parser.add_argument('pop', type=int, help='The size of the population.')
parser.add_argument('mu', type=int, help='The number of individuals to select for the next generation.')
parser.add_argument('lambda_', type=int, help='The number of children to produce at each generation.')
parser.add_argument('cxpb', type=float, help='The probability that an offspring is produced by crossover.')
parser.add_argument('mutpb', type=float, help='The probability that an offspring is produced by mutation.')
parser.add_argument('indpb', type=float, help='The probability that a gen will mutate.')
parser.add_argument('ngen', type=int, help='The number of generation.')
parser.add_argument('-v', dest='verbose', action='store_const',
                    const=True, default=False,
                    help='show more information')

args = parser.parse_args()

if args.verbose: pprint(vars(args))
n=args.pop
mu=args.mu
lambda_=args.lambda_
cxpb=args.cxpb
mutpb=args.mutpb
indpb=args.indpb
gen=args.ngen

p, m = shavzak.parseFile('sadac.json')

creator.create("FitnessMax", base.Fitness, weights=(-1.0, -1.0, -1.0)) #pnum, hardWorkScore, hasJobScore
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", make_instructions, creator.Individual, p, m)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("original", make_shavzak, list)
#pprint(execute_instructions(toolbox.individual()))
#exit()
toolbox.register("map", Pool().map)
toolbox.register("evaluate", evalFit, pip=p, mis=m)
toolbox.register("mate", mate, bfunc=tools.cxOnePoint)
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
								   stats=stats, halloffame=hof, verbose=args.verbose)
	
	return pop, log, hof

if __name__ == "__main__":
	_, log, hof = main()
	
	print(hof[0].fitness.values)
	if not args.verbose: exit()
	best=execute_instructions(hof[0], p, m)
	sortedBest=[]
	for mis, pip in best:
		pip=list(pip)
		pip.sort(key = lambda x: x.hardwork_score)
		sortedBest.append([mis, pip])
	pprint(sortedBest)
	print(toolbox.evaluate(hof[0]))
	print("are there duplicates?: {}".format(has_duplicates(best)))
	print("does it have everyone?: {}".format(has_everyone(best)))
	print("are all the missions full?: {}".format(missions_complete(best)))
	print("are all the jobs full?: {}".format(jobs_complete(best)))
	plt.plot(log.select('max'), label='max')
	plt.plot(log.select('min'), label='min')
	plt.plot(log.select('avg'), label='avg')
	plt.plot(log.select('std'), label='std')
	plt.legend()
	plt.xlabel('gen')
	plt.show()
