#!/usr/local/bin/python2.7

import sys
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import queryData

if __name__ == '__main__':	
	print "Content-type: text/html\n"

	feedbackTags = ""
	feedbackDate = ""

	name=""


	try:
		session_cookie = cgi_utils_sda.getCookieFromRequest('PHPSESSID')
		session_id = session_cookie.value
	except:
		session_id = "null"
	
	user_dict = queryData.get_user(session_id)
	name = user_dict['name']




	

	# Process data from new board and new post forms
	form_data = cgi.FieldStorage()

	date_values = {
		'year': '', 
		'month': '',
		'day': ''
	}

	tag_values = {
		'tags': ''
	}


	if 'tagselect' in form_data:
		tag_values['tags'] = cgi.escape(form_data.getfirst('tagselect'))
		feedbackTags = queryData.searchByTags(tag_values['tags'])
		
	searchDate = ""
	if 'year' in form_data:
		date_values['year'] = cgi.escape(form_data.getfirst('year'))
		searchDate = searchDate+date_values['year']

	if 'month' in form_data:
		date_values['month'] = cgi.escape(form_data.getfirst('month'))
		searchDate = searchDate+"-"+date_values['month']

	if 'day' in form_data:
		date_values['day'] = cgi.escape(form_data.getfirst('day'))
		searchDate = searchDate+"-"+date_values['day']

	if searchDate !="":
		feedbackDate = queryData.searchByDate(searchDate)
		
	tmpl = cgi_utils_sda.file_contents('NeighBoardQueries.html')
	tagnames = queryData.getTags()
	page = tmpl.format(feedbackTags=feedbackTags, feedbackDate=feedbackDate, name=name, tagnames=tagnames)
	print page



