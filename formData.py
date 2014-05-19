import math
from datetime import datetime
import re
import os


import MySQLdb
from neighbrd_dsn import DSN
import dbconn

def getAdmin():
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	curs.execute("select userId, username, name from user where category='staff'")
	
	#Need to add the menu elements here, using the results
	#from the database query.
	
	names = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		names.append("<option>{username}</option>".format(**row))


def addFeedback(boardname, subject, message, creator):
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	sent = ""
	failed_to_send = ""
	boardnameStr = boardname+"feedback"
	curs.execute('select max(formId) as id from form')
	feedback_row=curs.fetchone()
	feedbackId=feedback_row['id']+1

	boardID=0
	curs.execute("select boardId as id from board where name=%s", (boardnameStr,))
	
	board_row = curs.fetchone()
	

	if board_row != None:
		boardID = board_row['id']
    	current_time = str(datetime.now())
    	print "step 1"
    	if boardID==0:
    		print "step 2"
    		curs.execute('select max(boardId) as id from board')
    		board_row=curs.fetchone()
    		boardID=board_row['id']+1
    		curs.execute("insert into board values(%s, %s, %s, %s, 'feedback', 'private', 'staff')", (boardID, boardname, boardnameStr,creator,))
    		print "board added"
    	print "step 3"
    	curs.execute("insert into form values (%s, %s, %s, %s, %s, 2, 'feedback')", 
        	(feedbackId, boardID, current_time, subject, message,))
    	print "executed query"
		sent += boardname + ","
	if failed_to_send != "":
		unsent = "Post could not be sent to " + failed_to_send.rstrip(",")
	else:
		unsent = ""
	return "Post sent to " #+ sent.rstrip(",") + "<br>" + unsent


def get_user(session_id):
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	user_dict = {
		'username': "wwellesley",
		'user_id': "0",
		'name': "Wendy Wellesley"
	}

	try:
		curs.execute("select * from usersessions where sessionkey=%s",
			(session_id,))

		row = curs.fetchone()
		username = row['username']
		user_dict['username'] = username

		curs.execute("select * from user where username=%s", (username,))

		user_row = curs.fetchone()
		user_dict['user_id'] = user_row['userId']
		user_dict['name'] = user_row['name']
		print user_dict['name']
	except:
		pass

	return user_dict


def display_name(conn, creator):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select * from user where userId=%s", (creator,))
	row = curs.fetchone()

	name = row["name"]

	if row is None:
		return ""
	else:
		return "<small>By " + name + "</small>" 
	

    
if __name__ == "__main__":
        #addFeedback('kbottoml', 'feedback test', 'kbot is awesome sauce')
        #addFeedback('rpurcell', 'duplicate test', 'CAPS TO FIND IT')
        print getAdmin()