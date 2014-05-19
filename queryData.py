#!/usr/local/bin/python2.7
#queryData.py
#Written by Sydney Cusack & Caroline Gallagher, Spring 2014
#Searches the NeighBoard Database for Petitions and Posts by tags and/or date.

import sys
import os
import MySQLdb
from neighbrd_dsn import DSN 
import dbconn

#Connects to the database, queries by a given tag value, returns all posts with that tag value.
def searchByTags(tagValues):
	#Connect to database
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	
	#Execute query	
	curs.execute("select formId, name, title, content, created, value from form inner join tag inner join board where formId=postId and form.boardId=board.boardId and value=%s and form.type!='feedback'", (tagValues,))
	posts = []
	
	#HTML code to format results
	start_post = "<p class='text'>"

	post_html = "<h4 class='text'>{title}</h4><p>Board: {name}</p><p>{content}</p><p>Date: {created}</p>"
			
	end_post = "</p> </p>"


	while True:
		row = curs.fetchone()

		if row == None:
			return "\n".join(posts)			
		else:
			posts.append(start_post.format(**row))
			posts.append(post_html.format(**row))
			posts.append(end_post.format(**row))
			
#Connects to the database, queries whatever date constraints the user provides, and returns all dates within those constraints.
def searchByDate(searchDate):
	#Connect to Database
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	#format the given date for the SQL query
	formatSearchDate=str("%"+searchDate+"%")

	curs.execute("select title, content, name, created from form inner join board where form.boardId=board.boardId and form.type!='feedback' and created like %s", (formatSearchDate,))

	posts = []
	
	#HTML to format results		
	start_post = "<p class='text'>"

	post_html = "<h4 class='text'>{title}</h4><p>{content}</p><p>Date: {created}</p>"
	
	end_post = "</p> </p>"

	while True:
		row = curs.fetchone()

		if row == None:
			return "\n".join(posts)
		else:
			posts.append(start_post.format(**row))
			posts.append(post_html.format(**row))
			posts.append(end_post.format(**row))

def get_user(session_id):
    conn = dbconn.connect(DSN)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    user_dict = {
        'username': "null",
        'user_id': "null",
        'name': "null"
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

    except:
        pass

    return user_dict

def getTags():
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	curs.execute("select value from tag")
	
	repeatnames = []
	names = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		if row['value'] not in repeatnames:
			names.append("<option>{value}</option>".format(**row))
			repeatnames.append(row['value'])
		

def main():
	searchByTags("testTag")
	#searchByDate("2014-05-14")
	

if __name__ == "__main__":
	print main();