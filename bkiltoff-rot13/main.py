#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

form="""
    <form method="post">
    <label> Textarea
    <br>
        <textarea autofocus 

        style="text-align:left;
        height: 100px;
        width: 400px;"
        
        name="txtbox">
        %(txtboxTxt)s
        </textarea>
    </label>
    <br>
    <input type="submit">
    <br>
    <div style="color: red">%(error)s</div>
    <br>
    </form>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", usr_input=""):
        self.response.out.write(form % {"error": error,
                                        "txtboxTxt": usr_input})
    def get(self):
        self.write_form()

    def post(self):
        last_input = self.request.get('txtbox')
        self.write_form("Thanks", last_input)
        
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
