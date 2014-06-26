import webapp2
import cgi
import urllib

HTML_HEADER="""
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
"""
form="""
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value=%(username)s>
          </td>
          <td class="error">
            %(invalid_name)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value=%(password)s>
          </td>
          <td class="error">
            %(invalid_password)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value=%(verify)s>
          </td>
          <td class="error">
            %(password_mismatch)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value=%(email)s>
          </td>
          <td class="error">
             %(invalid_email)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
"""
HTML_FOOTER = """
  </body>

</html>
"""
import webapp2
import re

#regex sets for form validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PW_RE = re.compile(r"^.{3,20}$")

ERR_DICT = {'invalid_name':"",
            'invalid_password':"",
            'password_mismatch':"",
            'invalid_email':""}

def validEmail(email):
    ERR_DICT['invalid_email']=""
    if email:
        return EMAIL_RE.match(email)
    else:
        return 1 #email is optional, so if blank, return true

def validName(nm):
    ERR_DICT['invalid_name']=""
    if nm:
        return USER_RE.match(nm)
    else:
        return 0

def validPass(pw1):
    ERR_DICT['invalid_password']=""
    if pw1:
        return PW_RE.match(pw1)
    else:
        return 0

def validVerify(pw1,pw2):
    ERR_DICT['password_mismatch']=""
    return pw2 == pw1

def validate(name,password,verify,email):
    counter = 0
    if not validName(name):
        ERR_DICT['invalid_name'] = "Please enter a suitable name."
        counter = counter+1
    if not validPass(password):
        ERR_DICT['invalid_password'] = "Invalid password: retry."
        counter = counter+1
    if not validVerify(password,verify):
        ERR_DICT['password_mismatch'] = "Passwords don't match: retry."
        counter = counter+1
    if not validEmail(email):
        ERR_DICT['invalid_email']="Email address is invalid: retry."
        counter = counter+1
    if counter == 0:
        return 1
    else:
        return 0

#main handler
class MainHandler(webapp2.RequestHandler):
    def write_form(self, usr_input_name="", usr_input_p1="", usr_input_p2="", usr_input_email=""):
        self.response.out.write(form %{"username":usr_input_name,
                                        "password":usr_input_p1,
                                        "verify":usr_input_p2,
                                        "email":usr_input_email,
                                        "invalid_name":ERR_DICT['invalid_name'],
                                        "invalid_password":ERR_DICT['invalid_password'],
                                        "password_mismatch":ERR_DICT['password_mismatch'],
                                        "invalid_email":ERR_DICT['invalid_email']})

    def get(self):
        self.response.out.write(HTML_HEADER)
        self.write_form()
        self.response.out.write(HTML_FOOTER) 


    def post(self):
        nm = self.request.get("username")
        pw1 = self.request.get('password')
        pw2 = self.request.get('verify')
        email = self.request.get('email')
        if validate(nm,pw1,pw2,email):
            query_params = {'username':nm}
            self.redirect('/thx?' + urllib.urlencode(query_params))
        else:            ##invalid something, rewrite form
            self.response.out.write(HTML_HEADER)            
            self.write_form(nm,"","",email)
            self.response.out.write(HTML_FOOTER)

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        param = self.request.get('username')
        self.response.out.write("Thanks, " + param)
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thx', SuccessHandler)
], debug=True)
