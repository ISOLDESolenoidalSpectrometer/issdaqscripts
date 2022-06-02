#!/usr/bin/env python3

import vme8100lib

from serial.tools import list_ports
ports = list_ports.comports()

# Look for the VME crate
for port in ports:

	# It looks like the N1419 modules, FTDI is manufacturer, but no serial number
	if port.serial_number == None and port.manufacturer == 'FTDI':
	
		# We need to open it even if it is a N1419 (which might be locked)
		crate = vme8100lib.VME8100( port=port.device, baud=9600 )
		if crate.get_lock_state() is True:
		
			# Ask for the name, which will be an error for N1419 and VME8100 for the crate
			if crate.get_name() == 'VME8100':

				# Found it
				print("Found VME8100 unit (" + str(crate.get_serial_number()) + ") in port: " + str(port.device) )

				# Now we send command
				crate.get_fan_speed()
				
				# And close up
				crate.close()
				break

			# If it isn't a crate, close the device and move on
			print("This is not a VME crate")
			crate.close()

