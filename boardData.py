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

	panel_html = """<div class=\"panel panel-default\">
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


def main():
	names = getBoardNames()
	[boards_col1, boards_col2] = displayBoards()
	return names, boards_col1, boards_col2

if __name__ == "__main__":
	for each in main():
		print each



