#!/usr/bin/python3
import traceback
import sys
import hashlib
import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

DEFAULT_URL = 'tcp://validator:4004'

def hash(data):
    return hashlib.sha512(data.encode()).hexdigest()

logging.basicConfig(filename='example.log',level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# namespaces
family_name = "pharma"
FAMILY_NAME = hash(family_name)[:6]

TABLES = hash("tables")[:6]


MANUFACTURER_ENTRIES = hash("manufacturer-entries")[:6]
MANUFACTURERS = hash("manufacturers")
MANUFACTURERS_TABLE = FAMILY_NAME + TABLES + MANUFACTURERS[:58]

DISTRIBUTER_ENTRIES = hash("distributer-entries")[:6]
DISTRIBUTERS = hash("distributers")
DISTRIBUTERS_TABLE = FAMILY_NAME + TABLES + DISTRIBUTERS[:58]

def getDistributerAddress(distributerName):
    distributerName = str(distributerName)
    return FAMILY_NAME + DISTRIBUTER_ENTRIES + hash(distributerName)[:58]

def getManufacturerAddress(manufacturerName):
    return FAMILY_NAME + MANUFACTURER_ENTRIES + hash(manufacturerName)[:58]

class PharmaTransactionHandler(TransactionHandler):
    '''
    Transaction Processor class for the pharma family
    '''
    def __init__(self, namespace_prefix):
        '''Initialize the transaction handler class.
        '''
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        '''Return Transaction Family name string.'''
        return family_name

    @property
    def family_versions(self):
        '''Return Transaction Family version string.'''
        return ['1.0']

    @property
    def namespaces(self):
        '''Return Transaction Family namespace 6-character prefix.'''
        return [self._namespace_prefix]

    # Get the payload and extract the pharma-specific information.
    # It has already been converted from Base64, but needs deserializing.
    # It was serialized with CSV: action, value
    def _unpack_transaction(self, transaction):
        header = transaction.header
        payload_list = self._decode_data(transaction.payload)
        return payload_list

    def apply(self, transaction, context):
        '''This implements the apply function for the TransactionHandler class.
        '''
        LOGGER.info ('starting apply function')
        try:
            payload_list = self._unpack_transaction(transaction)
            LOGGER.info ('payload: {}'.format(payload_list))
            action = payload_list[0]
            try:
                if action == "addManufacturer":
                    manufacturerName = payload_list[1]
                    self._addManufacturer(context, manufacturerName)
                elif action == "addDistributor":
                    distributerName = payload_list[1]
                    self._addDistributer(context, distributerName)
                elif action == "manufacture":
                    manufacturerName = payload_list[1]
                    medicineName = payload_list[2]
                    self._manufacture(context, manufacturerName, medicineName)
                elif action == "giveTo":
                    manufacturerName = payload_list[1]
                    distributerName = payload_list[2]
                    medicineName = payload_list[3]
                    self._giveTo(context, manufacturerName, distributerName, medicineName)
                    action = payload_list[0]
                elif action == "giveToDistributer":
                    manufacturerName = payload_list[1]
                    distributerName = payload_list[2]
                    # medicineDetails = payload_list[3:7]
                    # self._giveToDistributer(context, manufacturerName, distributerName, medicineDetails)
                elif action == "giveToPharmacy":
                    distributerName = payload_list[1]
                    pharmacyName = payload_list[2]
                    medicineDetails = payload_list[3:7]
                    self._giveToPharmacy(context, distributerName, pharmacyName, medicineDetails)
                    action = payload_list[0]
                elif action == "getFromManufacturer":
                    manufacturerName = payload_list[1]
                    distributerName = payload_list[2]
                    medicineDetails = payload_list[3:7]
                    performaction = payload_list[7]
                    self._getFromManufacturer(context,manufacturerName,distributerName,medicineDetails,performaction)
                elif action == "getFromDistributer":
                    ditributerName = payload_list[1]
                    pharmacyName = payload_list[2]
                    medicineDetails = payload_list[3:7]
                    performaction = payload_list[7]
                    self._getFromditributer(context,ditributerName,pharmacyName,medicineDetails,performaction)
                else:
                    LOGGER.debug("Unhandled action: " + action)
            except IndexError as i:
                LOGGER.debug ('IndexError: {}'.format(i))
                raise Exception()
        except Exception as e:
            raise InvalidTransaction("Error: {}".format(e))
            
    @classmethod
    def _addDistributer(self, context, distributerName):
        try:
            LOGGER.info("entering addDist")
            distributers = self._readData(context, DISTRIBUTERS_TABLE)  
            LOGGER.info ('Distributers: {}'.format(distributers))
            if distributers:
                if distributerName not in distributers:
                    distributers.append(distributerName)
                    medicines = []
                    addresses  = context.set_state({
                                    getDistributerAddress(distributerName): self._encode_data(medicines)
                                })
                else:
                    raise Exception('no manufacturer: ' + distributerName)
            else:
                distributers = [distributerName]
            
            addresses  = context.set_state({
                            DISTRIBUTERS_TABLE: self._encode_data(distributers)
                        })
        except Exception as e:
            logging.debug ('exception: {}'.format(e))
            raise InvalidTransaction("State Error")

    @classmethod
    def _addManufacturer(self, context, manufacturerName):
        try:
            LOGGER.info("entering add manufacture")
            manufacturers = self._readData(context, MANUFACTURERS_TABLE)  
            LOGGER.info ('Manufacturers: {}'.format(manufacturers))
            if manufacturers:
                if manufacturerName not in manufacturers:
                    manufacturers.append(manufacturerName)
                    medicines = []
                    addresses  = context.set_state({
                                    getManufacturerAddress(manufacturerName): self._encode_data(medicines)
                                })
                else:
                    raise Exception('no manufacturer: ' + manufacturerName)
            else:
                manufacturers = [manufacturerName]
            
            addresses  = context.set_state({
                            MANUFACTURERS_TABLE: self._encode_data(manufacturers)
                        })
        except Exception as e:
            logging.debug ('excecption: {}'.format(e))
            raise InvalidTransaction("State Error")
    
    @classmethod
    def _manufacture(self, context, manufacturerName, medicineName):
        manufacturerAddress = getManufacturerAddress(manufacturerName)
        try:
            LOGGER.info("entering manufacture")
            manufacturers = self._readData(context, MANUFACTURERS_TABLE)  
            LOGGER.info ('Manufacturers: {}'.format(manufacturers))
            if manufacturers:
                if manufacturerName in manufacturers:
                    medicines = self._readData(context, manufacturerAddress)
                    medicines.append(medicineName)
                    addresses = context.set_state({
                        manufacturerAddress: self._encode_data(medicines)
                    })
                else:
                    raise Exception('no manufacturer: ' + manufacturerName)
            else:
                raise Exception('no manufacturers')
        except Exception as e:
            logging.debug ('excecption: {}'.format(e))
            raise InternalError("State Error")
        
    @classmethod
    def _giveToDistributer(self, context, manufacturerName, distributerName, medicineName):
        LOGGER.info("entering giveTo")
        manufacturerAddress = getManufacturerAddress(manufacturerName)
        distributerAddress = getDistributerAddress(distributerName)
        try:
            manufacturers = self._readData(context, MANUFACTURERS_TABLE)  
            distributers = self._readData(context, DISTRIBUTERS_TABLE)  
            LOGGER.info ('manufacturers: {}'.format(manufacturers))
            LOGGER.info ('distributers: {}'.format(distributers))
            if manufacturerName in manufacturers and distributerName in distributers:
                manufacturedMedicines = self._readData(context, manufacturerAddress)
                if medicineName in manufacturedMedicines:
                    manufacturedMedicines.remove(medicineName)
                    LOGGER.info (medicineName + 'removed')
                    distributerMedicine = self._readData(context, distributerAddress)
                    distributerMedicine.append(medicineName)
                    addresses = context.set_state({
                        manufacturerAddress: self._encode_data(manufacturedMedicines),
                        distributerAddress: self._encode_data(distributerMedicine)
                    })        
                else:
                    pass
            else:
                pass
            LOGGER.info('{} gave {} to {}'.format(manufacturerName, medicineName, distributerName))
        except TypeError as t:
            logging.debug('TypeError in _giveTo: {}'.format(t))
            raise InvalidTransaction('Type error')
        except InvalidTransaction as e:
            logging.debug ('excecption: {}'.format(e))
            raise e
        except Exception as e:
            logging.debug('exception: {}'.format(e))
            raise InvalidTransaction('excecption: {}'.format(e))

    # returns a list
    @classmethod
    def _readData(self, context, address):
        state_entries = context.get_state([address])
        if state_entries == []:
            return []
        data = self._decode_data(state_entries[0].data)
        return data

    # returns a list
    @classmethod
    def _decode_data(self, data):
        return data.decode().split(',')

    # returns a csv string
    @classmethod
    def _encode_data(self, data):
        return ','.join(data).encode()


def main():
    try:
        # Setup logging for this class.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

        # Register the Transaction Handler and start it.
        processor = TransactionProcessor(url=DEFAULT_URL)
        sw_namespace = FAMILY_NAME
        handler = PharmaTransactionHandler(sw_namespace)
        processor.add_handler(handler)
        processor.start()
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()