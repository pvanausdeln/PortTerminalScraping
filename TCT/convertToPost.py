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

def TCTStep(event):
    if(event.find("PTTGateOut") != -1):
        return("OA","OUTGATE", datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    elif(event.find("Delivered") != -1):
        return("A","ARRIVED", datetime.datetime.strptime(event.splitlines()[-1],"%m/%d/%Y %H:%M %p").strftime('%m-%d-%Y %H:%M:%S'))
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

def TCTPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
        postJson = copy.deepcopy(baseInfo.shipmentEventBase)

        postJson["resolvedEventSource"] = "TCT LA RPA"
        postJson["codeType"] = "UNLOCODE"
        postJson["location"] = "710 Port of Tacoma Rd, Tacoma, WA 98421"
        postJson["city"] = "Tacoma"
        postJson["state"] = "WA"
        postJson["country"] = "US"
        postJson["latitude"] = 47.27
        postJson["longitude"] = -122.41
        postJson["vessel"] = data["Vessel"]
        postJson["voyageNumber"] = data["Voyage"]
        postJson["billOfLadingNumber"] = data["BOLNumber"]
        postJson["workOrderNumber"] = data["WONumber"]
        postJson["reportSource"] = "OceanEvent"

        postJson["unitId"] = data["Container"].replace("-","")
        postJson["carrierName"] = data["SSCO"]
        postJson["unitTypeCode"] = data["Type"]
        postJson["unitSize"] = data["Length"].replace("'", "")
        postJson["eventCode"], postJson["eventName"], postJson["eventTime"] = TCTStep(data["Current State"])
        if(postJson["eventCode"] != None):
            headers = {'content-type':'application/json'}
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
            print(json.dumps(postJson))




def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        fileList = glob.glob(r""+path+"ContainerInformation\\"+container+".json", recursive = True) #get all the json steps
        if (not fileList):
            continue
        fileList = [f for f in fileList if containerList in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            TCTPost(step)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])