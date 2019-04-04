#!/usr/bin/python3
from client import *
import hashlib
import base64
import random
import time
import requests
import yaml
import sys
import logging
import optparse
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from flask import Flask, render_template, request


logging.basicConfig(filename='client.log',level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

parser = optparse.OptionParser()
parser.add_option('-U', '--url', action = "store", dest = "url", default = "http://rest-api:8008")

# def hash(data):
#     return hashlib.sha512(data.encode()).hexdigest()

family_name = "pharma"
FAMILY_NAME = hash(family_name)[:6]

TABLES = hash("tables")[:6]


MANUFACTURER_ENTRIES = hash("manufacturer-entries")[:6]
MANUFACTURERS = hash("manufacturers")
MANUFACTURERS_TABLE = FAMILY_NAME + TABLES + MANUFACTURERS[:58]

DISTRIBUTER_ENTRIES = hash("distributer-entries")[:6]
DISTRIBUTERS = hash("distributers")
DISTRIBUTERS_TABLE = FAMILY_NAME + TABLES + DISTRIBUTERS[:58]

PHARMACY_ENTRIES = hash("pharmacy-entries")[:6]
PHARMACY = hash("pharmacy")
PHARMACY_TABLE = FAMILY_NAME + TABLES + PHARMACY[:58]

# random private key
context = create_context('secp256k1')
private_key = context.new_random_private_key()
signer = CryptoFactory(context).new_signer(private_key)
public_key = signer.get_public_key().as_hex()

base_url = 'http://rest-api:8008'


# def getManufacturerAddress(manufacturerName):
#     return FAMILY_NAME + MANUFACTURER_ENTRIES + hash(manufacturerName)[:58]

# def getDistributerAddress(distributerName):
#     distributerName = str(distributerName)
#     return FAMILY_NAME + DISTRIBUTER_ENTRIES + hash(distributerName)[:58]

app=Flask(__name__)

@app.route("/")
def fun1():
	return render_template('admin.html')

@app.route('/addDist', methods = ['POST','GET'])
def fun2():
    # return "hello"
	# if request.method=='POST':
	distributer= request.form['name']
	k = addDistributer(distributer)
	if(k=="COMMITTED"):
        
		return render_template('alert.html',command="ADDED DISTRIBUTORS",port="5000")
	else:
        
		return render_template('alert.html',command="SOMETHING FAILED! \nOOPS!", port="5000")

@app.route('/addManu', methods=['POST', 'GET'])
def fun3():
    manufacturer= request.form['name']

    k= addManufacturer(manufacturer)
    if(k=="COMMITTED"):
        
        return render_template('alert.html',command="ADDED MANUFACTURER",port="5000")
    else:
        
       return render_template('alert.html',command="SOMETHING FAILED! \nOOPS!", port="5000")

@app.route('/addHos', methods=['POST', 'GET'])
def fun4():
    Med= request.form['name']

    k= addDistributer(distributor)
    if(k=="COMMITTED"):
        
        return render_template('alert.html',command="ADDED DISTRIBUTOR",port="5000")
    else:
        
       return render_template('alert.html',command="SOMETHING FAILED! \nOOPS!",port="5000")

@app.route('/listManu', methods=['POST', 'GET'])
def fun5():
        return render_template('alert.html',command=listClients(MANUFACTURERS_TABLE),port="5000")

@app.route('/listDis', methods=['POST', 'GET'])
def fun6():
        return render_template('alert.html',command=listClients(DISTRIBUTERS_TABLE),port="5000")
@app.route('/listHos', methods=['POST', 'GET'])
def fun7():        
        return render_template('alert.html',command=listClients(PHARMACY_TABLE),port="5000")

# def addManufacturer(manufacturerName):
#     logging.info ('addManufacturer({})'.format(manufacturerName))
#     input_address_list = [MANUFACTURERS_TABLE]
#     output_address_list = [MANUFACTURERS_TABLE, getManufacturerAddress(manufacturerName)]
#     response = wrap_and_send("addManufacturer", manufacturerName, input_address_list, output_address_list, wait = 5)
#     # print ("manufacture response: {}".format(response))
#     return yaml.safe_load(response)['data'][0]['status']

# def addDistributer(distributerName):
#     logging.info ('addDistributer({})'.format(distributerName))
#     input_address_list = [DISTRIBUTERS_TABLE]
#     output_address_list = [DISTRIBUTERS_TABLE, getDistributerAddress(distributerName)]
#     response = wrap_and_send("addDistributor", distributerName, input_address_list, output_address_list, wait = 5)
#     # print ("manufacture response: {}".format(response))
#     return  yaml.safe_load(response)['data'][0]['status']

# def listClients(clientAddress):
#     result = send_to_rest_api("state/{}".format(clientAddress))
#     try:
#         return (base64.b64decode(yaml.safe_load(result)["data"])).decode()
#     except BaseException:
#         return None

# def send_to_rest_api(suffix, data=None, content_type=None):
#     url = "{}/{}".format(base_url, suffix)
#     headers = {}
#     logging.info ('sending to ' + url)
#     if content_type is not None:
#         headers['Content-Type'] = content_type

#     try:
#         if data is not None:
#             result = requests.post(url, headers=headers, data=data)
#             logging.info ("\nrequest sent POST\n")
#         else:
#             result = requests.get(url, headers=headers)
#         if not result.ok:
#             logging.debug ("Error {}: {}".format(result.status_code, result.reason))
#             raise Exception("Error {}: {}".format(result.status_code, result.reason))
#     except requests.ConnectionError as err:
#         logging.debug ('Failed to connect to {}: {}'.format(url, str(err)))
#         raise Exception('Failed to connect to {}: {}'.format(url, str(err)))
#     except BaseException as err:
#         raise Exception(err)
#     return result.text

# def wait_for_status(batch_id, result, wait = 10):
#     '''Wait until transaction status is not PENDING (COMMITTED or error).
#         'wait' is time to wait for status, in seconds.
#     '''
#     if wait and wait > 0:
#         waited = 0
#         start_time = time.time()
#         logging.info ('url : ' + base_url + "batch_statuses?id={}&wait={}".format(batch_id, wait))
#         while waited < wait:
#             result = send_to_rest_api("batch_statuses?id={}&wait={}".format(batch_id, wait))
#             status = yaml.safe_load(result)['data'][0]['status']
#             waited = time.time() - start_time

#             if status != 'PENDING':
#                 return result
#         logging.debug ("Transaction timed out after waiting {} seconds.".format(wait))
#         return "Transaction timed out after waiting {} seconds.".format(wait)
#     else:
#         return result

# def wrap_and_send(action, data, input_address_list, output_address_list, wait=None):
#     '''Create a transaction, then wrap it in a batch.
#     '''
#     payload = ",".join([action, str(data)])
#     logging.info ('payload: {}'.format(payload))

#     # Construct the address where we'll store our state.
#     # Create a TransactionHeader.
#     header = TransactionHeader(
#         signer_public_key = public_key,
#         family_name = family_name,
#         family_version = "1.0",
#         inputs = input_address_list,         # input_and_output_address_list,
#         outputs = output_address_list,       # input_and_output_address_list,
#         dependencies = [],
#         payload_sha512 = hash(payload),
#         batcher_public_key = public_key,
#         nonce = random.random().hex().encode()
#     ).SerializeToString()

#     # Create a Transaction from the header and payload above.
#     transaction = Transaction(
#         header = header,
#         payload = payload.encode(),                 # encode the payload
#         header_signature = signer.sign(header)
#     )

#     transaction_list = [transaction]

#     # Create a BatchHeader from transaction_list above.
#     header = BatchHeader(
#         signer_public_key = public_key,
#         transaction_ids = [txn.header_signature for txn in transaction_list]
#     ).SerializeToString()

#     # Create Batch using the BatchHeader and transaction_list above.
#     batch = Batch(
#         header = header,
#         transactions = transaction_list,
#         header_signature = signer.sign(header)
#     )

#     # Create a Batch List from Batch above
#     batch_list = BatchList(batches=[batch])
#     batch_id = batch_list.batches[0].header_signature
#     # Send batch_list to the REST API
#     result = send_to_rest_api("batches", batch_list.SerializeToString(), 'application/octet-stream')

#     # Wait until transaction status is COMMITTED, error, or timed out
#     return wait_for_status(batch_id, result, wait = wait)

# def giveToDistributor(manufacturerName, distributer, medicineName):
#     l = [manufacturerName, distributer, medicineName]
#     command_string = ','.join(l)
#     distributerAddress = getDistributerAddress(distributer)
#     manufacturerAddress = getManufacturerAddress(manufacturerName)
#     input_address_list = [DISTRIBUTERS_TABLE, MANUFACTURERS_TABLE, manufacturerAddress, distributerAddress]
#     output_address_list = [manufacturerAddress, distributerAddress]
#     response = wrap_and_send("giveTo", command_string, input_address_list, output_address_list, wait = 5)
#     # print ("give response: {}".format(response))
#     return yaml.safe_load(response)['data'][0]['status']

if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0")
