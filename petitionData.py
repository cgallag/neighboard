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


def getPetitionNames():
	DSN['database'] = 'scusack_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select formId, title from form where type='petition'");
	names = []
	while True:
		row = curs.fetchone()
		if row == None:
			return "\n".join(names)
		names.append("<li id=\"{formId}-nav\"><a href=\"#\">{title}</a></li>".format(**row))

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

def main():
	addPetition("scusack", "Petitions", "Can I Please Graduate", "I don't want to do things anymore...")
	

if __name__ == "__main__":
	print main();
