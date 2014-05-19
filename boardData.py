#!/usr/local/bin/python2.7

import math
from datetime import datetime
import sys
import os
import base64

import MySQLdb
from neighbrd_dsn import DSN
import dbconn


DEST_DIR = '/students/neighbrd/public_html/images/'
DEST_URL = '/~neighbrd/images/'
MAX_FILE_SIZE = 100000          # 100 KB
# ======================================================================

# Code for adding photos to database
def filesize(absfilename):
    '''Returns the length of a file in bytes'''
    stat = os.stat(absfilename)
    return stat.st_size


def store_data_in_filesystem_paranoid(client_filename, file_data):
    '''Stores data checking for lots of errors'''
    dest_file = DEST_DIR + str(client_filename) + '.jpg'
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
    url = DEST_URL + str(client_filename) + '.jpg'

    return url


def process_file_upload(client_filename, local_file):
    ## Test if the file was uploaded
    if not client_filename:
        return 'No file uploaded (yet)'

    file_data = local_file.read()
    ## Double check whether the file upload is too big
    if len(file_data) > MAX_FILE_SIZE:
        return 'Uploaded file is too big: ' + str(len(file_data))

    if client_filename is None:
        return 'client_filename has illegal value: %s' % client_filename

    return store_data_in_filesystem_paranoid(client_filename, file_data)


def add_image_to_post(postId, url, client_filename, cursor):
    dest_file = DEST_DIR + str(client_filename) + '.jpg'

    try:
        ## inserts or updates picture blob for this post
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


def add_image(conn, boardId, current_time, filename, filedata):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute(
        "select formId from form where boardId=%s and created=%s and type='post'",
        (boardId, current_time))

    post_row = curs.fetchone()
    if post_row is not None:
        postId = post_row['formId']
        return process_file_upload(filename, filedata)


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


def is_user(session_id):
    conn = dbconn.connect(DSN)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("select * from usersessions where sessionkey=%s",
                     (session_id,))

    row = curs.fetchone()
    username = row['username']

    curs.execute("select * from user where username=%s", (username,))

    user_row = curs.fetchone()

    if user_row is None:
        return False
    else:
        return True


# Find the user given the session id
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


def getBoardNames():
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select boardId, name from board where type='board'")
    names = []
    while True:
        row = curs.fetchone()
        if row is None:
            return "\n".join(names)
        names.append(
            "<li id=\"{boardId}-nav\"><a href=\"#\">{name}</a></li>".format(
                **row))


def displayBoards():
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(
        "select boardId, name, mailname from board where type='board'")
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

        if row is None:
            return ["\n".join(boards_1), "\n".join(boards_2)]

        boardId = row['boardId']
        [posts, numposts] = displayPosts(boardId, conn)

        board_html = (
            panel_html_heading + str(numposts) + panel_html_posts).format(
            **row)
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

    posts = []

    start_post = """<a href="#" class="list-group-item">"""

    post_html_1 = """
            <h4 class="list-group-item-heading">{title}
            <small class="pull-right">{created}</small>
            <br>"""

    post_html_2 = """
            </h4>
            <p>{content}</p>
            <h4><small>"""

    end_post = "</small></h4> </a>"

    while True:
        row = curs.fetchone()

        if row == None:
            return ["\n".join(posts), numposts]

        postId = row['formId']
        creator = row['creator']

        post_tags = displayTags(postId, conn)

        image = display_image(conn, postId)

        created_by = display_name(conn, creator)

        posts.append(
            start_post + post_html_1.format(**row) + created_by +
            post_html_2.format(**row) + image + "<br>"
            + post_tags + end_post)


def display_name(conn, creator):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select * from user where userId=%s", (creator,))
    row = curs.fetchone()

    name = row["name"]

    if row is None:
        return ""
    else:
        return "<small>By " + name + "</small>"


def displayTags(postId, conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select * from tag where postId=%s", (postId,))

    tags = ""

    while True:
        row = curs.fetchone()

        if row is None:
            return tags

        if row['value'] != "":
            tags += "#" + row['value'].lower().strip() + " "


def addBoard(name, privacy_level, category, owner_id):
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    mailname = name.strip().lower().replace(" ", "-")

    curs.execute("select * from board where mailname=%s", (mailname,))
    row = curs.fetchone()

    if row is None:
        curs.execute(
            "insert into board (name, mailname, owner, type, privacyLevel, category) values (%s, %s, %s, 'board', %s, %s)",
            (name, mailname, owner_id, privacy_level, category))
        return "Board " + name + " created successfully."

    else:
        return "Board " + name + " already exists."


def addPost(boards, subject, message, tags, image, owner_id):
    conn = dbconn.connect(DSN)

    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    # For feedback.
    sent = ""
    failed_to_send = ""

    # For keeping track of posts that should have images with them.
    postIds = []

    for board in boards:
        mailname = board.strip().lower().replace(" ", "-")
        #print 'Searching for board ' + mailname
        curs.execute("select boardId from board where mailname=%s",
                     (mailname,))
        board_row = curs.fetchone()
        if board_row is not None:
            boardId = board_row['boardId']

            # I can't get the created timestamp from mysql without causing some timestamp issues later on,
            # so I have to calculate it myself in python beforehand.
            current_time = str(datetime.now())

            curs.execute(
                "insert into form (boardId, created, title, content, creator, type) values (%s, %s, %s, %s, %s, 'post')",
                (boardId, current_time, subject, message, owner_id))

            addTags(boardId, current_time, tags, conn)

            curs.execute("select formId from form where boardId=%s and created=%s and type='post'",
                (boardId, current_time))

            post_row = curs.fetchone()

            if post_row is not None:
                postIds.append(post_row['form_id'])

        else:
            failed_to_send += board + ","

    image_filename = str(base64.b64encode(os.urandom(16)))
    pic_url = process_file_upload(image_filename, image.file)

    for post in postIds:
        add_image_to_post(post, pic_url, image_filename, curs)

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


def main(session_key):
    return get_user(session_key)


if __name__ == "__main__":
    session_key = sys.argv[1]
    print session_key
    print main(session_key)



