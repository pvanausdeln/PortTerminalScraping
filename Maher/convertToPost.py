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

        postJson["unitId"] = data["Container"]
        postJson["carrierName"]=data["Carrier Name"]
        postJson["sealNumber"]= data["Seal Number"]
        postJson["unitSize"]= data["Unit Size"]
        #The following will be stored if no out activity occurs and if a trucker event the receiver name is added
        if("InVessel Activity" in data):
            postJson["eventName"]= "Vessel Arrival"
            postJson["eventTime"]= datetime.datetime.strptime(data["InVessel Activity"], '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]="VA"
        elif("InTruck Activity" in data):
            postJson["eventName"]= "Vessel Arrival"
            postJson["eventTime"] =datetime.datetime.strptime(data["InTruck Activity"], '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]="VA"
            postJson["receiverName"]= data["Trucker"]
        #The above event will be overwritten as out Activities happen the latest and if a trucker event then receiver name is added
        if("OutVessel Activity" in data):
            postJson["eventName"]= "Vessel Departure"
            postJson["eventTime"]=datetime.datetime.strptime(data["OutVessel Activity"], '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]= "VD"
        elif("OutTruck Activity" in data):
            postJson["eventName"]= "Vessel Departure"
            postJson["eventTime"]=datetime.datetime.strptime(data["OutTruck Activity"], '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]= "VD"
            postJson["receiverName"]= data["Trucker"]
        
        
        headers = {'content-type':'application/json'}
        r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
        print(r)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        fileList = glob.glob(r""+path+"\\ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
        if (not fileList):
            continue
        MaherPost(fileList[0])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])