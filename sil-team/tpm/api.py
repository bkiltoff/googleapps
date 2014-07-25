#########################################################################################
#
#	TeamworkPM API Wrapper
#	@author Taylor Pate
#	api.py - initialize the API connection, handles authorizing & url requests
#
#########################################################################################

import sys, requests, json

class API(object):

	def __init__(self, company, key):
		self.key = key
		self.url = 'http://'+company+'.companyworkflow.com'

	def get(self, model, tid, all=True):
		urlSuffix = ''
		urlPrefix = ''
		urlSuffix2 = ''
		if model.decendant == 'tasks':		
			urlSuffix += '/' + model.id	 + '/' + model.decendant
		elif not all:		
			urlSuffix += '/' + model.id						

		urlSuffix += '.json'

		getURL = self.url + urlPrefix

		if model.container == 'todo_lists' and all:
			getURL += '/tasks' + urlSuffix	
		elif model.decendant == 'tasks' and all:
			getURL +=  '/tasks' + urlSuffix	
		else:	
			getURL +=  '/' + model.plural + urlSuffix

		print getURL	

		r = requests.get( getURL, auth=(self.key, 'x') )

		if r.status_code == requests.codes.ok:
			return r._content
		else:
			return False

	def attach(self, model, data):	
		if data.id == 0:
			attachURL = self.url + '/' + model.plural + '/' + str(model.id) + '/' + data.plural + '.json'
		else:
			attachURL = self.url + '/' + model.plural + '/' + str(model.id) + '/' + data.plural + '/' + str(data.id) + '.json'

		print attachURL
		
		postData = {}
		try:
			postData[data.singular] = data.data
		except:
			postData[data.singular] = data.id
		postString = json.dumps(postData)
		print postString

		r = requests.post( attachURL, data=json.dumps(postData), auth=(self.key, 'x') )

		if r.status_code == requests.codes.ok:
			return r.headers
		else:
			return False

	def post(self, model, data, create=True):
		urlSuffix = ''
		if not create:		
			urlSuffix += '/' + model.id	

		urlSuffix += '.json'
	
		postURL = self.url + '/' + model.plural + urlSuffix
	
		postData = {}
		postData[model.singular] = data
		postString = json.dumps(postData)
		print postString

		r = requests.post( postURL, data=postString, auth=(self.key, 'x') )
	
		if r.status_code == requests.codes.ok:
			return r.headers
		else:
			return False
	
	def put(self, model, data, create=False):
		urlSuffix = ''
		if not create:		
			urlSuffix += '/' + model.id

		urlSuffix += '.json'

		putData = {}
		putData[model.singular] = data
		putString = json.dumps(putData)
		print putString

		putURL = self.url + '/' + model.plural + urlSuffix
		print putURL
		r = requests.put( putURL, data=json.dumps(putData), auth=(self.key, 'x') )

		if r.status_code == requests.codes.ok:
			return r
		else:
			return False



