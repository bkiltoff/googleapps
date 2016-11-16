import os
import jinja2 #jinja.pocoo.org
import webapp2
from google.appengine.ext import db

#this basically says that templates will be stored in the subfolder of this
#project called 'templates'
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#this basically devines the jinja_env variable using some cool jinja2 method
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                   autoescape = True)

#jinja handler... this stuff basically allows templating
class Handler(webapp2.RequestHandler):
	#the write function simply writes out some parameters &/or keyword paramters
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
	#define a render_str function to leverage jinja's power to take a template
    #and rewrite it using params
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
	#combine the render_str and write functions to allow easily rendering a set
    #of params and a define template
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#This defines a Post object. the db.Model parameter implicitly passes some
# properties to be fulfilled. As I recall, the db.Model is a Google database
# defined model with a lot of possible properties
class Post(db.Model):
    title = db.TextProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
#so the Post object has required properties: title(string), content(longer
#string), and creation date (time stamp)


#PostPage class for the page that takes post submissions
class PostPage(Handler):
	#render the page with post contents
    def render_posting(self, ttl="", pst="", err=""):
        self.render("blog_new_post_html.html", np_title=ttl, npost=pst,
                                                                    error=err)


    def get(self):
        self.render_posting()

    def post(self):
        new_post_title = self.request.get("subject")
        new_post = self.request.get("content")


        if(new_post_title and new_post):
            #commit new_post and new_post_title to db
            p = Post(title = new_post_title, content = new_post)
            #put stores the data in db and returns key, id() gets id number
            p_key = p.put().id()

            #assign id number to post

            #redirect to permalink to post page (id#)
            self.redirect("/%d" %p_key)
        else:
            error = "invalid entry - something's missing here..."
            self.render_posting(new_post_title, new_post, error)


class MainPage(Handler):
    def get(self):
        #render old posts
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC")

        self.render("blog_home_html.html", posts=posts)

class PostedPage(Handler):
    def get(self, p_id):
        p = Post.get_by_id(int(p_id))
        self.render("blog_post_html.html", title=p.title, content=p.content)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', PostPage),
    ('/(\d+)', PostedPage),
    ], debug=True)
