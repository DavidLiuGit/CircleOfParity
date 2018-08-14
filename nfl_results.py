# this script will request and scrape data from Pro Football Reference's
# week-by-week game results

from soupify import soupify



BASE_URL 		= 'https://www.pro-football-reference.com/years/'
YEAR 			= 2017
CONTAINER_CLASS = 'game_summary'
WINNER_CLASS	= 'winner'
LOSER_CLASS		= 'loser'
DRAW_CLASS		= 'draw'


def get_week_results ( year, week_number ) :
	"""
	Build the request URL, and make the request
	"""

	url = BASE_URL + '{}/week_{}.htm'.format(year, week_number)
	print ( 'requesting {}'.format(url) )
	soup = soupify ( url )
	if soup is None:
		print ('Error: page request unsuccessful. Exiting script.')
		exit(1)
	else:
		return soup



def analyze_soup ( soup ) :
	# get a list of every game
	all_games = soup.find_all ( 'div', class_=CONTAINER_CLASS )

	# for each game in the list, get the winner, loser, score
	for game in all_games:

		# find the tag containing data on the winner/loser of the game
		# note that it is possible for games to not have a winner/loser	
		winner = game.find(class_=WINNER_CLASS)
		loser = game.find(class_=LOSER_CLASS)
		draw = game.find(class_=DRAW_CLASS) if not winner else None		# not doing anything with draws for now

		# assuming each game has 1 winner and 1 loser... if there is a winner and loser
		if winner and loser :
			winner_str_list = winner.get_text().split('\n')
			winner_name = winner_str_list[1]
			winner_score = winner_str_list[2]
			# print ( winner_str_list )
			loser_str_list = loser.get_text().split('\n')
			loser_name = loser_str_list[1]
			loser_score = loser_str_list[2]
			print ( loser_name )






def process_week ( year, week_number ):
	# begin by making soup out of the relevant Pro Football Reference page
	soup = get_week_results ( year, week_number )

	# now that we have a page with all the match results of a given week, analyze it
	res = analyze_soup ( soup )



process_week ( YEAR, 1 ) 