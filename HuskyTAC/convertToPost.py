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

def HuskyStep(event):
    if(event.find("LOADRAIL") != -1):
        return("AL", "Loaded on Rail")
    elif(event.find("DISCHARGE") != -1):
        return("UV", "Unloaded from Vessel")
    elif(event.find("RECEIVE") != -1):
        return("CO", "Cargo Received")
    elif(event.find("LOAD") != -1):
        return("AE", "Loaded on Vessel")
    elif(event.find("UNLOAD") != -1):
        return("U", "Unloading")
    elif(event.find("GATEOUT") != -1):
        return("OA", "OUTGATE")
    elif(event.find("GATEIN") != -1):
        return("I", "INGATE")
    elif(event.find("RELEASE") != -1):
        return("CR", "Carrier Release")
    elif(event.find("SHIFT") != -1):
        return("TM", "Intra terminal movement")
    elif(event.find("CARGOEXAM") != -1):
        return("GI", "Terminal Gate Inspection")
    return(None, None)

def HuskyPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)

    postJson["resolvedEventSource"] = "HUSKY TAC RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["location"] = data.get("POL")
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["reportSource"] = "OceanEvent"

    postJson["unitId"] = data["Container"]
    postJson["eventTime"] = datetime.datetime.strptime(data["Date/Time"], '%m/%d/%Y %H:%M').strftime('%m-%d-%Y %H:%M:%S')
    postJson["eventCode"], postJson["eventName"] = HuskyStep(data["Event"])
    postJson["carrierName"] = data["Line"]
    postJson["unitState"] = data["Sts"]
    postJson["unitType"] = data["SzTpHt"][2:4]
    postJson["unitSize"] = data["SzTpHt"][:2]
    postJson["carrierCode"]  = data["Carrier"]
    #postJson["originatorId"]= int(data["POL"])

    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)
    print(json.dumps(postJson))

def testMain(container):
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    fileList = glob.glob(r""+path+"ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
    if (not fileList):
        return
    fileList = [f for f in fileList if container in f] #set of steps for this number
    fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
    fileList.reverse()
    for step in fileList:
        HuskyPost(step)

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
        fileList.reverse() #events in reverse order on site
        for step in fileList:
            HuskyPost(step)

if __name__=="__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
