import random
import shavzak
from pprint import pprint
from copy import deepcopy

def missions_complete(ind):
	for m, p in ind:
		if m.name!='spare' and m.num_of_people!=len(p):
			print('{}:{} -> {}'.format(m.name, m.num_of_people, len(p)))
			return False
	return True
	
def jobs_complete(ind):
	for m, p in ind:
		if m.name=='spare': continue
		
		jobs=deepcopy(m.jobs_dict)
		for jname, jnum in jobs.items():
			for pep in p:
				if jname in pep.jobs and jobs[jname]!=0:
					jobs[jname]-=1
		if sum(jobs.values())>0:
			print('{}:{} -> {}'.format(m.name, m.jobs_dict, jobs))
			return False
	return True

def has_duplicates(ind):
	ids=[]
	for pair in ind:
		ids+=[p.id_num for p in pair[1]]
	if len(ids) != len(set(ids)):
		return True
	return False

def has_everyone(ind, everyone=None):
	if everyone == None:
		peoples, missions = shavzak.parseFile('sadac.json')
		everyone={p.id_num for p in peoples}
	ids=set()
	for pair in ind:
		ids.update({p.id_num for p in pair[1]})
	if set(ids) == set(everyone):
		return True
	return False

def make_shavzak(t):
	ind=t()
	peoples, missions = shavzak.parseFile('sadac.json')
	ind.append((missions[0], peoples))
	for i in range(1,len(missions)):
		#l=int(len(peoples)/len(missions))
		ind.append((missions[i], []))
	ind.append((shavzak.Mission('spare', 0, [], [], 0.01),[]))
	return ind

def make_instructions(ind, peoples, missions):
	moves=ind()
	#peoples, missions = shavzak.parseFile('sadac.json')
	for pi in range(len(peoples)): #iterate over people
		mi=random.randrange(0, len(missions))
		moves.append([mi,pi])
	return moves

def execute_instructions(ind, people, missions):
	#instructions are (mission, person to take)
	slist=[[mi,set()] for mi in missions]
	usedPeople=set()
	for inst in ind:
		slist[inst[0]][1].add(people[inst[1]])
	return slist

def evalFit(ind, pip, mis):
	ind=execute_instructions(ind, pip, mis)
	pnum=0									#check the number of people in each job
	hardWorkScore=0							#check people get jobs with correct hardness
	hasJobScore=0							#check each mission has all requierd jobs
	
	for i in range(len(ind)): #go over each mission
		mission=ind[i][0]
		people=ind[i][1]
		#evaluate the hardness meshing
		for p in people:
			hardWorkScore-=abs(mission.hardness-p.hardwork_score)
		
		#evaluate the amount of people in each mission
		if mission.name=="spare":
			continue #don't care about the amount or jobs of people in the spare
		pnum += abs(mission.num_of_people-len(people)) #the farther away the number is the bigger the fitness
		
		#evaluate if correct jobs are in each mission
		for jname, jnum in mission.jobs_dict.items():
			pNum=0
			for p in people:
				if jname in p.jobs:
					pNum+=1
			hasJobScore+=abs(jnum-pNum)
			
	return pnum, hardWorkScore, hasJobScore

def mutate(ind, indpb, r):
	for i in range(len(ind)): #go through instructions
		if random.random()<=indpb:
			m=random.randrange(r[0]) #random mission
			ind[i][0]=m
	return ind,

def mate(ind, sind, bfunc):
	ind.sort(key = lambda x: x[1])
	sind.sort(key = lambda x: x[1])
	return bfunc(ind, sind)

origi=make_shavzak(list)

