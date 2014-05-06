#!/usr/local/bin.python2.7

'''
Written Spring 2014
Sydney Cusack & Caroline Gallagher
Description Here
'''
import MySQLdb
from scusack_dsn import DSN
import dbconn

#===================================
#functions

#connects to WMDB and uses SQL to insert actor data
def validateUser(conn,userID,userPassword):
    curs = conn.cursor(MySQLdb.cursors.DictCursor) #results as dictionaries
    curs.execute('SELECT username, userPassword from user where username=%s and userPassword=%s',(userID,userPassword,))
    test_row = curs.fetchone()
#if no rows to fetch, nm not in database
    if test_row == None:
        user_status="user invalid"
        return user_status
    else:
        #alerts the user that actor is already in database
        user_status="user valid" 
        return user_status

def connValidate(selected_ID,selected_Password):
    DSN['database'] = 'scusack_db'
    conn = dbconn.connect(DSN)
    return validateUser(conn,selected_ID,selected_Password)



if __name__=='__main__':
    import sys
    print connValidate(sys.argv[1],sys.argv[2])
