#!/usr/bin/env python3
#
# Test script to communicate with the MIDAS DAQ using SOAP protocol
# Gets the status of the DAQ (running or not) and prints rates for certain
# channels. Sends rates to a Influx database.
# Joonas Konki - 20180614
#
# Update by Liam Gaffney for new DAQ 19/07/2021
import sys
import requests
import time, datetime
from xml.etree import ElementTree as ET
import base64
from colorama import init, Fore, Back, Style
import urllib3
import numpy as np

# Settings
MODULE = 0
THRESHOLD = 10000 # change font colour when threshold reached
NEGATIVE = 500000000 # when the histograms are zeroed, we get a negative value that is unsigned, so a large positive false rate
DAQ_URL =  'http://iss0' + str(MODULE) + ':8015/'
DAQ_WSDL_SERVICE_NAME = 'DataAcquisitionControlServer'
SPECTRUM_WSDL_SERVICE_NAME = 'SpectrumService'
FULL_DAQ_URL = DAQ_URL + DAQ_WSDL_SERVICE_NAME
FULL_SPECTRUM_URL = DAQ_URL + SPECTRUM_WSDL_SERVICE_NAME
HEADER = {'content-type': 'text/xml'}
UPDATE_TIME = 20 # seconds

# Channel mapping to MIDAS HISTOGRAM numbers / ISS Array
Array0_chs = [6144,6145,6146,6147,6148,6149,6150,6151,6152,6153,6154,6155,6156,6157,6158,6159,6160,6161,6162,6163,6164,6165,6166,6167,6168,6169,6170,6171,6172,6173,6174,6175,6176,6177,6178,6179,6180,6181,6182,6183,6184,6185,6186,6187,6188,6189,6190,6191,6192,6193,6194,6195,6196,6197,6198,6199,6200,6201,6202,6203,6204,6205,6206,6207,6208,6209,6210,6211,6212,6213,6214,6215,6216,6217,6218,6219,6220,6221,6222,6223,6224,6225,6226,6227,6228,6229,6230,6231,6232,6233,6234,6235,6236,6237,6238,6239,6240,6241,6242,6243,6244,6245,6246,6247,6248,6249,6250,6251,6252,6253,6254,6255,6256,6257,6258,6259,6260,6261,6262,6263,6264,6265,6266,6267,6268,6269,6270,6271]
Array1_chs = [6283,6284,6285,6286,6287,6288,6289,6290,6291,6292,6293,6300,6301,6302,6303,6304,6305,6306,6307,6308,6309,6310,6361,6362,6363,6364,6365,6366,6367,6368,6369,6370,6371,6378,6379,6380,6381,6382,6383,6384,6385,6386,6387,6388]
Array2_chs = [6400,6401,6402,6403,6404,6405,6406,6407,6408,6409,6410,6411,6412,6413,6414,6415,6416,6417,6418,6419,6420,6421,6422,6423,6424,6425,6426,6427,6428,6429,6430,6431,6432,6433,6434,6435,6436,6437,6438,6439,6440,6441,6442,6443,6444,6445,6446,6447,6448,6449,6450,6451,6452,6453,6454,6455,6456,6457,6458,6459,6460,6461,6462,6463,6464,6465,6466,6467,6468,6469,6470,6471,6472,6473,6474,6475,6476,6477,6478,6479,6480,6481,6482,6483,6484,6485,6486,6487,6488,6489,6490,6491,6492,6493,6494,6495,6496,6497,6498,6499,6500,6501,6502,6503,6504,6505,6506,6507,6508,6509,6510,6511,6512,6513,6514,6515,6516,6517,6518,6519,6520,6521,6522,6523,6524,6525,6526,6527]
Array3_chs = [6528,6529,6530,6531,6532,6533,6534,6535,6536,6537,6538,6539,6540,6541,6542,6543,6544,6545,6546,6547,6548,6549,6550,6551,6552,6553,6554,6555,6556,6557,6558,6559,6560,6561,6562,6563,6564,6565,6566,6567,6568,6569,6570,6571,6572,6573,6574,6575,6576,6577,6578,6579,6580,6581,6582,6583,6584,6585,6586,6587,6588,6589,6590,6591,6592,6593,6594,6595,6596,6597,6598,6599,6600,6601,6602,6603,6604,6605,6606,6607,6608,6609,6610,6611,6612,6613,6614,6615,6616,6617,6618,6619,6620,6621,6622,6623,6624,6625,6626,6627,6628,6629,6630,6631,6632,6633,6634,6635,6636,6637,6638,6639,6640,6641,6642,6643,6644,6645,6646,6647,6648,6649,6650,6651,6652,6653,6654,6655]
Array4_chs = [6667,6668,6669,6670,6671,6672,6673,6674,6675,6676,6677,6684,6685,6686,6687,6688,6689,6690,6691,6692,6693,6694,6745,6746,6747,6748,6749,6750,6751,6752,6753,6754,6755,6762,6763,6764,6765,6766,6767,6768,6769,6770,6771,6772]
Array5_chs = [6784,6785,6786,6787,6788,6789,6790,6791,6792,6793,6794,6795,6796,6797,6798,6799,6800,6801,6802,6803,6804,6805,6806,6807,6808,6809,6810,6811,6812,6813,6814,6815,6816,6817,6818,6819,6820,6821,6822,6823,6824,6825,6826,6827,6828,6829,6830,6831,6832,6833,6834,6835,6836,6837,6838,6839,6840,6841,6842,6843,6844,6845,6846,6847,6848,6849,6850,6851,6852,6853,6854,6855,6856,6857,6858,6859,6860,6861,6862,6863,6864,6865,6866,6867,6868,6869,6870,6871,6872,6873,6874,6875,6876,6877,6878,6879,6880,6881,6882,6883,6884,6885,6886,6887,6888,6889,6890,6891,6892,6893,6894,6895,6896,6897,6898,6899,6900,6901,6902,6903,6904,6905,6906,6907,6908,6909,6910,6911]
Array_chs = [Array0_chs,Array1_chs,Array2_chs,Array3_chs,Array4_chs,Array5_chs]
Pulser_chs = [2239,2623]

