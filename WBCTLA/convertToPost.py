import os
import sys
import json
import copy
import requests
import datetime
import glob

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

def WBCTStep(event):
    if(event.find("PTTGateOut") != -1):
        return("OA","OUTGATE", datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    elif(event.find("Delivered") != -1):
        return("A","ARRIVED", datetime.datetime.strptime(event.splitlines()[1],"%m/%d/%Y %H:%M %p").strftime('%m-%d-%Y %H:%M:%S'))
    elif(event.find("Schedule Appointment") != -1):
        return("RN","Pickup Appointment", datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    elif(event.find("In Yard") != -1):
        return("IY","IN YARD", datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    elif(event.find("Manifested") != -1):
        return("MET","Manifest Event Hold", datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    elif(event.find("Assigned To Trucker") != -1):
        return("OA","OUTGATE", datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    elif(event.find("On Ship") != -1):
        return("IT","In Transit (Ocean)", datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    return (None, None, None)

def WBCTPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)

        postJson["resolvedEventSource"] = "WBCT LA RPA"
        postJson["location"] = "2050 John S Gibson Blvd, San Pedro, CA 90731"
        postJson["city"] = "San Pedro"
        postJson["state"] = "CA"
        postJson["country"] = "US"
        postJson["latitude"] = 33.73
        postJson["longitude"] = -118.33
        postJson["vessel"] = data["Vessel"]
        postJson["voyageNumber"] = data["Voyage"]
        postJson["billOfLadingNumber"] = data["BOLNumber"]
        postJson["workOrderNumber"] = data["WONumber"]
        postJson["reportSource"] = "OceanEvent"

        postJson["unitId"] = data["Container"].replace("-","")
        postJson["carrierName"] = data["SSCO"]
        postJson["unitTypeCode"] = data["Type"]
        postJson["unitSize"] = data["Length"].replace("'", "")
        postJson["eventCode"], postJson["eventName"], postJson["eventTime"] = WBCTStep(data["Current State"])
        if(postJson["eventCode"] != None):
            headers = {'content-type':'application/json'}
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
            print(json.dumps(postJson))




def main(containerList):
    for container in containerList:
        fileList = glob.glob(r"C:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\WBCTLA\\ContainerInformation\\"+container+".json", recursive = True) #get all the json steps
        if (not fileList):
            continue
        fileList = [f for f in fileList if containerList in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            WBCTPost(step)

if __name__=="__main__":
    main(sys.argv[1])