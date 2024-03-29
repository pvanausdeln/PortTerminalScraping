import sys
import os
import requests
import json
import copy
import datetime
import glob
import string

class baseInfo:
    postURL = "https://test-apps.blumesolutions.com/shipmentservice-api/v1/bv/shipmentevents"

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

def MaherPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)

        postJson["reportSource"] = "OceanEvent"
        postJson["resolvedEventSource"] = "Maher RPA"
        postJson["codeType"] = "UNLOCODE"
        postJson["workOrderNumber"] = data["WONumber"]
        postJson["billOfLadingNumber"] = data["BOLNumber"]
        postJson["vessel"] = data["Vessel"]
        postJson["voyageNumber"] = data["Voyage"]

        postJson["longitude"] = -74.13
        postJson["latitude"] = 40.66
        postJson["location"] = "1210 Corbin St, Elizabeth, NJ 07201"
        postJson["country"] = "US"
        postJson["state"] = "NJ"
        postJson["city"] = "Elizabeth"

        postJson["unitId"] = data["Container"]
        postJson["carrierName"]=data["Carrier Name"]
        postJson["sealNumber"]= data["Seal Number"]
        postJson["unitSize"]= data["Unit Size"][0:2]

        headers = {'content-type':'application/json'}
        if(data.get("Event") is None):
            return
        #The following will be stored if no out activity occurs and if a trucker event the receiver name is added
        if(data["Event"]=="InVessel Activity"  and data["Event_Time"] != ""):
            postJson["eventName"]= "Vessel Arrival"
            postJson["eventTime"]= datetime.datetime.strptime(data["Event_Time"], '%Y-%m-%d %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]="VA"
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
            print(json.dumps(postJson))
        elif(data["Event"]=="InTruck Activity" and data["Event_Time"] != ""):
            postJson["eventName"]= "Vessel Arrival"
            postJson["eventTime"] = datetime.datetime.strptime(data["Event_Time"], '%Y-%m-%d %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]="VA"
            postJson["receiverName"]= data["ReceiverName"]
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
            print(json.dumps(postJson))
        #The above event will be overwritten as out Activities happen the latest and if a trucker event then receiver name is added
        if(data["Event"]=="OutVessel Activity" and data["Event_Time"] != ""):
            postJson["eventName"]= "Vessel Departure"
            postJson["eventTime"]= datetime.datetime.strptime(data["Event_Time"], '%Y-%m-%d %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]= "VD"
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
            print(json.dumps(postJson))
        elif(data["Event"]=="OutTruck Activity"  and data["Event_Time"] != ""):
            postJson["eventName"]= "Vessel Departure"
            postJson["eventTime"]= datetime.datetime.strptime(data["Event_Time"], '%Y-%m-%d %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]= "VD"
            postJson["receiverName"]= data["ReceiverName"]
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
            print(json.dumps(postJson))
        elif(data["Event"]=="OutRail Activity"  and data["Event_Time"] != ""):
            postJson["eventName"]= "Vessel Departure"
            postJson["eventTime"]= datetime.datetime.strptime(data["Event_Time"], '%Y-%m-%d %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
            postJson["eventCode"]= "VD"
            postJson["receiverName"]= data["ReceiverName"]
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
            print(json.dumps(postJson))

def testMain(container):
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\" #just to add escape sequences for the glob method to work fine
    fileList = glob.glob(path + "ContainerInformation\\"+container+"Step*.json", recursive = True) #get all the json steps
    if (not fileList):
        return
    fileList = [f for f in fileList if container in f] #set of steps for this number
    fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
    for step in fileList:
        MaherPost(step)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\" #just to add escape sequences for the glob method to work fine
    for container in containerList:
        fileList = glob.glob(path + "ContainerInformation\\"+container+"Step*.json", recursive = True) #get all the json steps

        if (not fileList):
            continue
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            MaherPost(step)

if __name__ == "__main__":
    testMain(sys.argv[1])
    #main(sys.argv[1], sys.argv[2])
