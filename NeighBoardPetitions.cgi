#!/usr/local/bin/python2.7
# '''
# Written by Sydney Cusack & Caroline Gallagher Spring 2014
# '''

import sys
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import petitionData

if __name__ == '__main__':
	print "Content-type: text/html\n"

	feedback = ""

	# Process data from new board and new post forms
	form_data = cgi.FieldStorage()

	petition_values = {
		'creator': '',
		'recipients': [],
		'title': '',
		'message': '',
		'tags': []
	}

	# Processing new board
	if 'username1' in form_data:
		petition_values['creator'] = cgi.escape(form_data.getfirst('username1'))

		if 'board1' in form_data:
			petition_values['recipients'] = cgi.escape(form_data.getfirst('board1')).split(',')

		if 'title1' in form_data:
			petition_values['title'] = cgi.escape(form_data.getfirst('title1'))

		if 'description' in form_data:
			petition_values['message'] = cgi.escape(form_data.getfirst('description'))

		if 'tags' in form_data:
			petition_values['tags'] = cgi.escape(form_data.getfirst('tags')).split(',')


		feedback = petitionData.addPetition(petition_values['creator'], petition_values['recipients'], petition_values['title'], petition_values['message'], petition_values['tags'])


	# Stuff to print boards
	names = petitionData.getPetitionNames()
	petitionContent = petitionData.displayPetition(6)
	tmpl = cgi_utils_sda.file_contents('NeighBoard_Petition.html')
	page = tmpl.format(feedback=feedback, petitionnames=names, petitionContent=petitionContent)
	print page