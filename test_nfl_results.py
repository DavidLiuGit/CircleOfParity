import unittest
import nfl_results
from soupify import soupify


class TestNflResults (unittest.TestCase):

	year = 2018
	week = 1


	def test_build_results_url (self):
		# verify that the URL built is valid
		url = nfl_results.build_results_url ( self.year, self.week )
		print ( url )
		self.assertTrue ( url )
		self.assertGreater ( len(url), len(nfl_results.BASE_URL) )

		# verify that the year and week numbers are part of the url
		self.assertTrue ( url.index(str(self.year)) )
		self.assertTrue ( url.index(str(self.week)) )
		self.assertTrue ( url.endswith('.htm') )	# should NOT end with .html; just .htm


	def test_get_week_results (self):
		# verify that we have an object returned
		self.assertTrue ( 
			nfl_results.get_week_results (self.year, self.week)
		)

