#!/usr/local/bin/python2.7
#User Comment Here

import sys
import os
import MySQLdb
from neighbrd_dsn import DSN 
import dbconn

def searchByTags(tagValues):
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	for tagValue in tagValues:
		tagname = tagValue.strip().lower().replace(" ", "-")
		#print tagname
		
		curs.execute("select name, title, content, created, value from form inner join tag inner join board where formId=postId and form.boardId=board.boardId and value=%s and form.type!='feedback'", (tagValue,))

		isFirst = True
		posts = []
	
		start_post_active = "<p class='text'>"
					
		start_post = "<p class='text'>"

		post_html = "<h4 class='text'>{title}</h4><p>Board: {name}</p><p>{content}</p><p>Date: {created}</p><p>Tags: {value}</p>"
			
		end_post = "</p> </p>"

		while True:
			row = curs.fetchone()

			if row == None:
				return "\n".join(posts)
				
			if isFirst:
				posts.append(start_post_active.format(**row))
				posts.append(post_html.format(**row))
				posts.append(end_post.format(**row))
				isFirst = False

			else:
				posts.append(start_post.format(**row))
				posts.append(post_html.format(**row))
				posts.append(end_post.format(**row))
			

def searchByDate(searchDate):
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	formatSearchDate=str("%"+searchDate+"%")

	#print formatSearchDate

	curs.execute("select title, content, name, created from form inner join board where form.boardId=board.boardId and form.type!='feedback' and created like %s", (formatSearchDate,))

	isFirst = True
	posts = []
	
	start_post_active = "<p class='text'>"
			
	start_post = "<p class='text'>"

	post_html = "<h4 class='text'>{title}</h4><p>{content}</p><p>Date: {created}</p>"
	
	end_post = "</p> </p>"

	while True:
		row = curs.fetchone()

		if row == None:
			return "\n".join(posts)

		if isFirst:
			posts.append(start_post_active.format(**row))
			posts.append(post_html.format(**row))
			posts.append(end_post.format(**row))
			isFirst = False

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


def display_name(conn, creator):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select * from user where userId=%s", (creator,))
    row = curs.fetchone()

    name = row["name"]

    if row is None:
        return ""
    else:
        return "<small>By " + name + "</small>"    

def main():
	searchByTags("testTag")
	#searchByDate("2014-05-14")
	

if __name__ == "__main__":
	print main();