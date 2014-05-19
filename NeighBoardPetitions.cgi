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

	petitionContent = ""
	feedback = ""

	name = ""

	try:
		session_cookie = cgi_utils_sda.getCookieFromRequest('PHPSESSID')
		session_id = session_cookie.value
	except:
		session_id = "null"
	
	user_dict = petitionData.get_user(session_id)
	name = user_dict['name']

	form_data = cgi.FieldStorage()

	petition_values = {
		'recipients': [],
		'title': '',
		'message': '',
		'tags': []
	}

	search_values = {
		'petitionSearch': []
	}

	signature_values = {
		'petition': [],
		'created': '',
		'issigned': ''
	}
	# Processing new petition
	

	if 'board1' in form_data:
		petition_values['recipients'] = cgi.escape(form_data.getfirst('board1')).split(',')

		if 'title1' in form_data:
			petition_values['title'] = cgi.escape(form_data.getfirst('title1'))

		if 'description' in form_data:
			petition_values['message'] = cgi.escape(form_data.getfirst('description'))

		if 'tags' in form_data:
			petition_values['tags'] = cgi.escape(form_data.getfirst('tags')).split(',')


		feedback = petitionData.addPetition(petition_values['recipients'], 
			petition_values['title'], petition_values['message'], petition_values['tags'],user_dict['user_id'])

	if 'searchmenu' in form_data:
		search_values['petitionSearch'] = cgi.escape(form_data.getfirst('searchmenu'))
		petitionContent = petitionData.displayPetition(search_values['petitionSearch'])


	if 'sigmenu' in form_data:
		signature_values['petition'] = cgi.escape(form_data.getfirst('sigmenu'))

		if 'signature' in form_data:
			signature_values['issigned'] = cgi.escape(form_data.getfirst('signature'))
			if 'sigdates' in form_data:
				signature_values['created'] = cgi.escape(form_data.getfirst('sigdates'))
			if signature_values['issigned']=='yes':
				feedback = petitionData.signPetition(signature_values['petition'], signature_values['created'], user_dict['user_id'])


	# Stuff to print boards
	names = petitionData.getPetitionNames()
	petitionOptions = petitionData.getPetitionOptions()
	petitionOptions2 = petitionData.getPetitionOptions()
	petitionDates = petitionData.getDateCreated()
	
	tmpl = cgi_utils_sda.file_contents('NeighBoard_Petition.html')
	page = tmpl.format(feedback=feedback, petitionnames=names, petitionContent=petitionContent, petitionOptions2=petitionOptions2, 
		name=name, petitionOptions=petitionOptions, petitionDates=petitionDates)
	print page