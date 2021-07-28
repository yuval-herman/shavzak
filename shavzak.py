from enum import Enum
import json


def parseFile(path):

	with open(path, 'r') as doc:
		rawText = doc.read()
	jData=json.loads(rawText)
	people=[]
	missions=[]
	
	for person in jData['people']:
		people.append(Person.from_dict(person))
	for mission in jData['missions']:
		missions.append(Mission.from_dict(mission))

	missions.append(Mission('spare', 0, [], [], 0.01))
	return people, missions


class Status(Enum):
	BASE = 0
	HOME = 1
	SICK = 3

class Person:

	def __init__(self, name, id_num, recruit_date, status, jobs, hardwork_score, sleep_hours):
		self.name=name
		self.id_num=id_num
		self.recruit_date=recruit_date
		self.status=status
		self.jobs=jobs
		self.hardwork_score=hardwork_score
		self.sleep_hours=sleep_hours
	
	@classmethod
	def from_dict(cls, d):
		return cls(**d)
	
	def __repr__(self):
		return "Person-> {} #".format(self.__dict__)
	
	def __str__(self):
		return str(self.__dict__)

class Mission:
	
	def __init__(self, name, num_of_people, jobs_dict, required_people, hardness):
		self.name=name
		self.num_of_people=num_of_people
		self.jobs_dict=jobs_dict
		self.required_people=required_people
		self.hardness=hardness
	
	@classmethod
	def from_dict(cls, d):
		return cls(**d)
	
	def __repr__(self):
		return "Mission-> {} #".format(self.__dict__)
	
	def __str__(self):
		return str(self.__dict__)
		
		
if __name__ == '__main__':
    parseFile()
