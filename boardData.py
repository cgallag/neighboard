#!/usr/local/bin/python2.7

import math
from datetime import datetime
import re
import os

import MySQLdb
from neighbrd_dsn import DSN
import dbconn

DEST_DIR = '/home/neighbrd/public_html/images/'
DEST_URL = '/~neighbrd/images/'
MAX_FILE_SIZE = 100000          # 100 KB
# ======================================================================

# Code for adding photos to database
def filesize(absfilename):
    '''Returns the length of a file in bytes'''
    stat = os.stat(absfilename)
    return stat.st_size


def check_integer(string, default):
    '''Converts string to an integer if it's all digits, otherwise
returns default'''
    if re.search('^\\d+$', string):
        try:
            return int(string)
        except:
            return default
    else:
        return default


def store_data_in_filesystem_paranoid(postId, client_filename, file_data,
                                      cursor):
    '''Stores data checking for lots of errors'''
    dest_file = DEST_DIR + str(postId) + '.jpg'
    try:
        stream = open(dest_file, 'wb')
    except Exception as e:
        return 'Failure to open output file %s: %s' % (dest_file, e)
    try:
        stream.write(file_data)
    except Exception as e:
        return 'Failure to copy file data to %s: %s' % (dest_file, e)
    try:
        os.chmod(dest_file, 0644)
    except Exception as e:
        return 'Failure to make file %s world-readable: %s' % (dest_file, e)

    ## Now, record the URL in the database
    url = DEST_URL + str(postId) + '.jpg'
    try:
        ## inserts or updates picture blob for this actor
        rows_mod = cursor.execute('''
INSERT INTO picfile(postId,picUrl) VALUES (%s,%s)
ON DUPLICATE KEY UPDATE picUrl=%s
''',
                                  (postId, url, url))
    except Exception as e:
        print e
        return 'Failure to store picture URL in database: ' + str(e)
    if rows_mod != 1:
        return ('Failure to store picture URL in database; ' +
                'rows modified is ' +
                str(rows_mod))
    return ('The picture file %s was uploaded successfully as %s (%s) ' %
            (client_filename, dest_file, url))


def process_file_upload(postId, client_filename, local_file, cursor):
    ## Test if the file was uploaded
    if not client_filename:
        return 'No file uploaded (yet)'

    file_data = local_file.read()
    ## Double check whether the file upload is too big
    if len(file_data) > MAX_FILE_SIZE:
        return 'Uploaded file is too big: ' + str(len(file_data))

    ## Get the postId, which we will either use as a DB key or a filename
    postId = check_integer(postId, None)
    if postId == None:
        return 'postId has illegal value: %s' % postId

    return store_data_in_filesystem_paranoid(postId, client_filename,
                                             file_data, cursor)


def add_image(conn, boardId, current_time, filename, filedata):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute(
        "select formId from form where boardId=%s and created=%s and type='post'",
        (boardId, current_time))

    post_row = curs.fetchone()
    if post_row is not None:
        postId = post_row['formId']
        process_file_upload(postId, filename, filedata, curs)


def display_image(conn, postId):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select * from picfile where postId=%s", (postId,))

    post_row = curs.fetchone()
    if post_row is not None:
        picUrl = post_row['picUrl']
        return "<img alt={postId}-img src={picUrl}>".format(postId=postId,
                                                           picUrl=picUrl)
    else:
        return ""


def getBoardNames():
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select boardId, name from board where type='board'");
    names = []
    while True:
        row = curs.fetchone()
        if row == None:
            return "\n".join(names)
        names.append(
            "<li id=\"{boardId}-nav\"><a href=\"#\">{name}</a></li>".format(
                **row))


def displayBoards():
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        "select boardId, name, mailname from board where type='board'");
    total_boards = curs.rowcount

    boards_printed = 0
    boards_1 = []
    boards_2 = []

    panel_html_heading = """
		<div class=\"panel panel-default\">
			<div class=\"panel-heading\">{name}<span class=\"badge pull-right\">"""

    panel_html_posts = """</span></div>
			<div class=\"list-group\" id=\"{mailname}-board\">"""

    panel_html_end = """
			</div>
        </div>"""

    while True:
        row = curs.fetchone()

        if row == None:
            return ["\n".join(boards_1), "\n".join(boards_2)]

        boardId = row['boardId']
        [posts, numposts] = displayPosts(boardId, conn)

        board_html = (
            panel_html_heading + str(numposts) + panel_html_posts).format(**row)
        board_html += posts
        board_html += panel_html_end

        if (boards_printed < math.ceil(total_boards / 2)):
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
			<h4><small>"""

    end_post = "</small></h4> </a>"

    while True:
        row = curs.fetchone()

        if row == None:
            return ["\n".join(posts), numposts]

        postId = row['formId']

        post_tags = displayTags(postId, conn)

        image = display_image(conn, postId)

        if isFirst:
            posts.append(start_post_active + post_html.format(
                **row) + post_tags + end_post)
            isFirst = False

        else:
            posts.append(
                start_post + post_html.format(**row) + image + "<br>"
                + post_tags + end_post)


def displayTags(postId, conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select * from tag where postId=%s", (postId,))

    tags = ""

    while True:
        row = curs.fetchone()

        if row == None:
            return tags

        tags += "#" + row['value'].lower().strip() + " "


def addBoard(name, privacy_level, category):
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    mailname = name.strip().lower().replace(" ", "-")

    curs.execute("select * from board where mailname=%s", (mailname,))
    row = curs.fetchone()

    if row == None:
        curs.execute(
            "insert into board (name, mailname, type, privacyLevel, category) values (%s, %s, 'board', %s, %s)",
            (name, mailname, privacy_level, category))
        return "Board " + name + " created successfully."

    else:
        return "Board " + name + " already exists."


def addPost(boards, subject, message, tags, image):
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # For feedback.
    sent = ""
    failed_to_send = ""

    for board in boards:
        mailname = board.strip().lower().replace(" ", "-")
        #print 'Searching for board ' + mailname
        curs.execute("select boardId from board where mailname=%s",
                     (mailname,))
        board_row = curs.fetchone()
        if board_row != None:
            boardId = board_row['boardId']

            # I can't get the created timestamp from mysql without causing some timestamp issues later on,
            # so I have to calculate it myself in python beforehand.
            current_time = str(datetime.now())

            curs.execute(
                "insert into form (boardId, created, title, content, type) values (%s, %s, %s, %s, 'post')",
                (boardId, current_time, subject, message))

            addTags(boardId, current_time, tags, conn)

            add_image(conn, boardId, current_time, image.filename, image.file)

            sent += board + ","

        else:
            failed_to_send += board + ","

    if failed_to_send != "":
        unsent = "Post could not be sent to " + failed_to_send.rstrip(",")
    else:
        unsent = ""

    return "Post sent to " + sent.rstrip(",") + "<br>" + unsent


def addTags(boardId, current_time, tags, conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute(
        "select formId from form where boardId=%s and created=%s and type='post'",
        (boardId, current_time))

    post_row = curs.fetchone()
    if post_row is not None:
        postId = post_row['formId']

    for tag in tags:
        standardized_tag = tag.lower().strip()
        curs.execute("insert into tag (postId, value) values (%s, %s)",
                     (postId, standardized_tag))


def main():
    names = getBoardNames()
    [boards_col1, boards_col2] = displayBoards()
    #addPost(boards=['tower', ' claflin', 'Cs department  '], subject='High tea tonight', message='Come to tower high tea tonight at 8:30pm')
    return names, boards_col1, boards_col2


if __name__ == "__main__":
    for each in main():
        print each
    #main()



