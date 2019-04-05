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

class admin():
    def __init__(self):
        pass

    def addManufacturer(self, manufacturerName):
        logging.info('addManufacturer({})'.format(manufacturerName))
        input_address_list = [MANUFACTURERS_TABLE]
        output_address_list = [MANUFACTURERS_TABLE,
                               getManufacturerAddress(manufacturerName)]
        response = wrap_and_send(
            "addManufacturer", manufacturerName, input_address_list, output_address_list, wait=5)
        # print ("manufacture response: {}".format(response))
        return yaml.safe_load(response)['data'][0]['status']

    def addDistributer(self, distributerName):
        logging.info('addDistributer({})'.format(distributerName))
        distHasAddress = getDistributerAddress(distributerName, "has")
        distReqAddress = getDistributerAddress(distributerName, "request")
        input_address_list = [DISTRIBUTERS_TABLE]
        output_address_list = [DISTRIBUTERS_TABLE,
                               distHasAddress, distReqAddress]
        response = wrap_and_send(
            "addDistributor", distributerName, input_address_list, output_address_list, wait=5)
        print ("manufacture response: {}".format(response))
        return yaml.safe_load(response)['data'][0]['status']

    def addPharmacy(self, PharmacyName):
        logging.info('addPharmacy({})'.format(PharmacyName))
        PharmacyReqAddress = getPharmacyAddress(PharmacyName, "request")
        PharmacyHasAddress = getPharmacyAddress(PharmacyName, "has")
        input_address_list = [PHARMACY_TABLE]
        output_address_list = [PHARMACY_TABLE,
                               PharmacyHasAddress, PharmacyReqAddress]
        response = wrap_and_send(
            "addPharmacy", PharmacyName, input_address_list, output_address_list, wait=5)
        # print ("manufacture response: {}".format(response))
        return yaml.safe_load(response)['data'][0]['status']

    def listClients(self, clientAddress):
        result = send_to_rest_api("state/{}".format(clientAddress))
        try:
            return (base64.b64decode(yaml.safe_load(result)["data"])).decode()
        except BaseException:
            return None

    def listPharmacies(self):
        # address = getPharmacyAddress(pharmacyName)
        return listClients(PHARMACY_TABLE)

    def listDistributers(self):
        # address = getDistributerAddress(DistributerName)
        return listClients(DISTRIBUTERS_TABLE)

    def listManufacturers(self):
        # address = getManufacturerAddress(ManufacturerName)
        return listClients(MANUFACTURERS_TABLE)        
    
