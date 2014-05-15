#!/usr/local/bin/python2.7

import sys
import cgi
import cgitb; cgitb.enable()
import re

import cgi_utils_sda
import boardData

DEST_DIR = '/home/neighbrd/public_html/images/'
DEST_URL = '/~neighbrd/images/'
IN_DB    = False                # false means store in dest_dir
MAX_FILE_SIZE = 100000          # 100 KB
# ======================================================================

# Code for adding photos to database
def generate_actor_menu(cursor):
    '''Returns an HTML menu of all actors in the WMDB'''
    cursor.execute('SELECT nm,name FROM person ORDER BY name')
    menu = '<select name="nm">\n'
    for row in cursor.fetchall():
        menu += '<option value="%s">%s</option>\n' % row
    menu += '</select>\n'
    return menu

def filesize(absfilename):
    '''Returns the length of a file in bytes'''
    stat = os.stat(absfilename)
    return stat.st_size

def check_integer(string,default):
    '''Converts string to an integer if it's all digits, otherwise
returns default'''
    if re.search('^\\d+$',string):
        try:
            return int(string)
        except:
            return default
    else:
        return default

def store_data_in_filesystem_paranoid(nm,client_filename,file_data,cursor):
    '''Stores data checking for lots of errors'''
    dest_file = DEST_DIR + str(nm) + '.jpg'
    try:
        stream = open(dest_file,'wb')
    except Exception as e:
        return 'Failure to open output file %s: %s' % (dest_file,e)
    try:
        stream.write(file_data)
    except Exception as e:
        return 'Failure to copy file data to %s: %s' % (dest_file,e)
    try:
        os.chmod(dest_file,0644)
    except Exception as e:
        return 'Failure to make file %s world-readable: %s' % (dest_file,e)

    ## Now, record the URL in the database
    url = DEST_URL + str(nm) + '.jpg'
    try:
        ## inserts or updates picture blob for this actor
        rows_mod = cursor.execute('''
INSERT INTO picfile(nm,url) VALUES (%s,%s)
ON DUPLICATE KEY UPDATE url=%s
''',
                                  (nm,url,url))
    except Exception as e:
        print e
        return 'Failure to store picture URL in database: '+str(e)
    if rows_mod != 1:
        return ('Failure to store picture URL in database; '+
                'rows modified is '+
                str(rows_mod))
    return ('The picture file %s was uploaded successfully as %s (%s) ' %
            (client_filename,dest_file,url))


if __name__ == '__main__':
	print 'Content-type: text/html\n'

	feedback = ""

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

		feedback = boardData.addBoard(board_values['title'], board_values['visibility'], board_values['category'])

	# Processing new post
	if 'new-post-recipients' in form_data:
		post_values['recipients'] = cgi.escape(form_data.getfirst('new-post-recipients')).split(',')

		if 'new-post-subject' in form_data:
			post_values['subject'] = cgi.escape(form_data.getfirst('new-post-subject'))

		if 'new-post-message' in form_data:
			post_values['message'] = cgi.escape(form_data.getfirst('new-post-message'))

		if 'new-post-tags' in form_data:
			post_values['tags'] = cgi.escape(form_data.getfirst('new-post-tags')).split(',')

		if 'new-post-images' in form_data:
		    post_values['image'] = cgi.escape(form_data.getfirst('new-post-image'))

		feedback = boardData.addPost(post_values['recipients'], post_values['subject'], 
			post_values['message'], post_values['tags'])



	# Stuff to print boards
	names = boardData.getBoardNames()
	[boards_col1, boards_col2] = boardData.displayBoards()
	tmpl = cgi_utils_sda.file_contents('NeighBoard_Home.html')
	page = tmpl.format(feedback=feedback, boardnames=names, first_col_boards = boards_col1, second_col_boards = boards_col2)
	print page