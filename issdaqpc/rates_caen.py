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
import numpy as np

# Settings
THRESHOLD = 10000 # change font colour when threshold reached
NEGATIVE = 5000000 # when the histograms are zeroed, we get a negative value that is unsigned, so a large positive false rate
DAQ_URL =  'http://issdaqpc1:8015/'
DAQ_WSDL_SERVICE_NAME = 'DataAcquisitionControlServer'
SPECTRUM_WSDL_SERVICE_NAME = 'SpectrumService'
FULL_DAQ_URL = DAQ_URL + DAQ_WSDL_SERVICE_NAME
FULL_SPECTRUM_URL = DAQ_URL + SPECTRUM_WSDL_SERVICE_NAME
HEADER = {'content-type': 'text/xml'}
UPDATE_TIME = 2 # seconds


# Channel mapping to MIDAS HISTOGRAM numbers / CAEN ADC channels
RecoilE_chs = [65,67,69,71]
RecoildE_chs = [64,66,68,70]
ELUM_chs = [80,84,82,83]
#ZD_chs = [84,85]
ZD_chs = [86,87]
EBIS_ch = 94
#EBIS_delay_ch = 88
T1_ch = 95
Pulser_ch = 93
Laser_ch = 92
SC_ch = 88
Heimtime_ch = 90
FC_ch = 89


# counts and rates
counts_by_ch = np.zeros(128)
rates_by_ch = np.zeros(128)


# Initialise Colorama
init()

def get_soap_envelope(server,method,params=''):
	body = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance" xmlns:xsd="http://www.w3.org/1999/XMLSchema" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns:%s xmlns:ns="urn:%s">%s</ns:%s></SOAP-ENV:Body></SOAP-ENV:Envelope>' % (method,server,params,method)
	return body
	
def print_rates(name, rate):
	if rate > NEGATIVE or rate < 0:
		print(name + ':\t' + Fore.GREEN + str(0) + Style.RESET_ALL)
	elif rate > THRESHOLD:
		print(name + ':\t' + Fore.RED + str(rate) + Style.RESET_ALL)
	else :
		print(name + ':\t' + Fore.GREEN + str(rate) + Style.RESET_ALL)

def get_rate(bytes, ch):
	rate_ch = bytes[ (ch)*4 : (ch)*4+4]
	rate = int.from_bytes(rate_ch, byteorder='little') / 3
	if rate > NEGATIVE or rate < 0:
		return 0
	else:
		return rate


