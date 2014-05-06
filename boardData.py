#!/usr/local/bin/python2.7

import MySQLdb
from cgallag2_dsn import DSN 
import dbconn

def getBoards():
	DSN['database'] = 'cgallag2_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select boardId, name from board where type='board'");
	names = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		names.append("<li id=\"{boardId}-nav\"><a href=\"#\">{name}</a></li>".format(**row))

def main():
	boards = getBoards()
	return boards

if __name__ == "__main__":
	print main()



