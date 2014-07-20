##import sys
##sys.path.insert(0, 'libs')
#import fix_path
#api key grass856wool
import requests
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
        action = "2193526"

        req = requests.request('GET', comp,
auth=requests.auth.HTTPBasicAuth(key, 'password'))
        txt = req
        self.render("home_html.html", example=txt)

app = webapp2.WSGIApplication([
    ('/', LandingPage),
    ], debug=True)