if __name__ == '__main__':
	
	# Disable warnings related to security certificate checks being bypassed	
	urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

	# Keep the script running
	first_check = True
	while True:

		#
		# First check if the DAQ is going, because the Rate histogram is not reset to zero !!!!
		#
		soap_env = get_soap_envelope(FULL_DAQ_URL,'GetState','')
		try:
			r = requests.post(FULL_DAQ_URL, data=soap_env, headers=HEADER )
		except:
			print("Error getting rates from MIDAS")
			time.sleep( UPDATE_TIME )
			continue
		tree = ET.ElementTree(ET.fromstring(r.text))
		root = tree.getroot()

		daq_is_going = False
		for res in root.iter('State'):
			print(Back.BLUE + 'ISS CAEN DAQ Rates' + Style.RESET_ALL + '       ' + \
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
			spectrum_name = 'Stat'
			params ='<ns:Name xsi:type="xsd:string">%s</ns:Name><ns:Base xsi:type="xsd:int">0</ns:Base><ns:Range xsi:type="xsd:int">512</ns:Range>' % (spectrum_name)

			soap_env = get_soap_envelope(FULL_SPECTRUM_URL,'SpecRead1D',params)
			try:
				r = requests.post(FULL_SPECTRUM_URL, data=soap_env, headers=HEADER )
			except:
				print("Error getting rates from MIDAS")
				time.sleep( UPDATE_TIME )
				continue

			tree = ET.ElementTree(ET.fromstring(r.text))
			root = tree.getroot()

			result = ''

			# Decode the result that is given as base64 binary
			for res in root.iter('result'):
				result = base64.b64decode(res.text)

			payload = ''
			if result != '' and result != None:
				for i in range(len(RecoilE_chs)):
					#print_rates(result, "RecoilE ", RecoilE_chs[i] )
					ch_stat = get_rate(result,RecoilE_chs[i])
					ch_rate = ch_stat - counts_by_ch[RecoilE_chs[i]]
					if ch_rate < 0:
						ch_rate = 0
					ch_rate /= UPDATE_TIME
					counts_by_ch[RecoilE_chs[i]] = ch_stat
					payload += 'detector,name=Recoil,id=E,sector=' + str(i) + ' value=' + str( ch_rate ) + '\n'
					print_rates( 'RecoilE ' + str(i), ch_rate )

				for i in range(len(RecoildE_chs)):
					#print_rates(result, "RecoildE", RecoildE_chs[i])
					ch_stat = get_rate(result,RecoildE_chs[i])
					ch_rate = ch_stat - counts_by_ch[RecoildE_chs[i]]
					if ch_rate < 0:
						ch_rate = 0
					ch_rate /= UPDATE_TIME
					counts_by_ch[RecoildE_chs[i]] = ch_stat					
					payload += 'detector,name=Recoil,id=dE,sector=' + str(i) + ' value=' + str( ch_rate ) + '\n'
					print_rates( 'RecoildE ' + str(i), ch_rate )

				for i in range(len(ELUM_chs)):
					#print_rates(result, "ELUM", ELUM_chs[i])
					ch_stat = get_rate(result,ELUM_chs[i])
					ch_rate = ch_stat - counts_by_ch[ELUM_chs[i]]
					if ch_rate < 0:
						ch_rate = 0
					ch_rate /= UPDATE_TIME
					counts_by_ch[ELUM_chs[i]] = ch_stat					
					payload += 'detector,name=ELUM,sector=' + str(i) + ' value=' + str( ch_rate ) + '\n'
					print_rates( 'ELUM ' + str(i), ch_rate )

				for i in range(len(ZD_chs)):
					#print_rates(result, "ZeroDegree", ZD_chs[i])
					ch_stat = get_rate(result,ZD_chs[i])
					ch_rate = ch_stat - counts_by_ch[ZD_chs[i]]
					if ch_rate < 0:
						ch_rate = 0
					ch_rate /= UPDATE_TIME
					counts_by_ch[ZD_chs[i]] = ch_stat					
					payload += 'detector,name=ZeroDegree,id=' + str(i) + ' value=' + str( ch_rate ) + '\n'
					print_rates( 'ZeroDegree ' + str(i), ch_rate )


				# EBIS
				ch_stat = get_rate(result, EBIS_ch)
				ch_rate = ch_stat - counts_by_ch[EBIS_ch]
				if ch_rate < 0:
					ch_rate = 0
				ch_rate /= UPDATE_TIME
				counts_by_ch[EBIS_ch] = ch_stat
				payload += 'timing,name=EBIS value=' + str( ch_rate ) + '\n'
				print_rates( 'EBIS ' + str(i), ch_rate )
				
				# T1
				ch_stat = get_rate(result, T1_ch)
				ch_rate = ch_stat - counts_by_ch[T1_ch]
				if ch_rate < 0:
					ch_rate = 0
				ch_rate /= UPDATE_TIME
				counts_by_ch[T1_ch] = ch_stat
				payload += 'timing,name=T1 value=' + str( ch_rate ) + '\n'
				print_rates( 'T1 ' + str(i), ch_rate )
				
				# SC
				ch_stat = get_rate(result, SC_ch)
				ch_rate = ch_stat - counts_by_ch[SC_ch]
				if ch_rate < 0:
					ch_rate = 0
				ch_rate /= UPDATE_TIME
				counts_by_ch[SC_ch] = ch_stat
				payload += 'timing,name=SC value=' + str( ch_rate ) + '\n'
				print_rates( 'SC ' + str(i), ch_rate )

				# Pulser
				ch_stat = get_rate(result, Pulser_ch)
				ch_rate = ch_stat - counts_by_ch[Pulser_ch]
				if ch_rate < 0:
					ch_rate = 0
				ch_rate /= UPDATE_TIME
				counts_by_ch[Pulser_ch] = ch_stat
				payload += 'timing,name=Pulser value=' + str( ch_rate ) + '\n'
				print_rates( 'Pulser ' + str(i), ch_rate )
				
				# Laser
				ch_stat = get_rate(result, Laser_ch)
				ch_rate = ch_stat - counts_by_ch[Laser_ch]
				if ch_rate < 0:
					ch_rate = 0
				ch_rate /= UPDATE_TIME
				counts_by_ch[Laser_ch] = ch_stat
				payload += 'timing,name=Laser value=' + str( ch_rate ) + '\n'
				print_rates( 'Laser ' + str(i), ch_rate )
				
				# Heimtime
				ch_stat = get_rate(result, Heimtime_ch)
				ch_rate = ch_stat - counts_by_ch[Heimtime_ch]
				if ch_rate < 0:
					ch_rate = 0
				ch_rate /= UPDATE_TIME
				counts_by_ch[Heimtime_ch] = ch_stat
				payload += 'timing,name=Heimtime value=' + str( ch_rate ) + '\n'
				print_rates( 'Heimtime ' + str(i), ch_rate )
				
				# Send rates to Influx database
				if first_check == False:
					try:
						r = requests.post( 'https://dbod-iss.cern.ch:8080/write?db=rates', data=payload, auth=("admin","issmonitor"), verify=False )
					except:
						pass
				else:
					first_check = False
					continue


		# Sleep for a while and check again
		time.sleep( UPDATE_TIME )
