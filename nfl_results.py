# this script will request and scrape data from Pro Football Reference's
# week-by-week game results

from soupify import soupify



BASE_URL 		= 'https://www.pro-football-reference.com/years/'
YEAR 			= 2017

def get_week_results ( year, week_number ) :
	"""
	Build the request URL, and make the request
	"""

	url = BASE_URL + '{}/week_{}.html'.format(year, week_number)
	print ( 'requesting {}'.format(url) )
	soup = soupify ( url )
	if soup is None:
		print ('Error: page request unsuccessful. Exiting script.')
		exit(1)
	else:
		return soup



def process_week ():
	pass



get_week_results ( YEAR, 1 ) 