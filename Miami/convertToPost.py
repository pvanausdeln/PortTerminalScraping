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
    if(data_event.find("LOAD") != -1):
        return("Loaded on Truck", "AM")
    elif(data_event.find("EMPTY IN") != -1):
        return("In-Gate", "I")
    elif(data_event.find("FULL OUT") != -1):
        return("Out-Gate", "OA")
    elif(data_event.find("DISCHARGE") != -1):
        return("Unloaded from Vessel", "UV")
    elif(data_event.find("DAMAGE") != -1):
        return("Bad Order (Inoperative or Damaged)", "B")
    elif(data_event.find("SEALCHANGE") != -1):
        return("Seals Altered", "SC")
    elif(data_event.find("SEALRECORD") != -1):
        return("Seals Altered", "SC")
    elif(data_event.find("YARD SHIFT") != -1):
        return("Intra-Terminal Movement", "TM")
    elif(data_event.find("RAILUNLOAD") != -1):
        return("Unloaded from a Rail Car", "UR")
    elif(data_event.find("FULL IN") != -1):
        return("In-Gate", "I")
    elif(data_event.find("RAIL LOAD") != -1):
        return("Loaded on Rail", "AL")
    elif(data_event.find("RAIL ARRIVE") != -1):
        return("Rail Arrival at Destination Intermodal Ramp", "AR")
    elif(data_event.find("RAIL DEPART") != -1):
        return("Rail Departure from Origin Intermodal Ramp", "RL")
    return(None, None)
        
def MiamiPost(step):
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    with open(step) as jsonData:
        data = json.load(jsonData)
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "Miami RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["workOrderNumber"] = data.get("WON")
    postJson["billOfLadingNumber"] = data.get("BOL")
    postJson["vessel"] = data.get("Vessel")
    postJson["voyageNumber"] = data.get("Voyage")
    postJson["longitude"] = -80.16
    postJson["latitude"] = 25.77
    postJson["location"] = "2299 Port Blvd, Miami, FL 33132"
    postJson["country"] = "US"
    postJson["state"] = "FL"
    postJson["city"] = "Miami"
    postJson["unitId"]= data.get("Container")
    postJson["location"]=data.get("Location")
    postJson["terminalCode"]=data.get("Terminal")
    postJson["receiverCode"]=data.get("Trucker")
    postJson["carrierCode"]=data.get("Shipping Line")
    postJson["unitSize"]=data.get("Size")
    postJson["unitTypeCode"]=data.get("Type")
    postJson["carrierCode"]=data.get("Operator")
    postJson["notes"]=data.get("Notes")
    postJson["eventTime"]=datetime.datetime.strptime(data.get("Date"), '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
    postJson["eventName"], postJson["eventCode"] = Event(data.get("Event"))
    if(postJson["eventCode"] is None):
        return
    print(json.dumps(postJson))
    #TODO: config file for post urls
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    

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
            MiamiPost(step)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])