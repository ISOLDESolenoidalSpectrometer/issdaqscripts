#!/usr/bin/env python3

import sys
from serial.tools import list_ports

ports = list_ports.comports()
module = sys.argv[1]

if module == 'iss00':
	serial = 'FT5ZCJIX'
elif module == 'iss01':
	serial = 'FT5Z6QIP'
elif module == 'iss02':
#	serial = "FT5Z6TFW"
	serial = "FT5ZEXR5"
elif module == 'iss03':
#	serial = "FT5ZEXR5"
	serial = "FT5Z6TFW"

for port in ports:

	if serial == port.serial_number:
		sys.stdout.write(port.device)
		sys.stdout.write('\n')
		sys.exit(0)
	else:
		continue

