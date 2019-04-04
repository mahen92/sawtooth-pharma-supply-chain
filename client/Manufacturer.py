#!/usr/bin/python3
import hashlib
import base64
import random
import time
import requests
import yaml
import sys
import logging
import optparse
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

class Manufacturer(object):
	def __init__(self, url = "http://rest-api:8008"):
		self.url = url
		# random private key
		context = create_context('secp256k1')
		self.private_key = context.new_random_private_key()
		self.signer = CryptoFactory(context).new_signer(self.private_key)
		self.public_key = self.signer.get_public_key().as_hex()

	def manufacture(self, manufacturerName, medicineName):
		l = [manufacturerName, medicineName]
		manufacturerAddress = getManufacturerAddress(manufacturerName)
		command_string = ','.join(l)
		input_address_list = [MANUFACTURERS_TABLE, manufacturerAddress]
		output_address_list = [manufacturerAddress]
		response = wrap_and_send("manufacture", command_string, input_address_list, output_address_list, wait = 5)
		return yaml.safe_load(response)['data'][0]['status']

	def giveToDistributor(self, manufacturerName, distributer, medicineName):
		l = [manufacturerName, distributer, medicineName]
		command_string = ','.join(l)
		distributerAddress = getDistributerAddress(distributer)
		manufacturerAddress = getManufacturerAddress(manufacturerName)
		input_address_list = [DISTRIBUTERS_TABLE, MANUFACTURERS_TABLE, manufacturerAddress, distributerAddress]
		output_address_list = [manufacturerAddress, distributerAddress]
		response = wrap_and_send("giveTo", command_string, input_address_list, output_address_list, wait = 5)
		return yaml.safe_load(response)['data'][0]['status']