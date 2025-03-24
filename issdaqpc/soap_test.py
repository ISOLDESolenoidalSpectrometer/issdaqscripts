#!/usr/bin/env python3
#
# Test script to communicate with the MIDAS DAQ using SOAP protocol
# Joonas Konki - 20180613
#
import requests
from xml.etree import ElementTree as ET
import base64

#DAQ_URL =  'http://issdaqpc1:8015/'
DAQ_URL =  'http://localhost:8015/'
DAQ_WSDL_SERVICE_NAME = 'SpectrumService'
FULL_URL = DAQ_URL + DAQ_WSDL_SERVICE_NAME
HEADER = {'content-type': 'text/xml'}

RecoilE_chs = [27,29,32,34]
RecoildE_chs = [28,30,31,33]

def get_soap_envelope(server,method,params=''):
	body = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance" xmlns:xsd="http://www.w3.org/1999/XMLSchema" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns:%s xmlns:ns="urn:%s">%s</ns:%s></SOAP-ENV:Body></SOAP-ENV:Envelope>' % (method,server,params,method)
	return body
	
spectrum_name = 'Rate'
params ='<ns:Name xsi:type="xsd:string">%s</ns:Name><ns:Base xsi:type="xsd:int">0</ns:Base><ns:Range xsi:type="xsd:int">512</ns:Range>' % (spectrum_name)

soap_env = get_soap_envelope(FULL_URL,'SpecRead1D',params)
r = requests.post(FULL_URL, data=soap_env, headers=HEADER )

tree = ET.ElementTree(ET.fromstring(r.text))
root = tree.getroot()

result = ''

# Decode the result that is given as base64 binary
for res in root.iter('result'):
	result = base64.b64decode(res.text)

if result != '':
	i = 1
	for ch in RecoilE_chs:
		rate_ch = result[ 1+(ch-1)*4 : 1+ch*4]
		number = int.from_bytes(rate_ch, byteorder='big')
		print("Recoil-E ch " + str(i) + " rate: " + str(number))
		i+=1
		
	i = 1
	for ch in RecoildE_chs:
		rate_ch = result[ 1+(ch-1)*4 : 1+ch*4]
		number = int.from_bytes(rate_ch, byteorder='big')
		print("Recoil-dE ch " + str(i) + " rate: " + str(number))
		i+=1


