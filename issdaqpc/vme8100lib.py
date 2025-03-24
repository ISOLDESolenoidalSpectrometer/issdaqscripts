# -*- coding: utf-8 -*-
"""
The library for controlling the CAEN VME8100 VME crate via
the USB serial control interface.

Protocol data format is 9600 baud 8N1 (8 bit, no parity, 1 stop bit)
There is no echo of the input before the response from the unit.
"""


import serial
import time
import re
import fasteners

LOCK_TIMEOUT = 1
LOCK_PATH = '/tmp/'

class VME8100():
	def __init__(self,port,baud):
		lock_file = port[4:]+'.lock'
		self.lock = fasteners.InterProcessLock(LOCK_PATH + lock_file)
		self.lockstate = False
		if self.lock.acquire(timeout=LOCK_TIMEOUT):
			print('Lockfile acquired successfully: ' + LOCK_PATH + lock_file )
			self.lockstate = True
			self.port = port
			self.ser = serial.Serial( port=self.port, baudrate=baud, timeout=1, xonxoff=True )
			time.sleep(0.1) # Wait 100 ms after opening the port before sending commands
			self.ser.flushInput() # Flush the input buffer of the serial port before sending any new commands
			time.sleep(0.1)
		else:
			print('Lockfile could not be acquired for port ' + port)
			print('Is there another program using the a CAEN device here??')
			return

	def get_lock_state(self):
		return self.lockstate

	def close(self):
		"""The function closes and releases the serial port connection attached to the unit.

		"""
		self.ser.close()
		self.lock.release()

	def send_command(self, command=''):
		"""The function sends a command to the unit and returns the response string.

		"""
		if command == '': return ''
		self.ser.write( command.encode('utf-8') )
		time.sleep(0.1)
		#self.ser.readline() # read out echoed command (no echo in N1419)
		return self.ser.readline() # return response from the unit

	def flush_input_buffer(self):
		""" Flush the input buffer of the serial port.
		"""
		self.ser.flushInput()

	def set_on(self):
		"""The function turns the crate ON."""

		response = self.send_command( '$CMD:SET,CH:8,PAR:ON\r' )

	def set_off(self):
		"""The function turns the crate OFF."""

		response = self.send_command( '$CMD:SET,CH:8,PAR:OFF\r' )

	def vme_reset(self):
		"""The function sends VME system reset command."""

		response = self.send_command( '$CMD:SET,CH:8,PAR:SYSR\r' )

	def clear_alarm(self):
		"""The function clears the alarms."""

		response = self.send_command( '$CMD:SET,CH:8,PAR:CLR\r' )

	def get_name(self):
		"""The function returns the name of the crate, hopefully 'VME8100'."""
		response = self.send_command( '$CMD:MON,CH:8,PAR:CRNAME\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\w*)', linestr, re.IGNORECASE)

		if pattern is not None:
		
			if pattern.group(2) == 'OK':
			
				name = str(pattern.group(3)).rstrip('\r')
				return name
				
			else:
			
				print( pattern.group(2) )
				return 0.
				
		else:
			print( linestr )
			return -1

	def get_serial_number(self):
		"""The function returns the serial number of the crate."""
		response = self.send_command( '$CMD:MON,CH:8,PAR:PSSNUM\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\w*)', linestr, re.IGNORECASE)

		if pattern is not None:
		
			if pattern.group(2) == 'OK':
			
				snum = str(pattern.group(3)).rstrip('\r')
				return snum
				
			else:
			
				print( pattern.group(2) )
				return 0.
				
		else:
			print( linestr )
			return -1


	def get_power(self):
		"""The function returns the power status of the crate.
		Return value is 0 for OFF and 1 for ON
		"""
		response = self.send_command( '$CMD:MON,CH:8,PAR:CRST\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\d*)', linestr, re.IGNORECASE)

		if pattern is not None:
		
			if pattern.group(2) == 'OK':

				status = int(pattern.group(3))
				return status & 1
					
			else:
				print( linestr )
				return -1

		else:
			print( linestr )
			return -1

	def get_status(self):
		"""The function returns the status value and messages from the crate."""
		response = self.send_command( '$CMD:MON,CH:8,PAR:CRST\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\d*)', linestr, re.IGNORECASE)

		if pattern is not None:
		
			if pattern.group(2) == 'OK':
			
				status = int(pattern.group(3))
				if status & 2048:
					print( "Temperature fail" )
				if status & 1024:
					print( "Fan fail" )
				if status & 512:
					print( "Fan is ON" )
				else:
					print( "Fan is OFF" )
				if status & 32:
					print( "VME system fail" )
				if status & 16:
					print( "AC fail" )
				if status & 4:
					print( "Temperature fail" )
				if status & 2:
					print( "VCC supply fail" )
				if status & 1:
					print( "Crate is ON" )
				else:
					print( "Crate is OFF" )

					
				return status
				
			else:
				print( pattern.group(2) )
				return -1
				
		else:
			print( linestr )
			return -1


	def get_temperature(self):
		"""The function returns the temperature of the crate."""
		response = self.send_command( '$CMD:MON,CH:8,PAR:PSTEMP\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\d*.\d*)', linestr, re.IGNORECASE)

		if pattern is not None:

			if pattern.group(2) == 'OK':

				temp = float(pattern.group(3))
				print( "Crate temperature = {t}˚C".format(t=temp) )

			else:
				print( pattern.group(2) )
				return -1
				
		else:
			print( linestr )
			return -1


	def get_fan_speed(self):
		"""The function returns the fan speed for all fans and the set point."""
		response = self.send_command( '$CMD:MON,CH:8,PAR:FANSP\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\d*)', linestr, re.IGNORECASE)

		if pattern is not None:
		
			if pattern.group(2) == 'OK':

				speed = int(pattern.group(3))
				if( speed == 0 ):
					print( "Fan off" )
				if( speed == 1 ):
					print( "Fan speed set to ~1500 Rpm" )
				if( speed == 2 ):
					print( "Fan speed set to ~1800 Rpm" )
				if( speed == 3 ):
					print( "Fan speed set to ~2000 Rpm" )
				if( speed == 4 ):
					print( "Fan speed set to ~2300 Rpm" )
				if( speed == 5 ):
					print( "Fan speed set to ~2600 Rpm" )
				if( speed == 6 ):
					print( "Fan speed set to ~3000 Rpm" )

			else:
				print( linestr )
				return -1

		else:
			print( linestr )
			return -1
			
		# Then individual speeds - Fan 1
		response = self.send_command( '$CMD:MON,CH:8,PAR:FAN1\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\d*.\d*)', linestr, re.IGNORECASE)

		if pattern is not None:

			if pattern.group(2) == 'OK':

				speed = float(pattern.group(3))
				print( "Fan 1 speed = {sp} Rpm".format(sp=speed) )

		# Then individual speeds - Fan 2
		response = self.send_command( '$CMD:MON,CH:8,PAR:FAN2\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\d*.\d*)', linestr, re.IGNORECASE)

		if pattern is not None:

			if pattern.group(2) == 'OK':

				speed = float(pattern.group(3))
				print( "Fan 2 speed = {sp} Rpm".format(sp=speed) )

		# Then individual speeds - Fan 3
		response = self.send_command( '$CMD:MON,CH:8,PAR:FAN2\r' )
		linestr = response.decode('utf8')
		pattern = re.match(r'#(\w*):(\w*),VAL:(\d*.\d*)', linestr, re.IGNORECASE)

		if pattern is not None:

			if pattern.group(2) == 'OK':

				speed = float(pattern.group(3))
				print( "Fan 3 speed = {sp} Rpm".format(sp=speed) )
