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
        comp = u"https://snoisle.teamwork.com/tasks/"
        key = u"grass856wool"
        action = u"2203348.json"
        authz = requests.auth.HTTPBasicAuth(key,'pass')
        url = comp+action
        
        r = requests.get(url=url, auth=authz)
        ex =r.json()

        test = Task()
        test.taskName = ex[u'todo-item'][u'content']
        test.taskId = int(ex[u'todo-item'][u'id'])
        self.render("home_html.html", task_id=test.taskId, task_name=test.taskName)

    def post(self):
        comp = u"https://snoisle.teamwork.com/tasks/"
        key = u"grass856wool"
        action = u"2203348.json"
        authz = requests.auth.HTTPBasicAuth(key,'pass')
        url = comp+action
        newTaskName = self.request.get('inp_taskName')
        cont = json.dumps({u'todo-item':{u'content':newTaskName}})
        
        r = requests.put(url, data=cont, auth=authz)
        self.redirect("/")

        
app = webapp2.WSGIApplication([
    ('/', LandingPage),
    ], debug=True)
