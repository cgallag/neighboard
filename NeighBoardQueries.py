#!/usr/local/bin/python2.7
#User Comment Here

import sys
import MySQLdb
from scusack_dsn import DSN 
import dbconn

def searchByTags(tagValue):
	DSN['database'] = 'scusack_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	curs.execute("select formId, title, content from form inner join tag where formId=postId and value=%s", (tagValue,))

	numposts = curs.rowcount
	print numposts

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

		if isFirst:
			posts.append(start_post_active + post_html.format(**row) + post_tags + end_post)
			isFirst = False

		else:
			posts.append(start_post + post_html.format(**row) + post_tags + end_post)

def searchByDate(searchDate):
	DSN['database'] = 'scusack_db'
	conn = dbconn.connect(DSN)
	
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	formatSearchDate=str("%"+searchDate+"%")

	print formatSearchDate

	curs.execute("select title, content, formId from form where created like %s", (formatSearchDate,))

	numposts = curs.rowcount
	print numposts

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

		if isFirst:
			posts.append(start_post_active + post_html.format(**row) + post_tags + end_post)
			isFirst = False

		else:
			posts.append(start_post + post_html.format(**row) + post_tags + end_post)


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
	searchByTags("wellesley")
	searchByDate("2014-05-14")
	

if __name__ == "__main__":
	print main();