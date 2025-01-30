


''''
Mech_Pet_1 parrot check_EQ \
--origin "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_equality/directory_1" \
--to "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_equality/directory_2"
"'''

''''
Mech_Pet_1 parrot check_EQ \
--origin "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_inequality/directory_1" \
--to "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_inequality/directory_2"
"'''

''''
Mech_Pet_1 parrot equalize \
--origin "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_equality" \
--to "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_equality_2"

Mech_Pet_1 parrot check_EQ \
--origin "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_equality" \
--to "/Metro/vehicles/Mech_Pet/_health/monitors/parrot/status_1/example_equality_2"
"'''

''''
	TODO:
		Mech_Pet parrot equalize
		Mech_Pet parrot check_EQ
		
		__glossary/Mech_Pet_1
"'''
def check_1 ():
	return;



checks = {
	'check 1': check_1
}