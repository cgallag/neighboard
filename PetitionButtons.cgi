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

	petitionContent = petitionData.displayPetition(id)
	tmpl = cgi_utils_sda.file_contents('NeighBoard_Petition.html')
	page = tmpl.format(feedback=feedback, petitionnames=names, petitionContent=petitionContent)