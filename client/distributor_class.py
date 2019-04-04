#!/bin/python3
import hashlib
import base64
import random
import time
import requests
import yaml
import sys
import logging
import optparse
import client_class
from utils import *
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

class distributer(client_class.client):
	def __init__(self):
		super.__init__(self)


	def getFromManufacturer(self, manufacturerName, distributer, medicineName,batchID,manufactureDate,expiryDate , action):
		l = [manufacturerName, distributer, medicineName,batchID,manufactureDate,expiryDate,action]
		command_string = ','.join(l)
		distributerAddress = getDistributerAddress(distributer,"request")
		manufacturerAddress = getManufacturerAddress(manufacturerName)
		input_address_list = [DISTRIBUTERS_TABLE, MANUFACTURERS_TABLE, manufacturerAddress, distributerAddress]
		output_address_list = [manufacturerAddress, distributerAddress]
		response = self.wrap_and_send("getFromManufacturer", command_string, input_address_list, output_address_list, wait = 5)
		# print ("give response: {}".format(response))
		return yaml.safe_load(response)['data'][0]['status']

	def giveToPharmacy(self, distributer, pharmacy, medicineName,batchID,manufactureDate,expiryDate):
		l = [distributer, pharmacy, medicineName,batchID,manufactureDate,expiryDate]
		command_string = ','.join(l)
		distributerAddress = getDistributerAddress(distributer,"has")
		pharmacyAddress = getPharmacyAddress(pharmacy,"request")
		input_address_list = [DISTRIBUTERS_TABLE, PHARMACY_TABLE,pharmacyAddress, distributerAddress]
		output_address_list = [pharmacyAddress, distributerAddress]
		response = self.wrap_and_send("giveToPharmacy", command_string, input_address_list, output_address_list, wait = 5)
		# print ("give response: {}".format(response))
		return yaml.safe_load(response)['data'][0]['status']
