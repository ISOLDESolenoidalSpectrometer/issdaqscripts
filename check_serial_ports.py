#!/usr/bin/env python3

from serial.tools import list_ports
ports = list_ports.comports()

for port in ports:
	print( port.device, port.manufacturer, port.serial_number )
