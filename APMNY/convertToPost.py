import os
import sys
import json
import copy
import requests
import datetime
import glob
import csv
import string

class baseInfo:
    postURL = "https://demo-apps.blumesolutions.com/shipmentservice-api/v1/bv/shipmentevents"

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

def APMLAEventTranslate(postJson, eventText): #why doesn't python have case switch honestly
    if(eventText.find("Unit exited facility via vessel") != -1):
        postJson["eventCode"] = "VD"
        postJson["eventName"] = "Vessel Departure"
    elif(eventText.find("Unit loaded onto a vessel") != -1):
        postJson["eventCode"] = "AE"
        postJson["eventName"] = "Loaded on Vessel"
    elif(eventText.find("Unit received from a truck") != -1):
        postJson["eventCode"] = "R"
        postJson["eventName"] = "Received from Prior Carrier"
    elif(eventText.find("Unit entered facility via gate") != -1):
        postJson["eventCode"] = "I"
        postJson["eventName"] = "INGATE"
    elif(eventText.find("Dismount") != -1):
        postJson["eventCode"] = "CC"
        postJson["eventName"] = "Chassis Untie"
    elif(eventText.find("Mount") != -1):
        postJson["eventCode"] = "CB"
        postJson["eventName"] = "Chassis Tie"
    elif(eventText.find("Unit exited facility via gate") != -1):
        postJson["eventCode"] = "OA"
        postJson["eventName"] = "OUTGATE"
    elif(eventText.find("Unit discharged from a vessel") != -1):
        postJson["eventCode"] = "UV"
        postJson["eventName"] = "Unloaded from Vessel"
    elif(eventText.find("Unit entered facility via vessel") != -1):
        postJson["eventCode"] = "VA"
        postJson["eventName"] = "Vessel Arrival"
    elif(eventText.find("Unit position updated") != -1):
        postJson["eventCode"] = "E"
        postJson["eventName"] = "Estimate to arrive at location"
    elif(eventText.find("Unit moved in the yard") != -1):
        postJson["eventCode"] = "IY"
        postJson["eventName"] = "In Yard"
    else:
        return
    print(json.dumps(postJson))
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)
    return

def APMLAEventRead(container, postJson, path):
    with open(r""+path+"ContainerInformation\\"+container+".csv") as csvData:
        csv_reader = csv.reader(csvData, delimiter=',')
        for row in csv_reader:
            if(row[0].find("Performed") != -1): #skip title row
                continue
            postJson["eventTime"] = ''.join(x for x in row[0] if x in string.printable)
            postJson["eventTime"] = datetime.datetime.strptime(postJson["eventTime"], '%m/%d/%Y %H:%M').strftime('%m-%d-%Y %H:%M:%S')
            APMLAEventTranslate(postJson, row[1])

def APMLAPost(container, path):
    if(os.path.isfile(r""+path+"ContainerInformation\\"+container+".json") == False): #is there a legitimate event
        return
    if(os.path.isfile(r""+path+"ContainerInformation\\"+container+".csv") == False):
        return
    with open(r""+path+"ContainerInformation\\"+container+".json") as jsonData:
        data = json.load(jsonData)

    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    postJson["unitId"] = data["Container ID"]
    postJson["billOfLadingNumber"] = data["Bill Of Lading"]
    postJson["unitSize"] = data["Size/Type/Height"].split("/")[0]
    postJson["unitType"] = data["Size/Type/Height"].split("/")[1]

    postJson["location"] = "5080 McLester Street, Elizabeth, NJ 07207"
    postJson["city"] = "Elizabeth"
    postJson["state"] = "NJ"
    postJson["country"] = "US"
    postJson["latitude"] = 40.66
    postJson["longitude"] = -74.15

    postJson["resolvedEventSource"] = "APM NY RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["reportSource"] = "OceanEvent"
    postJson["shipmentReferenceNumber"] = data["ReferenceNumber"]
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]

    APMLAEventRead(container, postJson, path)
    return

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        APMLAPost(container, path)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
