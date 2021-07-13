import argparse
import json
import random
from multiprocessing import Pool

parser = argparse.ArgumentParser()
parser.add_argument("numOfPeople", type=int)
args = parser.parse_args()

pip={}
with open('names.txt', 'r') as f:
	doc=f.readlines()

def randomDate():
	day=random.randint(1, 28)
	mon=random.choice((3,8,11))
	year=random.randint(2018, 2022)
	return '{}/{}/{}'.format(day,mon,year)

def randomJob(k):
	return list(set(random.choices(('driver', 'nagmash', 'commander', 'officer'), [1/20, 1/15, 1/10, 1/35], k = k)))

def makeMan(i):
	pip['name']=random.choice(doc)[:-1]
	pip['id_num']=random.randint(8000000, 9999999)
	pip['recruit_date']=randomDate()
	pip['status']=random.choices(('BASE', 'HOME', 'SICK'), [1, 1/6, 1/30])[0]
	pip['jobs']=randomJob(random.choices(range(4), [1, 1/5, 1/15, 1/25])[0])
	pip['hardwork_score']=random.random()
	pip['sleep_hours']=random.choices(list(range(0, 12)), [1,2,3,4,5,6,5,4,3,2,1,1/2])[0]
	return(json.dumps(pip, indent=3))


with Pool(8) as p:
	print(',\n'.join(p.map(makeMan, range(args.numOfPeople))))
