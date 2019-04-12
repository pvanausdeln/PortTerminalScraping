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

def getEvent(event):
    if(event.find("Vessel Rc") != -1):
        return("VA", "Vessel Arrival")
    elif(event.find("Vessel Dl") != -1):
        return("UV", "Unloaded from Vessel")
    elif(event.find("Gate Rcv") != -1):
        return("I", "INGATE")
    elif(event.find("Gate Dlvr") != -1):
        return("OA", "OUTGATE")
    return(None, None)

def WWTPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        if(data["Terminal"].find("WWT") == -1):
            return
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)
        
        postJson["reportSource"] = "OceanEvent"
        postJson["resolvedEventSource"] = "WWT RPA"
        postJson["workOrderNumber"] = data["WONumber"]
        postJson["billOfLadingNumber"] = data["BOLNumber"]
        postJson["vessel"] = data["Vessel"]
        postJson["voyageNumber"] = data["Voyage"]

        postJson["longitude"] = -79.88
        postJson["latitude"] = 32.83
        postJson["location"] = "Mt Pleasant, SC 29464"
        postJson["country"] = "US"
        postJson["state"] = "SC"
        postJson["city"] = "Charleston"

        postJson["unitSize"] = data["Container Type"][0:2]
        postJson["unitType"] = data["Container Type"][2:2]
        postJson["eventCode"], postJson["eventName"] = getEvent(data["Transaction"])
        postJson["eventTime"] = ''.join(x for x in data["Datetime"] if x in string.printable)

        if(postJson["eventCode"] is None):
            return
        headers = {'content-type':'application/json'}
        r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
        print(r)

def main(containerList):
    for container in containerList:
        fileList = glob.glob(r"C:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\WWT\\ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
        if (not fileList):
            return
        fileList = [f for f in fileList if containerList in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            WWTPost(step)

if __name__ == "__main__":
    main(sys.argv[1])