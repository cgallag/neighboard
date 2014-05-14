#!/usr/local/bin/python2.7
# '''
# Written by Sydney Cusack & Caroline Gallagher Spring 2014
# '''
import sys
import cgi
import cgitb; cgitb.enable()
import signin

# #formats the web form based on existing html file and dynamic data
# def render_web_page(template_file):
#     return file_contents(template_file)
    

# #reads user input from form, validates user using methods from the python script
# def main():
#   form=cgi.FieldStorage()
#   if 'username' and 'password' in form: #checks for input
#       #gets user data
#     user_name=form.getfirst('username')
#     user_password=form.getfirst('password')
#     user_valid=signin.connValidate(user_name,user_password) #saves return value
#     if user_valid=='user invalid':
#       #checks if return value of connValidate is a string
#       print render_web_page('NeighBoard_NewUser.html') 
#         #formats html page with appropriate user message
#     else:
#       print render_web_page('NeighBoardPosts.html') 
#   else:
#      #renders blank html form
#     print render_web_page('NeighBoard_LogIn.html')

# if __name__=='__main__':
#    print 'Content-type: text/html\n'
#    main()	

import os
import os.path
 
import Cookie
import pickle
import cgi_utils_sda
 
PY_CGI_SESS_ID='PY_CGI_SESS_ID'   # a constant, the name of the cookie
 
def session_id():
    '''Intended to mimic the behavior of the PHP function of this name'''
    sesscookie = cgi_utils_sda.getCookieFromRequest(PY_CGI_SESS_ID)
    if sesscookie == None:
        sessid = cgi_utils_sda.unique_id()
        if sessid == None:
            print("I give up; couldn't create a session. No session id")
            return
    else:
        sessid=sesscookie.value   # get value out of morsel
    return sessid
     
def session_start(dir):
    sessid = session_id()
    # Set a cookie and print that header
    sesscookie = Cookie.SimpleCookie()
    cgi_utils_sda.setCookie(sesscookie,PY_CGI_SESS_ID,sessid)
    print(sesscookie)
    # check to see if there's any session data
    if not os.path.isfile(dir+sessid):
        return {}
    output = open(dir+sessid,'r+')
    # session already exists, so load saved data
    # rb for read binary
    input = open(dir+sessid,'r')
    sess_data = pickle.load(input)
    input.close()
    if isinstance(sess_data,dict):
        return sess_data
    else:
        raise Exception ("Possibly corrupted session data; not a dictionary: "
                         +sess_data)
        return
 
def save_session(dir,data):
    '''Save the session data to the filesystem.'''
    sessid = session_id()
    output = open(dir+sessid,'w+')
    pickle.dump(data,output,-1)
    output.close()
 
def main():
    my_sess_dir = '/home/cs304/public_html/python/sessions/'
    print 'Content-type: text/html'
    sess_data = session_start(my_sess_dir)
    print

    sessid = session_id()
    form_data = cgi.FieldStorage()
    if 'secret' in form_data:
        sess_data['secret'] = form_data.getfirst('secret')
 
    if 'secret' in sess_data:
        
    else:
        
    save_session(my_sess_dir,sess_data)
     
if __name__ == '__main__':
    main()
