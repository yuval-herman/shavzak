import random
import shavzak
from pprint import pprint

def missions_complete(ind):
	for m, p in ind:
		if m.name!='spare' and m.num_of_people!=len(p):
			print('{}:{} -> {}'.format(m.name, m.num_of_people, len(p)))
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

def make_instructions(ind):
	moves=ind()
	peoples, missions = shavzak.parseFile('sadac.json')
	for pi in range(len(peoples)): #iterate over people
		pi=random.randint(0, len(peoples))
		mi=random.randint(0, len(missions))
		moves.append([mi,pi])
	return moves

def execute_instructions(ind):
	#instructions are (mission, person to take)
	p, m = shavzak.parseFile('sadac.json')
	slist=[[mi,[]] for mi in m]
	for inst in ind:
		if  (0<=inst[0]<len(m) and #mission exists
		     0<=inst[1]<len(p)): #person exists
			slist[inst[0]][1].append(p[inst[1]])
	return slist

def evalFit(ind, pip, mis):
	ind=execute_instructions(ind)
	pnum=0
	hardWorkScore=0
	hasJobScore=0
	for i in range(len(ind)):
		mission=ind[i][0]
		people=ind[i][1]
		#evaluate the hardness meshing
		for p in people:
			hardWorkScore+=-abs(mission.hardness-p.hardwork_score)
		
		#evaluate the amount of people in each mission
		if mission.name=="spare":
			pnum += 1
			continue #don't care about the amount of people in the spare
		pnum += abs(mission.num_of_people-len(people)) #the farther away the number is the bigger the fitness
		
		#evaluate if correct jobs are in each mission
		for jname, jnum in mission.jobs_dict.items():
			pNum=0
			for p in people:
				if jname in p.jobs:
					pNum+=1
			if jnum==pNum: hasJobScore+=1
			
	return pnum, hardWorkScore, hasJobScore

def mutate(ind, indpb, r):
	for inst in ind: #go through instructions
		if random.random()<=indpb:
			i=random.choice((0, 1))
			inst[i]=random.randrange(r[i])
	return ind,

origi=make_shavzak(list)

