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
from manufacturer_class import manufacturer
logging.basicConfig(filename='client.log',level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

parser = optparse.OptionParser()
parser.add_option('-U', '--url', action = "store", dest = "url", default = "http://rest-api:8008")
parser.add_option('--manu-date', action = "store", dest = "manu_date", default = "4/4/19")
parser.add_option('--exp-date', action = "store", dest = "exp_date", default = "4/4/19")
parser.add_option('--batchId', action = "store", dest = "batchId", default = "0")

if __name__ == '__main__':
    manu = manufacturer()
    try:
        opts, args = parser.parse_args()
        # base_url = opts.url
        if sys.argv[1] == "manufacture":
            logging.info ('manufacture command: ' + sys.argv[2])
            result = manu.manufacture(sys.argv[2], sys.argv[3]) #, opts.batchID, opts.mau_date, opts.exp_date)
            if result == 'COMMITTED':
                logging.info (sys.argv[2] + " manufactured.")
                print ("Manufactured " + sys.argv[2])
            else:
                logging.info (sys.argv[2] + " not manufactured.")
                print ("\n{} not manufctured ".format(sys.argv[3]))
        elif sys.argv[1] == "giveto":
            logging.info ('giveto command: distributer: {}, medicine: {}'.format(sys.argv[2], sys.argv[3]))
            result = manu.giveToDistributor(sys.argv[2], sys.argv[3], sys.argv[4]) #, opts.batchID, opts.mau_date, opts.exp_date)
            if result == 'COMMITTED':
                logging.info ('Distributed - distributer: {}, medicine: {}'.format(sys.argv[2], sys.argv[3]))
                print ('Distributed - distributer: {}, medicine: {}'.format(sys.argv[2], sys.argv[3]))
            else:
                logging.info ("Didn't Distributed - distributer: {}, medicine: {}".format(sys.argv[2], sys.argv[3]))
                print ("Didn't Distributed - distributer: {}, medicine: {}".format(sys.argv[2], sys.argv[3]))
        else:
            print ('Invalid command.\nValid commands: \n\taddManufacturer manufacturerName, addDistributer name, \n\tmanufacture mname medicine name, giveto mname dname medicineName, \n\tlistManufacturers, listDistributers, seeManufacturer mname, seeDistributer dname')
    except IndexError as i:
        logging.debug ('Invalid command')
        print ('Invalid command.\nValid commands: \n\taddManufacturer manufacturerName, addDistributer name, \n\tmanufacture mname medicine name, giveto mname dname medicineName, \n\tlistManufacturers, listDistributers, seeManufacturer mname, seeDistributer dname')
        print (i)
    except Exception as e:
        print (e)
