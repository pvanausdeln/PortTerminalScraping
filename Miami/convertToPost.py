import os
import sys
import json
import copy
import requests
import datetime
import glob

class baseInfo:
    postURL = "https://demo-api.iasdispatchmanager.com:8502/v1/bv/shipmentevents"

    shipmentEventBase = {
    "associatedAssetSize": None,
    "associatedUnitId": None,
    "billOfLadingNumber": None,
    "bookingNumber": None,
    "bookingOffice": None,
    "carrierCode": None,
    "carrierName": None,
    "city": None,
    "codeType": None,
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
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "Miami RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["workOrderNumber"] = data["WON"]
    postJson["billOfLadingNumber"] = data["BOL"]
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]
    postJson["longitude"] = -80.16
    postJson["latitude"] = 25.77
    postJson["location"] = "2299 Port Blvd, Miami, FL 33132"
    postJson["country"] = "US"
    postJson["state"] = "FL"
    postJson["city"] = "Miami"
    print(json.dumps(postJson))
    #TODO: config file for post urls
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    return

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        fileList = glob.glob(r""+path+"ContainerInformation\\"+container+'.json', recursive = True) #get all the json steps
        if (not fileList):
            continue
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            EverportPost(step)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])