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

def NewarkPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)

        postJson["resolvedEventSource"] = "NEWARK RPA"
        postJson["location"] = "241 Calcutta St, Newark, NJ 07114"
        postJson["city"] = "Newark"
        postJson["state"] = "NJ"
        postJson["country"] = "US"
        postJson["latitude"] = 40.69
        postJson["longitude"] = -74.15
        postJson["unitId"] = data["Container Number"]
        postJson["vessel"] = data["Vessel"]
        postJson["voyageNumber"] = data["Voyage"]
        postJson["billOfLadingNumber"] = data["BOLNumber"]
        postJson["workOrderNumber"] = data["WONumber"]
        postJson["reportSource"] = "OceanEvent"

        postJson["receiverName"] = data["Trucker"]
        postJson["carrierCode"] = data["SSCO"]
        postJson["unitSize"] = data["Length"].strip("'")

        if(data["Customs Status"].find("RELEASED") != -1):
            postJson["eventCode"], postJson["eventName"] = ("CT", "Customs Release")
            postJson["eventTime"] = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            headers = {'content-type':'application/json'}
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
        if(data["Freight Status"].find("RELEASED") != -1):
            postJson["eventCode"], postJson["eventName"] = ("FS", "Freight Release")
            postJson["eventTime"] = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            headers = {'content-type':'application/json'}
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
        if(postJson["eventCode"] == None):
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
            NewarkPost(step)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])