#!/bin/env python3
#
# Script to communicate with the MIDAS DAQ using SOAP protocol
# Gets the status of the DAQ status and TapeServer status
# then sends info to an Influx database
# Liam Gaffney - 20230427
#
# Thanks to Joonas Konki (Miniball + ISS fellow 2017-2019) for initial script
import sys
import glob
import os
import shutil
import requests
import time, datetime
from xml.etree import ElementTree as ET
import base64
from colorama import init, Fore, Back, Style
import urllib3
import numpy as np

# Settings
DAQ_HOST = 'lipc-4'
DAQ_WSDL_SERVICE_NAME = 'DataAcquisitionControlServer'
TAPE_HOST = 'mbdaq'
TAPE_WSDL_SERVICE_NAME = 'TapeServer'
HEADER = {'content-type': 'text/xml'}
UPDATE_TIME = 2 # seconds

# Initialise Colorama
init()

def get_soap_envelope(server,method,params=''):
	body = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance" xmlns:xsd="http://www.w3.org/1999/XMLSchema" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns:%s xmlns:ns="urn:%s">%s</ns:%s></SOAP-ENV:Body></SOAP-ENV:Envelope>' % (method,server,params,method)
	return body

if __name__ == '__main__':

	# Disable warnings related to security certificate checks being bypassed
	urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

	print( 'hello' )

	previous_tape_status = '-2'

	# Keep the script running
	while True:

		payload = ''

		FULL_TAPE_URL = 'http://' + str(TAPE_HOST) + ':8015/' + str(TAPE_WSDL_SERVICE_NAME)
		soap_env = get_soap_envelope(FULL_TAPE_URL,'InquireAcqStatus','')
		r = None
		try:
			r = requests.post( FULL_TAPE_URL, data=soap_env, headers=HEADER )
		except OSError:
			payload += 'tape,name=' + str(TAPE_HOST) + ' state=-1' + '\n'
			print( payload )

		if r is not None:
			tree = ET.ElementTree(ET.fromstring(r.text))
			root = tree.getroot()

			for res in root.iter():
				if res.text is not None:
					tape_status = res.text.split()
					if len(tape_status) == 6:
						payload += 'tape,name=' + str(TAPE_HOST) + ' state=' + str(tape_status[1])
						if str(tape_status[1]) == '2' and previous_tape_status == '1':
							payload += ',run=' + str(tape_status[5]) + ',mode=2' + '\n'
						elif str(tape_status[1]) == '1' and previous_tape_status == '2':
							payload += ',run=' + str(int(tape_status[5])-1) + ',mode=1' + '\n'
						else:
							payload += '\n'
						previous_tape_status = str(tape_status[1])

					else:
						payload += 'tape,name=' + str(TAPE_HOST) + ' state=-2\n'
						previous_tape_status = '-2'

					data_folders = sorted( glob.iglob('/TapeData/*'), key=os.path.getctime, reverse=True)
					for folder in data_folders:
						if os.path.isdir(folder):
							list_of_files = glob.glob(folder + '/*')
							try:
								latest_file = max(list_of_files, key=os.path.getctime)
							except:
								latest_file = 'Error'
								file_size = 0
								file_time = 0
								continue
							file_size = os.stat(latest_file).st_size
							file_time = os.path.getmtime(latest_file) * 1000.0
							break
						else:
							latest_file = 'Error'
							file_size = 0
							file_time = 0

					disk_free = shutil.disk_usage('/TapeData/').free
					disk_used = shutil.disk_usage('/TapeData/').used

					if str(tape_status[1]) == '2':
						payload += 'file filename=\"' + str(latest_file) + '\",size=' + str(file_size) + \
							',free=' + str(disk_free) + ',used=' + str(disk_used) + ',modified=' + str(file_time) + '\n'
					else:
						payload += 'file free=' + str(disk_free) + ',used=' + str(disk_used) + '\n'



		DAQ_URL =  'http://' + str(DAQ_HOST) + ':8015/'
		FULL_DAQ_URL = DAQ_URL + DAQ_WSDL_SERVICE_NAME

		soap_env = get_soap_envelope(FULL_DAQ_URL,'GetState','')
		r = None
		try:
			r = requests.post( FULL_DAQ_URL, data=soap_env, headers=HEADER )
		except OSError:
			payload += 'daq,name=' + str(DAQ_HOST) + ',state=-1' + '\n'


		if r is not None:
			tree = ET.ElementTree(ET.fromstring(r.text))
			root = tree.getroot()

			for res in root.iter('State'):
				if 'going' in res.text:
					payload += 'daq,name=' + str(DAQ_HOST) + ' state=3' + '\n'
				elif 'error' in res.text:
					payload += 'daq,name=' + str(DAQ_HOST) + ' state=4' + '\n'
				elif 'reset' in res.text:
					payload += 'daq,name=' + str(DAQ_HOST) + ' state=5' + '\n'
				elif 'stop' in res.text:
					payload += 'daq,name=' + str(DAQ_HOST) + ' state=1' + '\n'
				else:
					payload += 'daq,name=' + str(DAQ_HOST) + ' state=-2' + '\n'


		# Send to influx
		try:
			print( payload )
			r = requests.post( 'https://dbod-miniball.cern.ch:8080/write?db=daq', data=payload, auth=("admin","miniballmonitor"), verify=False )
		except InsecureRequestWarning:
			pass
		except ConnectionError:
			print("Error connecting to DBOD server, waiting extra cycle")
			time.sleep( UPDATE_TIME )


		# Wait for next update
		time.sleep( UPDATE_TIME )

