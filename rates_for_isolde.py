#!/usr/bin/env python3
#
# Test script to communicate with the MIDAS DAQ using SOAP protocol
# Gets the status of the DAQ (running or not) and prints rates for certain
# channels. Sends rates to a Influx database.
# Joonas Konki - 20180614
#
# Edited by Liam Gaffney for the 2021 ISS runs... Thanks Joonas!!
#
import requests
import time, datetime
from xml.etree import ElementTree as ET
import base64
from colorama import init, Fore, Back, Style
import urllib3
import socket
import json
import sys
import random
import numpy as np

# Settings
THRESHOLD = 10000 # change font colour when threshold reached
NEGATIVE = 5000000 # when the histograms are zeroed, we get a negative value that is unsigned, so a large positive false rate
DAQ_URL =  'http://issdaqpc:8015/'
DAQ_WSDL_SERVICE_NAME = 'DataAcquisitionControlServer'
SPECTRUM_WSDL_SERVICE_NAME = 'SpectrumService'
FULL_DAQ_URL = DAQ_URL + DAQ_WSDL_SERVICE_NAME
FULL_SPECTRUM_URL = DAQ_URL + SPECTRUM_WSDL_SERVICE_NAME
HEADER = {'content-type': 'text/xml'}

# For ISOLDE server
HOST, PORT = 'cs-ccr-isoop', 9701
Beamline='XT02'

# Channel mapping to MIDAS HISTOGRAM numbers / CAEN ADC channels
RecoilE_chs = [64,74,73,71]
RecoildE_chs = [65,75,72,70]
ELUM_chs = [80,81,82,83]
ZD_chs = [86,87]
EBIS_ch = 94
T1_ch = 95
Pulser_ch = 93

# Initialise Colorama
init()

def get_soap_envelope(server,method,params=''):
	body = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance" xmlns:xsd="http://www.w3.org/1999/XMLSchema" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns:%s xmlns:ns="urn:%s">%s</ns:%s></SOAP-ENV:Body></SOAP-ENV:Envelope>' % (method,server,params,method)
	return body
	
def print_rates(bytes, name, ch):
	rate_ch = bytes[ (ch)*4 : (ch)*4+4]
	rate_ch_int = int.from_bytes(rate_ch, byteorder='little') / 3
	if rate_ch_int > NEGATIVE:
		print(name + " (ch %3d): " % ch + Fore.GREEN + str(0) + Style.RESET_ALL)
	elif rate_ch_int > THRESHOLD:
		print(name + " (ch %3d): " % ch + Fore.RED + str(rate_ch_int) + Style.RESET_ALL)
	else :
		print(name + " (ch %3d): " % ch + Fore.GREEN + str(rate_ch_int) + Style.RESET_ALL)

def get_rate(bytes, ch):
	rate_ch = bytes[ (ch)*4 : (ch)*4+4]
	rate = int.from_bytes(rate_ch, byteorder='little') / 3
	if rate > NEGATIVE:
		return 0
	else:
		return rate


if __name__ == '__main__':
	
	# Disable warnings related to security certificate checks being bypassed	
	urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

	random.seed()
	ELUM_rates = np.zeros( len(ELUM_chs) )

	# Keep the script running
	while True:

		#
		# First check if the DAQ is going, because the Rate histogram is not reset to zero !!!!
		#
		soap_env = get_soap_envelope(FULL_DAQ_URL,'GetState','')
		r = requests.post(FULL_DAQ_URL, data=soap_env, headers=HEADER )
		tree = ET.ElementTree(ET.fromstring(r.text))
		root = tree.getroot()

		daq_is_going = False
		for res in root.iter('State'):
			print(Back.BLUE + 'ISS DAQ Rates' + Style.RESET_ALL + '       ' + \
				  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			if 'going' in res.text:
				print('                        ' + Back.GREEN + ' DAQ is GOING! ' + Style.RESET_ALL)
				daq_is_going = True
		
		if not daq_is_going:
			print('                        ' + Back.RED + ' DAQ is STOPPED !? ' + Style.RESET_ALL)

		else:

			#
			# Get the Rate histogram from SpectrumService WSDL service
			#
			spectrum_name = 'Rate'
			params ='<ns:Name xsi:type="xsd:string">%s</ns:Name><ns:Base xsi:type="xsd:int">0</ns:Base><ns:Range xsi:type="xsd:int">512</ns:Range>' % (spectrum_name)

			soap_env = get_soap_envelope(FULL_SPECTRUM_URL,'SpecRead1D',params)
			r = requests.post(FULL_SPECTRUM_URL, data=soap_env, headers=HEADER )

			tree = ET.ElementTree(ET.fromstring(r.text))
			root = tree.getroot()

			result = ''

			# Decode the result that is given as base64 binary
			for res in root.iter('result'):
				result = base64.b64decode(res.text)

			if result != '' and result != None:

				data2send={"Beamline":Beamline, "AllData":[]}
				
				for i in range(len(ELUM_chs)):

					print_rates(result, "ELUM", ELUM_chs[i])
					ELUM_rates[i] = get_rate(result,ELUM_chs[i])
					DataName = "ELUM" + str(i)
					DataText = "ELUM" + str(i)
					DataPiece = {"Name": DataName,"DataText": DataText,"Data": ELUM_rates[i]}
					JSONName = "Data"
					if i < 10:
						JSONName += "0"
					JSONName += str(i)

					data2send["AllData"].append( {JSONName:DataPiece} )

				data = json.dumps(data2send)

				print( data )

				try:

					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.connect((HOST, PORT))
					sock.sendall(bytes(data,encoding="utf-8"))
					
				finally:

					sock.close()

		# Sleep for a while and check again
		time.sleep(2)