# Per channel stats
Array_stats = [np.zeros( len(Array0_chs) ),np.zeros( len(Array1_chs) ),np.zeros( len(Array2_chs) ),np.zeros( len(Array3_chs) ),np.zeros( len(Array4_chs) ),np.zeros( len(Array5_chs) )]
Pulser_stats = np.zeros( len(Pulser_chs) )


# Initialise Colorama
init()

def get_soap_envelope(server,method,params=''):
	body = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance" xmlns:xsd="http://www.w3.org/1999/XMLSchema" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns:%s xmlns:ns="urn:%s">%s</ns:%s></SOAP-ENV:Body></SOAP-ENV:Envelope>' % (method,server,params,method)
	return body
	
def print_rates(bytes, name, rate):
	if rate > NEGATIVE or rate < 0:
		print(name + Fore.GREEN + str(0) + Style.RESET_ALL)
	elif rate > THRESHOLD:
		print(name + Fore.RED + str(rate) + Style.RESET_ALL)
	else :
		print(name + Fore.GREEN + str(rate) + Style.RESET_ALL)

def get_rate(bytes, ch):
	rate_ch = bytes[ (ch)*4 : (ch)*4+4]
	rate = int.from_bytes(rate_ch, byteorder='big')
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
		except OSError:
			print( "FMC not powered, or maybe crashed?" )
			time.sleep( UPDATE_TIME )
			continue
		tree = ET.ElementTree(ET.fromstring(r.text))
		root = tree.getroot()
	
		daq_is_going = False
		for res in root.iter('State'):
			print(Back.BLUE + 'iss0' + str(MODULE) + ' DAQ Rates' + Style.RESET_ALL + '       ' + \
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
			params ='<ns:Name xsi:type="xsd:string">%s</ns:Name><ns:Base xsi:type="xsd:int">0</ns:Base><ns:Range xsi:type="xsd:int">8192</ns:Range>' % (spectrum_name)
		
			soap_env = get_soap_envelope(FULL_SPECTRUM_URL,'SpecRead1D',params)
			r = requests.post(FULL_SPECTRUM_URL, data=soap_env, headers=HEADER )
		
			tree = ET.ElementTree(ET.fromstring(r.text))
			root = tree.getroot()
		
			result = ''
		
			# Decode the result that is given as base64 binary
			for res in root.iter('result'):
				result = base64.b64decode(res.text)
		
			payload = ''
			if result != '' and result != None:

				for i in range( len(Array_chs) ):

					asic_rate = 0
					for j in range( len(Array_chs[i]) ):
						ch_stat = get_rate(result,Array_chs[i][j])
						ch_rate = ch_stat - Array_stats[i][j]
						if ch_rate < 0:
							ch_rate = 0
						ch_rate /= UPDATE_TIME
						Array_stats[i][j] = ch_stat
						#payload += 'detector,name=Array,module=' + str(MODULE) + ',asic=' + str(i) + ',channel=' + str(j) + ' value=' + str(ch_rate) + '\n'
						asic_rate += ch_rate
					payload += 'detector,name=Array,module=' + str(MODULE) + ',asic=' + str(i) + ' value=' + str(asic_rate) + '\n'
					print_rates(result, 'Array - Module ' + str(MODULE) + ' ASIC ' + str(i) + ' = ', asic_rate )
		
				for i in range(len(Pulser_chs)):
					ch_stat = get_rate(result,Pulser_chs[i])
					ch_rate = ch_stat - Pulser_stats[i]
					if ch_rate < 0:
						ch_rate = 0
					ch_rate /= UPDATE_TIME
					Pulser_stats[i] = ch_stat
					payload += 'timing,name=ASIC,module=' + str(MODULE) + ',pulser=' + str(i) + ' value=' + str(ch_rate) + '\n'
					print_rates(result, 'Pulser ' + str(i) + ' = ', ch_rate )
		
			# Send to influx
			if first_check == False:
				try:
					r = requests.post( 'https://dbod-iss.cern.ch:8080/write?db=rates', data=payload, auth=("admin","issmonitor"), verify=False )
				except InsecureRequestWarning:
					pass

			else:
				first_check = False
				continue
		
		# Wait for next update
		time.sleep( UPDATE_TIME )	
	
