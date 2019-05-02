import os
import sys
import json
import copy
import requests
import datetime

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

def getSize(size):
    if(size.find("20")):
        return 20
    if(size.find("40")):
        return 40
    if(size.find("53")):
        return 53

def TTILongBeachPost(container, postJson, eventCode, eventName):
    postJson["eventName"] = eventName
    postJson["eventCode"] = eventCode
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "TTI LB RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["city"] = "Long Beach" #mandatory
    postJson["country"] = "US" #mandatory
    postJson["state"] = "CA"
    postJson["location"] = "301 Mediterranean Way, Long Beach, CA 90802"
    postJson["latitude"] = 33.76
    postJson["longitude"] = -118.23
    #TODO: config file for different databases
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)


def TTILongBeach(container, path):
    if(os.path.isfile(r""+path+"ContainerInformation\\"+container+".json") == False):
        return
    with open(r""+path+"ContainerInformation\\"+container+".json") as jsonData:
        data = json.load(jsonData)
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    postJson["unitId"] = data["Container Number"]
    postJson["vessel"] = data["Vessel"] #mandatory
    postJson["voyageNumber"] = data["Voyage"] #mandatory
    postJson["resolvedEventStatus"] = data["Trouble Transaction"]
    postJson["eventTime"] = data["Appt Time"].split("~")[0]+":00" if (data["Appt Time"].find("~") != -1) else datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    postJson["unitSize"] = getSize(data["Container Type/Length/Height"])
    postJson["reasonName"] = data["Miscellaneous Hold Reason"]
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["terminalCode"] = "TTI Long Beach"

    if(data["Available for Pickup"].find("Yes") != -1):
        TTILongBeachPost(container, postJson, "AV", "Available For Pickup")
    if(data["Yard Location"].find("Out-Gated") != -1):
        postJson["eventTime"] = datetime.datetime.strptime(data["Yard Location"].split('(')[1].split(')')[0] + ":00", '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
        TTILongBeachPost(container, postJson, "OA", "Outgate")
    elif(data["Yard Location"].find("On Ship")  != -1):
        TTILongBeachPost(container, postJson, "IT", "In Transit (Ocean)")
    elif(data["Yard Location"].find("Delivered") != -1 and data["Appt Time"].find("~") != -1):
        TTILongBeachPost(container, postJson, "AFD", "Arrived For Delivery")
    if(data["Hold Reason"].find("Released") != -1):
        TTILongBeachPost(container, postJson, "CH", "Customs Hold")
    if(data["Customs Status"].find("Released") != -1):
        TTILongBeachPost(container, postJson, "CT", "Customs Release")
    if(data["Freight Status"].find("Released") != -1):
        TTILongBeachPost(container, postJson, "FS", "Freight Release")
    if(data["Carrier Status"].find("Released") != -1):
        TTILongBeachPost(container, postJson, "CR", "Carrier Release")


def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        TTILongBeach(container, path)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
