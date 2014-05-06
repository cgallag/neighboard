#!/usr/local/bin/python2.7
'''
Written by Sydney Cusack & Caroline Gallagher Spring 2014
This cgi reads user input from the html form and updates the WMDB accordingly.  It then 
updates the web form based on the results of the SQL queries in the Python script.
'''
import sys
import cgi
import cgitb; cgitb.enable()
import signin
from cgi_utils_sda import file_contents,cgi_header 

#formats the web form based on existing html file and dynamic data
def render_web_page(template_file):
    return file_contents(template_file)
    

#reads user input from form
#updates WMDB by calling functions from Python script
def main():
   form=cgi.FieldStorage()
   if 'username' and 'password' in form: #checks for nm input
      #gets user data
      user_name=form.getfirst('username')
      user_password=form.getfirst('password')
      user_valid=signin.connValidate(user_name,user_password) #saves return value, updates database
      if user_valid=='user invalid':
      #checks if return value of connActor is a string
      	print render_web_page('NeighBoard_NewUser.html') 
        #formats html page with appropriate user message
      else:
	#formats the html page with polite user message indicating that the actor is input successfully
        print render_web_page('board.html') 
   else:
     #renders blank html form
      print render_web_page('NeighBoard_LogIn.html')

if __name__=='__main__':
   print 'Content-type: text/html\n'
   main()	


