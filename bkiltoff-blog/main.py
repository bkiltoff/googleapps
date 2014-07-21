import os
import jinja2 #jinja.pocoo.org
import webapp2

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

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True) 
    created = db.DateTimeProperty(auto_now_add = True)
    
    

class PostPage(Handler):
    def render_posting(self, ttl="", pst="", err=""):
        self.render("blog_new_post_html.html", np_title=ttl, npost=pst, error=err)

    
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