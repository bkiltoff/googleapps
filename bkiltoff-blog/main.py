import os
import jinja2
#jinja.pocoo.org
import webapp2

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

class PostPage(Handler):
    def get(self):
        self.render("blog_new_post_html.html")

    def post(self):
        #redirect to permalink to post page
        new_post_title = self.request.get("np_title")
        new_post = self.request.get("npost")

        if(new_post_title and new_post):
            self.write("Thanks")
        else:
            error = "invalid entry - something's missing here..."
            self.render("blog_new_post_html.html", error=error)
        

class MainPage(Handler):
    def get(self):
        self.render("blog_home_html.html")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', PostPage)
], debug=True)
