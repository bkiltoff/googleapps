import logging
import requests
import json
import webapp2
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                   autoescape = False) ##set to true when done fucking around

class Task(db.Model):
    taskId = db.IntegerProperty()
    taskName = db.StringProperty()
    

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class LandingPage(Handler):
    def get(self):
        comp = "https://snoisle.teamwork.com/tasks/"
        key = "grass856wool"
        action = "2203348.json"

        r = requests.request('GET', comp+action,
                            auth=requests.auth.HTTPBasicAuth(key, 'password'))
        ex =r.json()

        test = Task()
        test.taskName = ex[u'todo-item'][u'content']
        test.taskId = int(ex[u'todo-item'][u'id'])
        self.render("home_html.html", task_id=test.taskId, task_name=test.taskName)

    def post(self):
        comp = "https://snoisle.teamwork.com/tasks/"
        key = "grass856wool"
        action = "2203348.json"

        newTaskName = self.get.request('inp_taskName')
        
        r = requests.request('PUT', comp+action, 
                            auth=requests.auth.HTTPBasicAuth(key, 'password'))

app = webapp2.WSGIApplication([
    ('/', LandingPage),
    ], debug=True)
