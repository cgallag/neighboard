import math
from datetime import datetime
import re
import os


import MySQLdb
from scusack_dsn import DSN
import dbconn

def addFeedback(boardname, subject, message):
	DSN['database'] = 'scusack_db'
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	sent = ""
	failed_to_send = ""

	curs.execute("select boardId from board where name=%s", (boardname,))
	board_row = curs.fetchone()

	if board_row != None:
		boardId = board_row['boardId']
        # I can't get the created timestamp from mysql without causing some timestamp issues later on,
        # so I have to calculate it myself in python beforehand.
        current_time = str(datetime.now())

        curs.execute(
            "insert into form (boardId, created, title, content, type) values (%s, %s, %s, %s, 'feedback')",
              (boardId, current_time, subject, message))
        sent += board + ","

    else:
    	failed_to_send += board + ","
    	
    if failed_to_send != "":
    	unsent = "Post could not be sent to " + failed_to_send.rstrip(",")
    else:
    	unsent = ""

    return "Post sent to " + sent.rstrip(",") + "<br>" + unsent	

    
if __name__ == "__main__":
        addFeedback('scusackfeedback', 'feedback test', 'sydney is awesome sauce')
        


