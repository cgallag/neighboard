#!/usr/local/bin/python2.7
import math
from datetime import datetime

import sys
import MySQLdb
from neighbrd_dsn import DSN 
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


def getPetitionNames():
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select formId, title, name, created from form inner join board where form.type='petition' and form.boardId=board.boardId order by created desc")
	names = []
	numpetitions = 0
	while (True and numpetitions<4):
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		names.append("<li id=\"{formId}\"><h6>{title}</h6><p>Sent To: {name} at {created}</p></li>".format(**row))
		numpetitions = numpetitions+1
		if numpetitions==4:
			return "\n".join(names)

def getPetitionOptions():
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select title from form where form.type='petition'")
	names = []
	previousTitle=""
	
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		if row['title']!=previousTitle:
			names.append("<option>{title}</option>".format(**row))
		previousTitle = row['title']

def getDateCreated():
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select created from form where form.type='petition'")
	dates = []
	previousDate=""
	
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(dates)
		if row['created']!=previousDate:
			dates.append("<option>{created}</option>".format(**row))
		previousDate = row['created']
		
def signPetition(petitionName, dateCreated, signerId):
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	# curs.execute('select max(sigId) as id from signature')
	# signature_row=curs.fetchone()
	# signatureId=signature_row['id']+1

	curs.execute("select formId as id from form where type='petition' and title=%s and created=%s", (petitionName, dateCreated))
	sent = ""
	petitionIDS = []
	numpetitions = curs.rowcount

	while True:
		row=curs.fetchone()
		if row!=None:
			petitionIDS.append(row['id'])
		else:
			break

	numsig = 0
	while numsig<numpetitions:
		curs.execute('select max(sigId) as id from signature')
		signature_row=curs.fetchone()
		signatureId=signature_row['id']+1
		curs.execute("insert into signature values(%s, %s, %s)", (signatureId, petitionIDS[numsig], signerId,))
		numsig = numsig+1


def addPetition(boards, title, message, tags, creator):
	DSN['database'] = 'neighbrd_db'
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

			curs.execute("insert into form (formId, boardId, created, title, content, creator, type) values (%s, %s, %s, %s, %s, %s, 'petition')", 
				(petitionId, boardId, current_time, title, message, creator,))
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


# def displayTags(postId, conn):
# 	curs = conn.cursor(MySQLdb.cursors.DictCursor)
# 	curs.execute("select * from tag where postId=%s", (postId,))

# 	tags = ""

# 	while True:
# 		row = curs.fetchone()

# 		if row == None:
# 			return tags

# 		tags += "#" + row['value'].lower().strip() + " "

def displayPetition(petitionName):
	DSN['database'] = 'neighbrd_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select title as title, content as content, created as date, name from form inner join board where form.boardId=board.boardId and type='petition' and title=%s", (petitionName,))
	petition = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(petition)
		petition.append("<h4>{title}</h4>".format(**row))
		petition.append("<p class='text'>{content}</p>".format(**row))
		petition.append("<p class='text'>Posted To: {name}</p>".format(**row))
		petition.append("<p class='text'>Created On: {date}</p>".format(**row))

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

def main():
	#addPetition("scusack", "Petitions", "Can I Please Graduate", "I don't want to do things anymore...")
	#petitionid = getPetition("Duplicate?")
	#print displayPetition(6)
	#signPetition("TEST PETITION", "2014-05-18 12:16:44", 2)
	print getDateCreated("TEST PETITION")
	

if __name__ == "__main__":
	print main();
