#!/usr/local/bin/python2.7
# '''
# Written by Sydney Cusack & Caroline Gallagher Spring 2014
# '''
import sys
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import formData

if __name__ == '__main__':
	print "Content-type: text/html\n"

	feedback = ""

	# Process data from new board and new post forms
	form_data = cgi.FieldStorage()

	feedback_values = {
		'creator': '2',
		'recipient': '',
		'title': 'Feedback Post',
		'message': ''
	}

	# Processing new board
	

	if 'select1' in form_data:
		feedback_values['recipient'] = cgi.escape(form_data.getfirst('select1'))

		if 'question1' in form_data:
			feedback_values['message'] = cgi.escape(form_data.getfirst('question1'))



		#adminId = formData.getAdminBoard(feedback_values["recipient"])
		feedback = formData.addFeedback(feedback_values['recipient'], feedback_values["title"], feedback_values['message'],)


	# Stuff to print boards
	names = formData.getAdmin()
	tmpl = cgi_utils_sda.file_contents('NeighBoard_Form.html')
	page = tmpl.format(feedback=feedback, adminNames=names)
	print page