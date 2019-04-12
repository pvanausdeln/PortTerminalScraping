import sys
import os
import requests
import json
import copy
import datetime
import glob
import string

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

def MaherPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)
        
        postJson["reportSource"] = "OceanEvent"
        postJson["resolvedEventSource"] = "Maher RPA"
        postJson["workOrderNumber"] = data["WONumber"]
        postJson["billOfLadingNumber"] = data["BOLNumber"]
        postJson["vessel"] = data["Vessel"]
        postJson["voyageNumber"] = data["Voyage"]

        postJson["longitude"] = -74.13
        postJson["latitude"] = 40.66
        postJson["location"] = "1210 Corbin St, Elizabeth, NJ 07201"
        postJson["country"] = "US"
        postJson["state"] = "NY"
        postJson["city"] = "New York"

        #TODO: all the scraped event data
        
        headers = {'content-type':'application/json'}
        r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
        print(r)

def main(containerList):
    for container in containerList:
        fileList = glob.glob(str(os.getcwd())+"\\ContainerInformation\\"+container+'.json', recursive = True) #get all the json steps
        if (not fileList):
            return
        MaherPost(fileList[0])

if __name__ == "__main__":
    main(sys.argv[1])