import os
import sys
import json
import copy
import requests
import datetime
import glob

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

def EverportPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
    if(data["Move Type"] not in ["Discharge", "Load", "Export In", "Empty In", "Empty Out", "Import"]):
        return
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    if(data["Move Type"] == "Discharge"):
        postJson["eventCode"] = "APL"
        postJson["eventName"] = "Available For Pickup"
    elif(data["Move Type"] == "Load"):
        postJson["eventCode"] = "AE"
        postJson["eventName"] = "Loaded On Vessel"
    elif(data["Move Type"] == "Export In"):
        postJson["eventCode"] = "I"
        postJson["eventName"] = "INGATE"
    elif(data["Move Type"] == "Empty In"):
        postJson["eventCode"] = "I"
        postJson["eventName"] = "INGATE"
    elif(data["Move Type"] == "Empty Out"):
        postJson["eventCode"] = "EE"
        postJson["eventCode"] = "Empty Equipment Dispatched"
    elif(data["Move Type"] == "Import"):
        postJson["eventCode"] = "EE"
        postJson["eventName"] = "Empty Equipment Dispatched"
    
    postJson["eventTime"] = datetime.datetime.strptime(data["Datetime"], '%Y/%m/%d %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
    if(postJson["eventTime"].find(str(datetime.datetime.now().year))) == -1: #it is the current year
        return
    postJson["unitId"] = data["Container"]
    postJson["carrierName"] = data["Trucker"]
    postJson["carrierCode"] = data["Carrier"]
    postJson["sealNumber"] = data["Seal"]
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "EVRPRT OAK RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]
    postJson["longitude"] = -122.33
    postJson["latitude"] = 37.81
    postJson["location"] = "7th St, Oakland, CA 94607"
    postJson["country"] = "US"
    postJson["state"] = "CA"
    postJson["city"] = "Oakland"
    postJson["terminalCode"] = "Everport OAK"
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
        fileList = glob.glob(r""+path+"ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
        if (not fileList):
            continue
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            EverportPost(step)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])