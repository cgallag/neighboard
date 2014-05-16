#!/usr/local/bin/python2.7
# '''
# Written by Sydney Cusack & Caroline Gallagher Spring 2014
# '''
import sys
import cgi
import cgitb; cgitb.enable()
import signin

import os
import os.path
 
import Cookie
import pickle
import cgi_utils_sda
import pycas

# CAS_SERVER  = "https://my.wellesley.edu/cp/home/displaylogin"
# SERVICE_URL = "http://cs.wellesley.edu/~scusack/cgi-bin/signin.cgi"
# status, id, cookie = pycas.login(CAS_SERVER, SERVICE_URL)

#formats the web form based on existing html file and dynamic data
def render_web_page(template_file):
    return file_contents(template_file)
    

#reads user input from form, validates user using methods from the python script
def main():
  form=cgi.FieldStorage()
  if ('username' and 'password') in form: #checks for input
      #gets user data
    user_name=form.getfirst('username')
    user_password=form.getfirst('password')
    user_valid=signin.connValidate(user_name,user_password) #saves return value
    if user_valid=='user invalid':
      #checks if return value of connValidate is a string
      print render_web_page('NeighBoard_NewUser.html') 
        #formats html page with appropriate user message
    else:
      print render_web_page('NeighBoardPosts.html') 
  else:
     #renders blank html form
    print render_web_page('NeighBoard_LogIn.html')

if __name__=='__main__':
   print 'Content-type: text/html\n'
   CAS_SERVER  = "https://esapps.wellesley.edu"
   SERVICE_URL = "http://cs.wellesley.edu/~scusack/cgi-bin/signin.cgi"
   status, id, cookie = pycas.login(CAS_SERVER, SERVICE_URL)
   main()
   render_web_page("NeighBoard_LogIn.html")
   #CAS_SERVER  = "https://my.wellesley.edu/cp/home/displaylogin"
   #SERVICE_URL = "http://cs.wellesley.edu/~scusack/cgi-bin/signin.cgi"
   #status, id, cookie = pycas.login(CAS_SERVER, SERVICE_URL)
  	
