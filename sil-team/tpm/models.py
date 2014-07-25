#########################################################################################
#
#	TeamworkPM API Wrapper
#	@author Taylor Pate
#	models.py - houses different models
#
#########################################################################################

import sys, json, time

class Model(object):
	"""Base class for all models"""

	def __init__(self, api, id=0):
		self.api = api
		self.id = id

	def create(self, data):
		result = self.api.post(self, data)
		if result:
			self.id = result['id']
			print 'Created project: ' + str(self.id)
		else:
			print 'ERROR: POST was not successful.'

	def update(self, data):
		print self.api.put(self, data)

	def getAll(self):
		return self.api.get(self)

class Project(Model):
	singular = 'project'
	plural = 'projects'
	container = ''
	decendant = ''

	def addPerson(self, pid):
		person = Person(self.api, pid)
		result = self.api.attach(self, person)
	
		if result:
			print 'Added Person: ' + str(pid)
		else:
			print 'ERROR: addPerson was not successful.'
	
	def createTaskList(self, tasklistData):
		if self.id:
			tasklist = TaskList(self.api, 0)
			tasklist.data = tasklistData
			result = self.api.attach(self, tasklist)
			if result:
				return result['id']
			else:
				print 'ERROR: POST was not successful.'

		else:
			print 'ERROR: project has not been created yet!'
	
	def createMessage(self, messageData):
		if self.id:
			message = Message(self.api, 0)
			message.data = messageData
			result = self.api.attach(self, message)
			
			if result:
				return result['id']
			else:
				print 'ERROR: POST was not successful.'

		else:
			print 'ERROR: project has not been created yet!'

class Person(Model):
	singular = 'person'
	plural = 'people'
	container = ''
	decendant = ''

class Message(Model):
	singular = 'post'
	plural = 'posts'
	container = 'project'
	decendant = ''

class TaskList(Model):
	singular = 'todo-list'
	plural = 'todo_lists'
	container = 'project'
	decendant = 'tasks'

	def getTasks(self):
		if self.id:
			result = self.api.get(self, self.id, False)
			return result
		else:
			print "ERROR: TaskList object has no id"

class Task(Model):
	singular = 'todo-item'
	plural = 'todo_items'
	container = 'todo_lists'
	decendant = ''

	def assignPerson(self,tkid,pid,desc=False):
		if self.id:
			data = {"responsible-party-id":pid}		# init task data
			result = self.api.put(self, data)

		if result:
			print 'Task Assigned to user: ' + str(pid)
		else:
			print 'ERROR: Could not assign the task to user: ' + str(pid)




