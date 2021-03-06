import math
from datetime import datetime
import re
import os


import MySQLdb
from neighbrd_dsn import DSN
import dbconn

#Returns all users who are marked as 'staff' formatted for HTML
def getAdmin():
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	curs.execute("select userId, username, name from user where category='staff'")
	
	names = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		names.append("<option>{username}</option>".format(**row))

#Adds feedback to private user board, creates private user board if DNE
def addFeedback(boardname, subject, message, creator):
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	sent = ""
	failed_to_send = ""
	#format for all private feedback board names
	boardnameStr = boardname+"feedback"
	curs.execute('select max(formId) as id from form')
	feedback_row=curs.fetchone()
	feedbackId=feedback_row['id']+1

	boardID=0
	curs.execute("select boardId as id from board where privacyLevel='private' and name=%s", (boardnameStr,))

	
	board_row = curs.fetchone()
	numrows = curs.rowcount
	#if search returns result, board already exists
	if numrows!=0:
		boardID=board_row['id']
	print boardID
	
	current_time = str(datetime.now())
	#create board if necessary
	if boardID==0:
		curs.execute('select max(boardId) as id from board')
		board_row=curs.fetchone()
		boardID=board_row['id']+1
		curs.execute("insert into board values(%s, %s, %s, %s, 'feedback', 'private', 'staff')", (boardID, boardnameStr, boardname,creator,))
	#insert feedback
	curs.execute("insert into form values (%s, %s, %s, %s, %s, %s, 'feedback')", (feedbackId, boardID, current_time, subject, message, creator,))
	#feedback for CGI script
	sent = sent+boardnameStr 
	if failed_to_send != "":
		unsent = "Post could not be sent to " + failed_to_send.rstrip(",")
	else:
		unsent = ""
	return "Post sent to " + sent + "<br>" + unsent

#returns a user_dict from the session key.
def get_user(session_id):
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	user_dict = {
		'username': "",
		'user_id': "",
		'name': ""
	}
	
	try:
		#use session id associatd with user to pull additional data
		curs.execute("select * from usersessions where sessionkey=%s",
			(session_id,))

		row = curs.fetchone()
		username = row['username']
		user_dict['username'] = username
		#use username pulled from usersessions table to query more data
		curs.execute("select * from user where username=%s", (username,))

		user_row = curs.fetchone()
		user_dict['user_id'] = user_row['userId']
		user_dict['name'] = user_row['name']
		print user_dict['name']
	except:
		pass

	return user_dict

    
if __name__ == "__main__":
        addFeedback('kbottoml', 'feedback test', 'kbot is awesome sauce',2)
        #addFeedback('rpurcell', 'duplicate test', 'CAPS TO FIND IT')
        #print getAdmin()