#!/usr/local/bin/python2.7

import math
from datetime import datetime

import MySQLdb
from cgallag2_dsn import DSN 
import dbconn


def getBoardNames():
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


def displayBoards():
	DSN['database'] = 'cgallag2_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select boardId, name from board where type='board'");
	total_boards = curs.rowcount
	#curs.execute("select boardId, name from board where type='board'");
	boards_printed = 0
	boards_1 = []
	boards_2 = []

	panel_html_heading = """
		<div class=\"panel panel-default\">
			<div class=\"panel-heading\">{name}<span class=\"badge pull-right\">"""

	panel_html_posts = """</span></div>
			<div class=\"list-group\" id=\"{boardId}-board\">"""

	panel_html_end = """
			</div>
        </div>"""

	while True:
		row = curs.fetchone()

		if row == None:
			return ["\n".join(boards_1), "\n".join(boards_2)]

		boardId = row['boardId']
		[posts, numposts] = displayPosts(boardId, conn)

		board_html = (panel_html_heading + str(numposts) + panel_html_posts).format(**row)
		board_html += posts
		board_html += panel_html_end

		if (boards_printed < math.ceil(total_boards/2)):
			boards_1.append(board_html)

		else:
			boards_2.append(board_html)

		boards_printed += 1


# TODO: enable pagination for long pages of posts.
# TODO: display timestamps at some point. Still trying to figure out 
# how to do so.
def displayPosts(boardId, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	data = (boardId,)
	curs.execute("select * from form where type='post' and boardId= %s ", data)
	numposts = curs.rowcount

	isFirst = True
	posts = []
	
	start_post_active = """<a href="#" class="list-group-item active">"""
			
	start_post = """<a href="#" class="list-group-item">"""

	post_html = """
			<h4 class="list-group-item-heading">{title}</h4>
			<p>{content}</p>
			<h4><small>#tags-will-go-here</small></h4>
		</a>"""

	while True:
		row = curs.fetchone()

		if row == None:
				return ["\n".join(posts), numposts]

		if isFirst:
			posts.append(start_post_active + post_html.format(**row))
			isFirst = False

		else:
			posts.append(start_post + post_html.format(**row))


def addBoard(name, privacy_level, category):
	DSN['database'] = 'cgallag2_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("insert into board (name, type, privacyLevel, category) values (%s, 'board', %s, %s)", 
		(name, privacy_level, category))
	

def addPost(boards, subject, message):
	DSN['database'] = 'cgallag2_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	for board in boards:
		boardname = '%' + board + '%'
		curs.execute("select boardId from board where name like %s", (boardname,))
		board_row = curs.fetchone()
		boardId = board_row['boardId']

		# I can't get the created timestamp from mysql without causing some timestamp issues later on, 
		# so I have to calculate it myself in python beforehand.
		current_time = str(datetime.now())

		curs.execute("insert into form (boardId, created, title, content, type) values (%s, %s, %s, %s, 'post')", 
			(boardId, current_time, subject, message))


def main():
	names = getBoardNames()
	[boards_col1, boards_col2] = displayBoards()
	return names, boards_col1, boards_col2

if __name__ == "__main__":
	for each in main():
		print each



