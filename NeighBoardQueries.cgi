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

	# Process data from new board and new post forms
	form_data = cgi.FieldStorage()

	date_values = {
		'year': '', 
		'month': '',
		'day': ''
	}

	tag_values = {
		'tags': []
	}


	if 'tags' in form_data:
		tag_values['tags'] = cgi.escape(form_data.getfirst('tags')).split(',')
		feedbackTags = queryData.searchByTags(tag_values['tags'])
		
	if ('year' or 'month' or 'day') in form_data:
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

		feedbackDate = queryData.searchByDate(searchDate)
		

	
	

	tmpl = cgi_utils_sda.file_contents('NeighBoardQueries.html')
	page = tmpl.format(feedbackTags=feedbackTags, feedbackDate=feedbackDate)
	print page



