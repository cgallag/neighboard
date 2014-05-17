#!/usr/local/bin/python2.7
import math
from datetime import datetime

import sys
import MySQLdb
from scusack_dsn import DSN 
import dbconn


def addTags(formId, tags, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	for tag in tags:
		curs.execute("select max(tagId) as id from tag")
		tag_row = curs.fetchone()
		tagId=tag_row['id'] + 1
		standardized_tag = tag.lower().strip()
		curs.execute("insert into tag values (%s, %s, %s)", 
			(tagId, formId, standardized_tag))

# def getPetition(petitionName):
# 	DSN['database'] = 'scusack_db'
# 	conn = dbconn.connect(DSN)
	
# 	curs = conn.cursor(MySQLdb.cursors.DictCursor)
# 	curs.execute("select formId from form where type='petition' and title=%s", (petitionName,))

# 	iD = []
# 	while True:
# 		row = curs.fetchone()
# 		if row ==None:
# 			return iD
# 		iD.append(row)



def getPetitionNames():
	DSN['database'] = 'scusack_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select formId, title from form where type='petition'")
	names = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		names.append("<li id=\"{formId}\"><a href=\"#\">{title}</a></li>".format(**row))

def addPetition(emailName, boards, title, message, tags):
	DSN['database'] = 'scusack_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	# For feedback.
	sent = ""
	failed_to_send = ""

	for board in boards:
		boardname = board.strip().lower().replace(" ", "-")
		#print 'Searching for board ' + mailname
		curs.execute("select boardId from board where name=%s", (boardname,))
		board_row = curs.fetchone()
		if board_row != None:
			boardId = board_row['boardId']

			curs.execute('select max(formId) as id from form')
			petition_row=curs.fetchone()
			petitionId=petition_row['id']+1

			# I can't get the created timestamp from mysql without causing some timestamp issues later on, 
			# so I have to calculate it myself in python beforehand.
			current_time = str(datetime.now())

			curs.execute("insert into form (formId, boardId, created, title, content, creator, type) values (%s, %s, %s, %s, %s, 2, 'petition')", 
				(petitionId, boardId, current_time, title, message,))
			addTags(petitionId, tags, conn)
			print 'petition added'
			#addTags(boardId, current_time, tags, conn)

			sent += board + ","

		else:
			failed_to_send += board + ","

	if failed_to_send != "":
		unsent = "Post could not be sent to " + failed_to_send.rstrip(",")
	else:
		unsent = ""

	return "Post sent to " + sent.rstrip(",") + "<br>" + unsent


def displayTags(postId, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select * from tag where postId=%s", (postId,))

	tags = ""

	while True:
		row = curs.fetchone()

		if row == None:
			return tags

		tags += "#" + row['value'].lower().strip() + " "

def displayPetition(petitionID):
	DSN['database'] = 'scusack_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select title as title, content as content from form where type='petition' and formId=%s", (petitionID,))
	petition = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(petition)
		petition.append("<h2>{title}</h2> <div class='form-group' name='signature' id='signature'>".format(**row))
		petition.append("<div class='text'>{content}</div>".format(**row))
		petition.append("<div class='checkbox'><input type='checkbox' id='signature1'> Sign the Petition</label></div></div>".format(**row))



def main():
	#addPetition("scusack", "Petitions", "Can I Please Graduate", "I don't want to do things anymore...")
	#petitionid = getPetition("Duplicate?")
	print displayPetition(6)
	

if __name__ == "__main__":
	print main();
