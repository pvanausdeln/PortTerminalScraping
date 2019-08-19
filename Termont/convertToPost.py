import os
import sys
import json
import copy
import requests
import datetime
import glob
import csv

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

def outEvents(reader, postJson):
    if(reader[2][20] == "VESSEL"):
        postJson["eventCode"], postJson["eventName"] = ("VD", "Vessel Departure")
    elif(reader[2][20] == "TRUCK"):
        postJson["eventCode"], postJson["eventName"] = ("OA", "OUTGATE")
    if(postJson["eventCode"] is not None):
        print(postJson["eventCode"])
        postJson["eventTime"] = datetime.datetime.strptime(reader[2][22] + " " + reader[2][23], '%Y/%m/%d %H:%M').strftime('%m-%d-%Y %H:%M:%S')
        r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = {'content-type':'application/json'}, verify = False)
        print(r)
        print(json.dumps(postJson))

def inEvents(reader, postJson):
    if(reader[1][20] == "VESSEL"):
        postJson["eventCode"], postJson["eventName"] = ("VA", "Vessel Arrival")
    elif(reader[1][20] == "TRUCK"):
        postJson["eventCode"], postJson["eventName"] = ("I", "INGATE")
    if(postJson["eventCode"] is not None):
        postJson["eventTime"] = datetime.datetime.strptime(reader[1][22] + " " + reader[1][23], '%Y/%m/%d %H:%M').strftime('%m-%d-%Y %H:%M:%S')
        r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = {'content-type':'application/json'}, verify = False)
        print(r)
        print(json.dumps(postJson))


def checkOtherNums(reader):
    WO, BOL, SRN = (None, None, None)
    for i in range(24, 27):
        if(reader[1][i] == "WorkOrder"):
            WO = reader[2][i]
        elif(reader[1][i] == "BOLNumber"):
            BOL = reader[2][i]
        elif(reader[1][i] == "ReferenceNumbers"):
            SRN = reader[2][i]
    return (WO, BOL, SRN)

def TermontPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".csv")):
        with open(path+"ContainerInformation\\"+container+".csv") as containerInfo:
            reader = list(csv.reader(containerInfo)) #get rows of csv (2nd row has all the information)
            postJson = copy.deepcopy(baseInfo.shipmentEventBase)

            postJson["resolvedEventSource"] = "Termont RPA"
            postJson["codeType"] = "UNLOCODE"
            postJson["location"] = "Montreal, QC H1N 3K9, Canada"
            postJson["city"] = "Montreal"
            postJson["state"] = "QC"
            postJson["country"] = "CA"
            postJson["latitude"] = 45.58
            postJson["longitude"] = -73.51
            postJson["unitId"] = container
            postJson["vessel"] = reader[2][8]
            postJson["voyageNumber"] = reader[2][9]
            postJson["billOfLadingNumber"], postJson["workOrderNumber"], postJson["shipmentReferenceNumber"] = checkOtherNums(reader)
            postJson["reportSource"] = "OceanEvent"
            postJson["unitSize"] = reader[2][2]
            postJson["unitTypeCode"] = reader[2][3]
            postJson["carrierCode"] = reader[2][1]
            postJson["carrierName"] = reader[2][21]
            postJson["destinationCity"] = reader[2][12]
            inEvents(reader, postJson)
            postJson["eventCode"], postJson["eventName"] = (None, None)
            outEvents(reader, postJson)


def testMain(container):
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    TermontPost(container, path)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        fileList = glob.glob(r""+path+"ContainerInformation\\"+container+'.csv', recursive = True) #get all the json steps
        if (not fileList):
            continue
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            TermontPost(step, path)

if __name__=="__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])