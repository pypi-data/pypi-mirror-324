

'''
	mongo connection strings
		
		DB: Mech_Pet
			
			collection: 
				cautionary_ingredients
				essential_nutrients
'''

''''
	https://github.com/jonhoo/fantoccini
"'''

import pathlib
from os.path import dirname, join, normpath
import sys
def add_paths_to_system (paths):
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))
	

add_paths_to_system ([
	'/Metro/vehicles'
])


from Mech_Pet._health import monitor_health

monitor_health ({
	"argv": sys.argv
})


