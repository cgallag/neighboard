#!/usr/local/bin/python2.7

import MySQLdb
from cgallag2_dsn import DSN 
import dbconn

def getBoards():
	DSN['database'] = 'cgallag2_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select ')




