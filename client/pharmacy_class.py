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
from client import *
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

class pharmacy():
	def __init__(self):
		pass

	def getFromDistributor(self, distributer, pharmacy, batchID, date, action):
		l = [distributer, pharmacy, batchID, date, action]
		command_string = ','.join(l)
		distributerAddress = getDistributerAddress(distributer, "has")
		pharmacyReqAddress = getPharmacyAddress(pharmacy,"request")
		pharmacyHasAddress = getPharmacyAddress(pharmacy,"has")
		batchAddress = getBatchAddress(batchID)
		input_address_list = [DISTRIBUTERS_TABLE, PHARMACY_TABLE, pharmacyReqAddress, pharmacyHasAddress, distributerAddress, batchAddress]
		output_address_list = [distributerAddress, distributerAddress, pharmacyHasAddress, pharmacyReqAddress, batchAddress]
		response = wrap_and_send("getFromDistributer", command_string, input_address_list, output_address_list, wait = 5)
		# print ("give response: {}".format(response))
		return yaml.safe_load(response)['data'][0]['status']


	def listMedicines(self, pharmacyName, qualifier = 'has'):
		address = getPharmacyAddress(pharmacyName, qualifier)
		result = listClients(address)
		if result:
			return result
		else:
			return "No medicines"
		
	def readMedicineBatch(self, batchid):
		address = getBatchAddress(batchid)
		result = listClients(address)
		if result:
			return result
		else:
			return "No such medicine batch"