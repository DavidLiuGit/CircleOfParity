# this script will request and scrape data from Pro Football Reference's
# week-by-week game results

from soupify import soupify
from collections import namedtuple
from pprint import pprint



BASE_URL 		= 'https://www.pro-football-reference.com/years/'
YEAR 			= 2017
CONTAINER_CLASS = 'game_summary'
WINNER_CLASS	= 'winner'
LOSER_CLASS		= 'loser'
DRAW_CLASS		= 'draw'




###############################################################################
##### CLASS DECLARATIONS
###############################################################################

GameResult = namedtuple ( 'GameResult', 'winner loser winner_score loser_score year week' )

script_teams_dict = {}


class Team:

	def __init__ ( self, name ):
		self.name = name
		self.beat_list = []
		self.lost_to_list = []

	def add_beat_team ( self, beaten_team_obj ):
		self.beat_list.append (beaten_team_obj)

	def add_lost_to_team ( self, lost_to_team_obj ):
		self.lost_to_list.append (lost_to_team_obj)

	def __str__ ( self ):
		return str(vars(self))

	def __repr__ ( self ):
		return str(vars(self))
	




###############################################################################
##### HELPER FUNCTIONS
###############################################################################

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




def analyze_soup ( soup, yr=0, wk=0 ) :
	"""
	Given the soup of a PFR weekly results page, analyze the games that happened in the week.
	Return a list of namedtuples, containing the results of each game
	"""

	# get a list of every game
	all_games = soup.find_all ( 'div', class_=CONTAINER_CLASS )
	analyzed_games = []

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
			loser_str_list = loser.get_text().split('\n')
			game_result = GameResult (		# create a namedtuple with the following properties
				winner_str_list[1],				# name of winner
				loser_str_list[1],				# name of loser
				winner_str_list[2],				# score of winner
				loser_str_list[2],				# score of loser
				year=yr, week=wk				# year and week numbers
			)
			analyzed_games.append(game_result)	# add this game to the list of analyzed games
		# if there was no winner/loser (e.g. ended in a draw), it will not be added to analyzed_games

	return analyzed_games




def append_results_to_dict ( teams_dict, results ):
	"""
	Add the latest list of results to the Teams in `teams_dict`. `results` 
	should be a list of `GameResult` namedtuples
	"""
	assert isinstance(teams_dict, dict), "Error: teams_dict argument must be a dict"

	# iterate thru each GameResult namedtuple in results 
	for res in results :
		winner_name = res.winner
		loser_name = res.loser

		# for both the loser and winner: if the team name is not in the dict
		# a new Team object must be instantiated for that team
		# the object is added to the teams_dict, whose key will be the name of the team
		if not winner_name in teams_dict :
			winner_obj = Team(winner_name)
			teams_dict[winner_name] = winner_obj
		else :
			winner_obj = teams_dict[winner_name]
		# repeat the process with the loser
		if not loser_name in teams_dict:
			loser_obj = Team(loser_name)
			teams_dict[loser_name] = loser_obj
		else :
			loser_obj = teams_dict[loser_name]

		# now update the beat_list and lost_to_list of the winner and loser
		winner_obj.add_beat_team ( loser_obj )
		loser_obj.add_lost_to_team ( winner_obj )




def post_analysis_sanity_check ( teams_dict ) :
	"""
	Using what we know about the NFL, do a few sanity checks on the data
	"""
	assert len(teams_dict) == 32, "Error: there should be exactly 32 teams in the teams_dict"
	# assert 




###############################################################################
##### MAIN
###############################################################################

def process_week ( year, week_number ):
	# begin by making soup out of the relevant Pro Football Reference page
	soup = get_week_results ( year, week_number )

	# now that we have a page with all the match results of a given week, analyze it
	results = analyze_soup ( soup, year, week_number )

	# the results we got back from analyze_soup can either be formatted to be saved as CSV, or
	# used in building a data structure for further analysis in python
	teams_dict = append_results_to_dict ( script_teams_dict, results )

	# sanity check the data
	post_analysis_sanity_check ( teams_dict )



def main () :
	# iterate thru weeks 1-17 (week_number = wk + 1)
	for wk in range(17):
		process_week ( YEAR, wk+1 ) 

if __name__ == "__main__":
	main()