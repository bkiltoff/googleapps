import logging
import requests
import json
import webapp2
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                   autoescape = True)

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
        action = "https://snoisle.teamwork.com/tasks/2193526.json"

        r = requests.request('GET', action,
                            auth=requests.auth.HTTPBasicAuth(key, 'password'))
        ex =json.dumps(r.json()) # this line works
        #ex = json.loads(r) #doezn't work... what's going on in above working line?
        self.render("home_html.html",example=ex)

app = webapp2.WSGIApplication([
    ('/', LandingPage),
    ], debug=True)
