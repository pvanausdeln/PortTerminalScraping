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

def getEvent(event):
    if(event.find("UNIT_RESERVE") != -1):
        return("RC", "Reserve Container Against Booking")
    elif(event.find("UNIT_OUT_VESSEL") != -1):
        return("VD", "Vessel Departure")
    elif(event.find("UNIT_DISMOUNT") != -1):
        return("CC", "Chassis Un-Tie")
    elif(event.find("UNIT_LOAD") != -1):
        return("AE", "Loaded on Vessel")
    elif(event.find("UNIT_MOUNT") != -1):
	    return("CB", "Chassis Tie")
    elif(event.find("UNIT_REROUTE") != -1):
	    return("AI", "Shipment has been reconsigned")
    elif(event.find("UNIT_DELIVER") != -1):
        return("OFD", "Out for Delivery")
    elif(event.find("UNIT_IN_GATE") != -1):
	    return("I", "In-Gate")
    elif(event.find("UNIT_OUT_GATE") != -1):
	    return("OA", "Out-Gate")
    elif(event.find("UNIT_RECEIVE") != -1):
        return("R", "RECEIVED")
    elif(event.find("UNIT_YARD_MOVE") != -1):
	    return("TM", "Intra-Terminal Movement")
    elif(event.find("UNIT_DISCH") != -1):
	    return("UV", "Unloaded from Vessel")
    print("failed: " + event)
    return(None, None)

def BayportPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)

    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "BAYPORT RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]


    postJson["longitude"] = -95.01
    postJson["latitude"] = 29.61
    postJson["location"] = "12619 Port Rd, Seabrook, TX 77586"
    postJson["country"] = "US"
    postJson["state"] = "TX"
    postJson["city"] = "Houston"
    postJson["eventTime"] = datetime.datetime.strptime(data["datetime"][:-3], '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
    postJson["unitId"] = data["Container"]
    postJson["notes"]=data["Notes"]
    postJson["unitTypeCode"]=data["Unit Code"]
    postJson["receiverCode"]=data["Receiver Code"]
    postJson["carrierName"]=data["Carrier"]
    postJson["sealNumber"]=data["Seal Number"]
    postJson["unitSize"] = data["SizeTypeHeight"][0:2]
    postJson["unitType"] = data["SizeTypeHeight"][5:7]
    postJson["eventCode"], postJson["eventName"] = getEvent(data["Event"])
        #we only need this line of code if the datetime has unprintable characters
    #postJson["eventTime"] = ''.join(x for x in data["datetime"] if x in string.printable)
    if(postJson["eventCode"] is None):
        return
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)

def testMain(container):
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    fileList = glob.glob(r""+path+"ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
    if(not fileList):
        return
    fileList = [f for f in fileList if container in f] #set of steps for this number
    fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
    for step in fileList:
        BayportPost(step)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        fileList = glob.glob(r""+path+"ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
        if(not fileList):
            continue
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            BayportPost(step)

if __name__ == "__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
