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
def Event(data_event):
    if(data_event.find("Gate-out") != -1):
        return("OUTGATE", "OA")
    elif(data_event.find("Gate-In") != -1):
        return("INGATE", "I")
    elif(data_event.find("Discharged") != -1):
        return("Unloaded From Vessel", "UV")
    elif(data_event.find("Vessel Load") != -1):
        return("Loaded on Vessel", "AE")
    return(None, None)

def getType(typeDesc):
    if(typeDesc.find("High-cube") != -1):
        return "HC"
    return None
        
def PackerPost(step):
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    with open(step) as jsonData:
        data = json.load(jsonData)
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "Packer RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["workOrderNumber"] = data.get("WON")
    postJson["billOfLadingNumber"] = data.get("BOL")
    postJson["vessel"] = data.get("Vessel")
    postJson["voyageNumber"] = data.get("Voyage")
    postJson["longitude"] = -75.14
    postJson["latitude"] = 39.91
    postJson["location"] = "3301 S Christopher Columbus Blvd, Philadelphia, PA 19148"
    postJson["country"] = "US"
    postJson["state"] = "PA"
    postJson["city"] = "Philadelphia"
    postJson["unitId"]= data.get("Container")
    postJson["location"]=data.get("Location")
    postJson["terminalCode"]=data.get("Terminal")
    postJson["receiverCode"]=data.get("Trucker")
    postJson["carrierCode"]=data.get("Shipping Line")
    postJson["unitSize"]=data.get("Size")
    postJson["unitTypeCode"]=data.get("Type")
    postJson["carrierCode"]=data.get("Operator")
    postJson["notes"]=data.get("Notes")
    postJson["unitState"] = data.get("Description").split(",")[0]
    try:
        postJson["unitTypeCode"] = data.get("Description").split(",")[3] + getType(data.get("Description").split(",")[2])
        postJson["eventName"], postJson["eventCode"] = Event(data.get("Last Move/Datetime").split(",")[0])
    except:
        return
    postJson["unitSize"] = data.get("Description").split(",")[3].strip()
    if(postJson["eventCode"] is None):
        return
    if(postJson["eventCode"].find("AE") != -1):
        postJson["eventTime"] = data.get("Last Move/Datetime").split(",")[1].strip() + " 00:00:00"
    else:
        postJson["eventTime"] = data.get("Last Move/Datetime").split(",")[1].strip() + ":00"
    print(json.dumps(postJson))
    #TODO: config file for post urls
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    

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
            PackerPost(step)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])