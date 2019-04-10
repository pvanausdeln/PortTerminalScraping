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
    elif(event.find("UNIT_RECEIVE") != -1):
	    return("I", "In-Gate")
    elif(event.find("UNIT_YARD_MOVE") != -1):
	    return("TM", "Intra-Terminal Movement")
    elif(event.find("UNIT_DISCH") != -1):
	    return("UV", "Unloaded from Vessel")
    return(None, None)

def BayportPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        # if(data["Terminal"].find("NCT") == -1):
            # return
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
        
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "BAYPORT RPA"
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]
		

    postJson["longitude"] = -79.96
    postJson["latitude"] = 32.90
    postJson["location"] = "1000 Remount Rd, North Charleston, SC 29406"
    postJson["country"] = "US"
    postJson["state"] = "SC"
    postJson["city"] = "Charleston"
    postJson["eventTime"] = datetime.datetime.strptime(data["datetime"], '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
    postJson["unitId"] = data["Container"]
    postJson["notes"]=data["Notes"]
    postJson["unitTypeCode"]=data["Unit Code"]
    postJson["receiverCode"]=data["Receiver Code"]
    postJson["carrierName"]=data["Carrier"]
    postJson["sealNumber"]=data["Seal Number"]
    postJson["unitSize"] = data["SizeTypeHeight"][0:2]
    postJson["unitType"] = data["SizeTypeHeight"][5:7]
    postJson["eventCode"], postJson["eventName"] = getEvent(data["Event"])
    postJson["eventTime"] = ''.join(x for x in data["Datetime"] if x in string.printable)
    if(postJson["eventCode"] is None):
        return
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)

def main():
    current_dir=os.getcwd()
    fileList = glob.glob(r""+current_dir+"\\ContainerInformation\\BEAU4054276Step0.json", recursive = True) #get all the json steps
    if (not fileList):
        return
    fileList = [f for f in fileList if containerList in f] #set of steps for this number
    fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
    for step in fileList:
        BayportPost(step)

if __name__ == "__main__":
    main(sys.argv[1])