import requests
from bs4 import BeautifulSoup



def soupify ( url ) :
	"""
	Given an URL, request the page and return a BeautifulSoup object.
	If the request was not successful, return None
	"""

	page = requests.get(url)
	print ("return code {}".format(page.status_code))
	if page.status_code >= 200 and page.status_code < 300:
		return BeautifulSoup ( page.content, 'html.parser' )
	else :
		print ( "page requested did NOT return with OK" )
		return None
