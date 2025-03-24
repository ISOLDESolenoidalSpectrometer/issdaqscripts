#!/usr/bin/env python3
#
# Read the temperature registers from the CAEN modules
#
# Liam Gaffney - 20/03/2025
#
import sys
import glob
import os
import requests
import shutil
import time, datetime
from xml.etree import ElementTree as ET
import base64
import urllib3
import numpy as np

# Settings
DAQ_HOST = 'issdaqpc1'
DAQ_WSDL_SERVICE_NAME = 'VMEAccessServer'
HEADER = {'content-type': 'text/xml'}
TIMEOUT = 1 # seconds
UPDATE_TIME = 5 # seconds

# Information on modules
NMOD = 2
NCH = 16

# List of registers
board_registers = [ 'AcqStatus', 'BoardFail', 'BoardFailStatus', 'ChShutDown', 'Config', 'EventSize', 'VMEStatus' ]
ch_registers = [ 'ADCTemp', 'Status' ]


def return_register(soap_env):
	# Extract the register after building the soap envelope
	r = None
	try:
		r = requests.post( FULL_DAQ_URL, data=soap_env, headers=HEADER, timeout=TIMEOUT )
	except Exception as e:
		print(e)
		return None

	# check that we got something in return
	if r is not None:
		tree = ET.ElementTree(ET.fromstring(r.text))
		root = tree.getroot()

		# iterate, but return the first time we get a result
		for res in root.iter('result'):
			integer_result = int( res.text, 0 )
			return integer_result

	# return a blank string if we fail
	return None


def get_soap_envelope(server,method,params=''):
	body = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance" xmlns:xsd="http://www.w3.org/1999/XMLSchema" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns:%s xmlns:ns="urn:%s">%s</ns:%s></SOAP-ENV:Body></SOAP-ENV:Envelope>' % (method,server,params,method)
	return body

if __name__ == '__main__':

	# Disable warnings related to security certificate checks being bypassed
	urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

	# Keep the script running
	while True:

		payload = ''

		# DAQ info
		DAQ_URL =  'http://' + str(DAQ_HOST) + ':8015/'
		FULL_DAQ_URL = DAQ_URL + DAQ_WSDL_SERVICE_NAME

		# Loop over modules
		for mod in range(NMOD):

			# Loop over all requested board registers
			for regID in range( len(board_registers) ):

				# board register
				register_name = 'v1725psd#' + str(mod+1) + '.' + str(board_registers[regID])
				params ='<ns:Register xsi:type="xsd:string">%s</ns:Register>' % (register_name)
				soap_env = get_soap_envelope(FULL_DAQ_URL,'ReadRegister',params)
				result = return_register(soap_env)

				# add it to the paylod
				if result is not None:
					payload += 'registers,daq=' + str(DAQ_HOST) + ',mod=' + str(mod) + ',ch=-1'
					payload += ',name=' + str(board_registers[regID]) + ' value=' + str(result) + '\n'

			# Loop over channels
			for ch in range(NCH):

				# Loop over all channel registers
				for regID in range( len(ch_registers) ):

					# channel register name
					register_name = 'v1725psd#' + str(mod+1) + '.Ch' + str(ch) + '.' + str(ch_registers[regID])
					params ='<ns:Register xsi:type="xsd:string">%s</ns:Register>' % (register_name)
					soap_env = get_soap_envelope(FULL_DAQ_URL,'ReadRegister',params)
					result = return_register(soap_env)

					# add it to the paylod
					if result is not None:
						payload += 'registers,daq=' + str(DAQ_HOST) + ',mod=' + str(mod) + ',ch=' + str(ch)
						payload += ',name=' + str(ch_registers[regID]) + ' value=' + str(result) + '\n'


		# Send to influx
		try:
			print( payload )
			r = requests.post( 'https://dbod-iss.cern.ch:8080/write?db=daq', data=payload, auth=("admin","issmonitor"), verify=False )
		except Exception as e:
			print(e)

		# Wait for next update
		time.sleep( UPDATE_TIME )

