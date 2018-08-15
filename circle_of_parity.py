import nfl_results
import sys
from pprint import pprint



###############################################################################
##### HELPER FUNCTIONS
###############################################################################

def brute_force ( teams_dict ):
	"""
	Attempt to find a Hamiltonian path (which is the circle of parity) using brute force.
	Good luck. This may take forever.
	"""
	print ( "Attempting to find circle of parity using brute force. This can take a while..." )

	# create a list of teams from teams_dict, ranked by number of wins (ascending)
	teams_list = list ( teams_dict.values() )
	num_wins_sorted = sorted ( teams_list, key=lambda x: len(x.beat_list) )
	num_loss_sorted = sorted ( teams_list, key=lambda x: len(x.lost_to_list) )



def presolve_sanity_check ( teams_dict, strict_circle=True ):
	"""
	Make sure that the data is formatted correctly, and that a circle of parity is possible.
	If 1 or more teams do not have a win/loss, then a circle is NOT possible
	"""
	
	for team in teams_dict.values():
		assert isinstance ( team, nfl_results.Team ), "Error: object is not instance of nfl_results.Team"
		if strict_circle:
			assert len(team.beat_list), "Error: a circle of parity CANNOT be created. {} does not have any wins".format(team)
			assert len(team.lost_to_list), "Error: a circle of parity CANNOT be created. {} does not have any losses".format(team)

	print ( "Presolve sanity check OK" )
	return True




###############################################################################
##### MAIN
###############################################################################

def main ( args ) :

	# invoke the main function in nfl_results to get a dict
	# dict contains graph nodes - representing teams, 
	# each with references (vertices) to other teams that they beat/lost to
	teams_dict = nfl_results.main ( 2016 )
	pprint ( teams_dict )

	# do a sanity check first
	try:
		presolve_sanity_check ( teams_dict )
	except AssertionError as e:
		print (e)
		exit(1)
	
	brute_force ( teams_dict )


	# create a list of teams from teams_dict, ranked by number of wins (ascending)
	# teams_list = list ( teams_dict.values() )
	# num_wins_sorted = sorted ( teams_list, key=lambda x: len(x.beat_list) )
	# num_loss_sorted = sorted ( teams_list, key=lambda x: len(x.lost_to_list) )
	
	# pprint ( num_wins_sorted )
	# pprint ( num_loss_sorted )



if __name__ == "__main__":
	main ( sys.argv )