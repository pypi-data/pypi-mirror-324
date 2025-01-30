



##
#

#
#
##


#/
#
import click
#
#
from Mech_Pet.adventures.sanique.venture import sanique_venture
from Mech_Pet.adventures.demux_hap.venture import demux_hap_venture
#
#
from Mech_Pet._essence import retrieve_essence
#
#
from ventures import ventures_map
#
#\


from Mech_Pet.adventures.harbor_basin import turn_on_harbor
from Mech_Pet._essence import turn_off_external_essence
	

def ventures_group ():
	# essence = retrieve_essence ()

	@click.group ("harbor")
	def group ():
		pass;
	
	
	@group.command ("open")
	def command__health ():	
		turn_off_external_essence ()
		turn_on_harbor ({});
	
	
	return group;






#



