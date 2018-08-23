import nfl_results
import sys
from pprint import pprint
from collections import namedtuple


###############################################################################
##### DATA STRUCTURES
###############################################################################


GameResult = namedtuple ( 'GameResult', 'winner loser winner_score loser_score year week' )

# linked list (bi-directional)
LL = namedtuple ( 'LL', ['this', 'next', 'prev'] )


class Team:

	def __init__ ( self, name ):
		self.name = name
		self.beat_list = []
		self.lost_to_list = []
		self.visited = False

	def add_beat_team ( self, beaten_team_obj ):
		self.beat_list.append (beaten_team_obj)

	def add_lost_to_team ( self, lost_to_team_obj ):
		self.lost_to_list.append (lost_to_team_obj)

	def __str__ ( self ):
		return "{}: {} wins, {} losses".format( self.name, len(self.beat_list), len(self.lost_to_list))

	def __repr__ ( self ):
		return "{}: {} wins, {} losses".format( self.name, len(self.beat_list), len(self.lost_to_list))



###############################################################################
##### HELPER FUNCTIONS
###############################################################################

def ham_depth_first_search ( team, path_list, max_depth ):
	"""
	Use depth-first search to traverse thru the graph. To complete the DFS, the following must be satisfied:
	1. the number of vertices visited == max_depth (no vertex can be visited more than once)
	2. the last vertex must have an edge leading to the first vertex (to complete a Ham. cycle)
	"""

	# add this team to the path list, and mark it as visited
	path_list.append ( team )
	team.visited = True
	
	# check the number of vertices in the path list to see if the conditions are satisfied
	if len(path_list) == max_depth:			# if condition 1 is satisfied, then
		if path_list[0] in team.beat_list:		# if condition 2 is satisfied, return True
			print ( 'Found a Hamiltonian cycle!' )	# but first, celebrate
			pprint ( path_list )
			return True								# both conditions satisfied; we've got the cycle!
		else: 									# if condition 2 is NOT satisfied, then
			team.visited = False					# reset the visited flag
			path_list.pop()							# remove the last element of the list, and
			return False							# stop and return False
	
	# if the path list is not yet full (i.e. condition 1 not satisfied)
	else :
		# for each team that this team beat:
		for beaten_team in team.beat_list:
			# optionally, check if the beaten_team is the same as the first team in the path_list
			if beaten_team == path_list[0]:
				print ( 'Found a cycle of length {}'.format ( len(path_list) ) )
			
			# if the team has already been visited, skip it
			if beaten_team.visited :
				continue

			# recursively call this function with the new team; this will do the search depth-first
			ret = ham_depth_first_search ( beaten_team, path_list, max_depth )
			
			# if the recursive call is successful, then we've found the cycle!
			if ret: 
				return True
			# otherwise, we need to keep looking
	
	# if the conditions have NOT been satisfied, AND all DFS attempts have failed, then we need to move on
	path_list.pop()					# make sure to remove this team from the path_list
	team.visited = False			# reset the visited flag
	return False






def brute_force ( teams_dict ):
	"""
	Attempt to find a Hamiltonian cycle (which is the circle of parity) using brute force.
	Good luck. This may take forever.
	"""
	print ( "Attempting to find circle of parity using brute force. This can take a while..." )

	# create a list of teams from teams_dict, ranked by number of wins (ascending)
	teams_list = list ( teams_dict.values() )
	num_wins_sorted = sorted ( teams_list, key=lambda x: len(x.beat_list) )
	# num_loss_sorted = sorted ( teams_list, key=lambda x: len(x.lost_to_list) )

	# some variables to track progress
	max_depth = len ( teams_dict )	# the hamiltonian cycle must visit this many vertices, EXACTLY once

	# determine seeds: use the team with most wins (best_seed), and team with least wins (worst_seed)
	best_seed = num_wins_sorted[-1]			# currently not in use
	worst_seed= num_wins_sorted[0]			
	
	# use a map to track the path explored
	ham_map = []
	result = ham_depth_first_search ( worst_seed, ham_map, max_depth )
	return ham_map





def presolve_sanity_check ( teams_dict, strict_circle=True ):
	"""
	Make sure that the data is formatted correctly, and that a circle of parity is possible.
	If 1 or more teams do not have a win/loss, then a circle is NOT possible
	"""
	
	for team in teams_dict.values():
		# how should we do this check? make sure team is an instance of Team
		# assert team is Team, "Error: object is not instance of Team, but {} instead".format(type(team))
		if strict_circle:
			assert len(team.beat_list), "Error: a circle of parity CANNOT be created. {} does not have any wins".format(team)
			assert len(team.lost_to_list), "Error: a circle of parity CANNOT be created. {} does not have any losses".format(team)

	print ( "Presolve sanity check OK" )
	return True




def postsolve_sanity_check ( teams_dict, ham_map ):
	"""
	Did we really find a Hamiltonian cycle? Or is this script bullshittin' on front street
	"""
	assert len(teams_dict) == len(set(ham_map)), "Error: the number of teams in the map is incorrect; there may have been duplicates"

	# iterate thru each team in the map, and make sure that each is valid
	for i in range(len(teams_dict)):
		# assert isinstance ( ham_map[i], Team ), "Error: element in ham_map is NOT an instance of Team"
		assert ham_map[i] in ham_map[i-1].beat_list, "Error: {} did NOT beat {}. WTF?".format(ham_map[i-1].name, ham_map[i].name)

	print ( "Postsolve sanity check OK" )
	return True





###############################################################################
##### MAIN
###############################################################################

def main ( args ) :

	# invoke the main function in nfl_results to get a dict
	# dict contains graph nodes - representing teams, 
	# each with references (vertices) to other teams that they beat/lost to

	teams_dict = nfl_results.main ( 'iasdfjaosdokf' )
	pprint ( teams_dict )

	# do a sanity check first
	try:
		presolve_sanity_check ( teams_dict )
	except AssertionError as e:
		print (e)
		exit(1)
	
	ham_map = brute_force ( teams_dict )
	try:
		postsolve_sanity_check ( teams_dict, ham_map )
	except AssertionError as e:
		print (e)
		print ( "Error: failed postsolve sanity check" )
		exit(1)

	print ( "\n\nFound a Hamiltonian cycle, and therefore, a Circle of Parity:" )
	pprint (ham_map)




# if this script is being executed from cmd line, get 2016 results unless year specified
if __name__ == "__main__":
	main ( sys.argv )