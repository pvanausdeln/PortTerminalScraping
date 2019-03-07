import sys
import os
import requests
import json
import copy
import datetime

class baseInfo:
    postURL = "https://demo-api.iasdispatchmanager.com:8502/v1/shipmentevents"

    shipmentEventBase = {
    "associatedAssetSize": None,
    "associatedUnitId": None,
    "billOfLadingNumber": None,
    "bookingNumber": None,
    "bookingOffice": None,
    "carrierCode": None,
    "carrierName": None,
    "city": None,
    "consigneeName": None,
    "containerBookingNumber": None,
    "country": None,
    "createdBy": None,
    "customerOrderReferenceNumber": None,
    "destinationCity": None,
    "destinationSPLC": None,
    "destinationState": None,
    "eventCode": None,
    "eventName": None,
    "eventTime": None,
    "houseBill": None,
    "importReferenceNumber": None,
    "latitude": 0,
    "location": None,
    "longitude": 0,
    "masterBill": None,
    "notes": None,
    "onHandNumber": None,
    "originSPLC": None,
    "originatorCode": None,
    "originatorId": 0,
    "originatorName": None,
    "postalCode": None,
    "purchaseOrderReferenceNumber": None,
    "railBillingNumber": None,
    "reasonCode": None,
    "reasonName": None,
    "receiverCode": None,
    "receiverName": None,
    "reportSource": None,
    "reportedBy": None,
    "resolvedEventId": 0,
    "resolvedEventOriginalId": 0,
    "resolvedEventSource": None,
    "resolvedEventStatus": None,
    "sealNumber": None,
    "shipmentReferenceNumber": None,
    "signedBy": None,
    "state": None,
    "stopType": None,
    "terminalCode": None,
    "terminalFunction": None,
    "unitId": None,
    "unitSize": 0,
    "unitState": None,
    "unitTypeCode": None,
    "vessel": None,
    "voyageNumber": None,
    "workOrderNumber": None
    }

def Seattle18Post(container):
    if(os.path.isfile(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\SeattleTerminal46\\ContainerInformation\\"+container+"Vessel.json") == False): #is there a Vessel event
        return

    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    #TODO: Fill info that is same for Vessel and Load events

    loadPostJson = None
    if(os.path.isfile(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\SeattleTerminal46\\ContainerInformation\\"+container+"Load.json") == True): #is there a Load event
        loadPostJson = copy.deepcopy(postJson)

    #TODO: Fill info for Vessel event information
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)

    if(loadPostJson != None):
        #TODO: fill in Load event information
        headers = {'content-type':'application/json'}
        r = requests.post(baseInfo.postURL, data = json.dumps(loadPostJson), headers = headers, verify = False)
        print(r)

def main(containerList):
    for container in containerList:
        Seattle18Post(container)

if __name__ == "__main__":
    main(sys.argv[1])