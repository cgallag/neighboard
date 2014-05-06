#!/usr/local/bin/python2.7

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
	curs.execute("select boardId, name from board where type='board'");
	boards_printed = 0
	boards_1 = []
	boards_2 = []

	panel_html = """
		<div class=\"panel panel-default\">
			<div class=\"panel-heading\">{name}<span class=\"badge pull-right\">10</span></div>
			<div class=\"list-group\" id=\"{boardId}-board\">
			</div>
        </div>"""

	while True:
		row = curs.fetchone()

		if (boards_printed < total_boards/2):
			boards_1.append(panel_html.format(**row))

		else:
			if row == None:
				return ["\n".join(boards_1), "\n".join(boards_2)]
			boards_2.append(panel_html.format(**row))

		boards_printed += 1


def displayPosts(boardId, conn):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	data = (boardId,)
	curs.execute("select * from form where type='post' and boardId= %s ", data)

	isFirst = True
	posts = []
	
	post_html_active = """
		<a href="#" class="list-group-item active">
			<h4 class="list-group-item-heading">{title}</h4>
			<p>{content}</p>
			<h4><small>#tags-will-go-here</small></h4>
		</a>"""

	post_html = """
		<a href="#" class="list-group-item">
			<h4 class="list-group-item-heading">{title}</h4>
			<p>{content}</p>
			<h4><small>#tags-will-go-here</small></h4>
		</a>"""

	while True:
		row = curs.fetchone()

		if isFirst:
			posts.append(post_html_active.format(**row))
			isFirst = false

		else:
			if row == None:
				return "\n".join(posts)

			posts.append(post_html.format(**row))


def main():
	names = getBoardNames()
	[boards_col1, boards_col2] = displayBoards()
	return names, boards_col1, boards_col2

if __name__ == "__main__":
	for each in main():
		print each



