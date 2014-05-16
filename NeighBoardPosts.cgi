#!/usr/local/bin/python2.7

import cgi
import cgitb; cgitb.enable()

import cgi_utils_sda
import boardData


if __name__ == '__main__':
    print 'Content-type: text/html\n'

    feedback = ""

    try:
        session_cookie = cgi_utils_sda.getCookieFromRequest('PHPSESSID')
        session_id = session_cookie.value
    except:
        session_id = "null"

    user_dict = boardData.get_user(session_id)
    name = user_dict['name']

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
        board_values['title'] = cgi.escape(
            form_data.getfirst('new-board-title'))

        if 'category' in form_data:
            board_values['category'] = cgi.escape(
                form_data.getfirst('category'))

        if 'visibility' in form_data:
            board_values['visibility'] = cgi.escape(
                form_data.getfirst('visibility'))

        feedback = boardData.addBoard(board_values['title'],
                                      board_values['visibility'],
                                      board_values['category'],
                                      user_dict['user_id'])

    # Processing new post
    if 'new-post-recipients' in form_data:
        post_values['recipients'] = cgi.escape(
            form_data.getfirst('new-post-recipients')).split(',')

        if 'new-post-subject' in form_data:
            post_values['subject'] = cgi.escape(
                form_data.getfirst('new-post-subject'))

        if 'new-post-message' in form_data:
            post_values['message'] = cgi.escape(
                form_data.getfirst('new-post-message'))

        if 'new-post-tags' in form_data:
            post_values['tags'] = cgi.escape(
                form_data.getfirst('new-post-tags')).split(',')

        if form_data.has_key('new-post-image'):
            image = form_data['new-post-image']
        else:
            image = None

        feedback = boardData.addPost(post_values['recipients'],
                                     post_values['subject'],
                                     post_values['message'],
                                     post_values['tags'],
                                     image,
                                     user_dict['user_id'])


    # Stuff to print boards
    boardnames = boardData.getBoardNames()
    [boards_col1, boards_col2] = boardData.displayBoards()
    tmpl = cgi_utils_sda.file_contents('NeighBoard_Home.html')

    page = tmpl.format(feedback=feedback + " cookie value is " + session_id,
                       name=name,
                       boardnames=boardnames,
                       first_col_boards=boards_col1,
                       second_col_boards=boards_col2)
    print page