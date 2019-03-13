import os
import sys
import json
import copy
import requests
import datetime
import glob
import csv

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

def APMLAEvent(row, postJson):
    return postJson

def APMLAPost(container):
    if(os.path.isfile(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\APMLA\\ContainerInformation\\"+container+".json") == False): #is there a legitimate event
        return
    if(os.path.isfile(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\APMLA\\ContainerInformation\\"+container+".csv") == False):
        return
    with open(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\APMLA\\ContainerInformation\\"+container+".json") as jsonData:
        data = json.load(jsonData)
    with open(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\APMLA\\ContainerInformation\\"+container+".csv") as csvData:
        csv_reader = csv.reader(csvData, delimiter=',')

    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    postJson["unitId"] = data["Container"]
    postJson["billOfLadingNumber"] = data["Bill of Lading"]
    postJson["unitSize"] = data["Size/Type/Height"].split("/")[0]
    postJson["unitType"] = data["Size/Type/Height"].split("/")[1]
    postJson["terminalCode"] = data["Terminal"]

    postJson["location"] = "2500 Navy Way, San Pedro, CA 90731"
    postJson["city"] = "Los Angeles"
    postJson["state"] = "CA"
    postJson["country"] = "US"
    postJson["latitude"] = 33.72
    postJson["longitude"] = -118.25

    postJson["resolvedEventSource"] = "APM LA RPA"
    postJson["shipmentReferenceNumber"] = data["ReferenceNumber"]
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]

    for row in csv_reader:
        print(row)
        postJson = APMLAEvent(row, postJson)
    print(json.dumps(postJson))
    return

def main(containerList):
        APMLAPost(containerList)

if __name__ == "__main__":
    main(sys.argv[1])
