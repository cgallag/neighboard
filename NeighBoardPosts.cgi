#!/usr/local/bin/python2.7

import sys
import cgitb; cgitb.enable()
import cgi_utils_sda
import boardData

if __name__ == '__main__':
	print 'Content-type: text/html\n'

	names = boardData.getBoards()
	tmpl = cgi_utils_sda.file_contents('NeighBoard_Home.html')
	page = tmpl.format(boardnames=names)
	print page