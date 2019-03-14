import os
import sys
import json
import copy
import requests
import datetime
import glob

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

def EverportPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)

        postJson["resolvedEventSource"] = "TRAPAC LA RPA"
        postJson["location"] = "630 W Harry Bridges Blvd, Wilmington, CA 90744"
        postJson["city"] = "Los Angeles"
        postJson["state"] = "CA"
        postJson["country"] = "US"
        postJson["latitude"] = 33.77
        postJson["longitude"] = -118.27
        postJson["vessel"] = data["Vessel"]
        postJson["voyageNumber"] = data["Voyage"]
        postJson["billOfLadingNumber"] = data["BOLNumber"]
        postJson["workOrderNumber"] = data["WONumber"]

        postJson["eventTime"] = data["Datetime"]

        print(json.dumps(postJson))




def main(containerList):
    for container in containerList:
        fileList = glob.glob(r"C:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\TPLA\\ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
        if (not fileList):
            return
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            EverportPost(step)

if __name__=="__main__":
    main(sys.argv[1])