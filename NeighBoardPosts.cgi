#!/usr/local/bin/python2.7

import sys
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import boardData

if __name__ == '__main__':
	print 'Content-type: text/html\n'

	# Process data from new board and new post forms
	form_data = cgi.FieldStorage()

	board_values = {
		'title': '', 
		'category': 'all',
		'visibility': 'public'
	}

	post_values = {
		'recipients': [],
		'subject': '',
		'message': '',
		'tags': []
	}

	# Processing new board
	if 'new-board-title' in form_data:
		board_values['title'] = cgi.escape(form_data.getfirst('new-board-title'))

		if 'category' in form_data:
			board_values['category'] = cgi.escape(form_data.getfirst('category'))

		if 'visibility' in form_data:
			board_values['visibility'] = cgi.escape(form_data.getfirst('visibility'))

		boardData.addBoard(board_values['title'], board_values['visibility'], board_values['category'])

	# Processing new post
	if 'new-post-recipients' in form_data:
		post_values['recipients'] = cgi.escape(form_data.getfirst('new-post-recipients')).split(',')

		if 'new-post-subject' in form_data:
			post_values['subject'] = cgi.escape(form_data.getfirst('new-post-subject'))

		if 'new-post-message' in form_data:
			post_values['message'] = cgi.escape(form_data.getfirst('new-post-message'))

		if 'new-post-tags' in form_data:
			post_values['tags'] = cgi.escape(form_data.getfirst('new-post-tags')).split(',')

		boardData.addPost(post_values['recipients'], post_values['subject'], 
			post_values['message'], post_values['tags'])



	# Stuff to print boards
	names = boardData.getBoardNames()
	[boards_col1, boards_col2] = boardData.displayBoards()
	tmpl = cgi_utils_sda.file_contents('NeighBoard_Home.html')
	page = tmpl.format(boardnames=names, first_col_boards = boards_col1, second_col_boards = boards_col2)
	print page