import os
import sys
import json
import copy
import requests
import datetime
import csv

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

def LBCTStep(event):
    if(event.find("CUSTOMS_DEFAULT_HOLD") != -1):
        return("CT", "Customs Release")
    elif(event.find("FREIGHT_BL_HOLD") != -1):
        return("FS", "Freight Release")
    return (None, None)

def LBCTPost(container):
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    with open(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\LBCT\\ContainerInformation\\"+container+".json") as jsonData:
        data = json.load(jsonData)
    postJson["unitId"] = data["Container"]
    postJson["unitSize"] = data["Size"]
    postJson["unitTypeCode"] = data["Type"]

    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "LBCT RPA"
    postJson["location"] = "201 Pico Ave, Long Beach, CA 90802"
    postJson["city"] = "Long Beach"
    postJson["state"] = "CA"
    postJson["country"] = "US"
    postJson["latitude"] = 33.77
    postJson["longitude"] = -118.21
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]

    with open(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\LBCT\\ContainerInformation\\"+container+".csv") as csvData:
        csv_reader = csv.reader(csvData, delimiter=',')
        holdJson = copy.deepcopy(postJson)
        for row in csv_reader:
            if(row[1] == "APPLIED"):
                continue
            holdJson["eventCode"], holdJson["eventName"] = LBCTStep(row[0])
            if(holdJson["eventCode"] is None):
                continue
            holdJson["eventTime"] = datetime.datetime.strptime(row[1], '%m/%d/%Y %H:%M').strftime('%m-%d-%Y %H:%M') + ":00"
            headers = {'content-type':'application/json'}
            r = requests.post(baseInfo.postURL, data = json.dumps(holdJson), headers = headers, verify = False)
    if(data["Discharged"].find("Actual") == -1):
        return
    elif(data["Available for Pickup"].find("Yes") != -1):
        postJson["eventCode"], postJson["eventName"] = ("APL", "Arrived Pickup Location")
        postJson["eventTime"] = datetime.datetime.strptime(data["Discharged"].rsplit(" ", 1)[0], '%m/%d/%Y %H:%M').strftime('%m-%d-%Y %H:%M') + ":00"
        headers = {'content-type':'application/json'}
        r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    postJson["eventCode"], postJson["eventName"] = ("DI", "Discharged")
    postJson["eventTime"] = datetime.datetime.strptime(data["Discharged"].rsplit(" ", 1)[0], '%m/%d/%Y %H:%M').strftime('%m-%d-%Y %H:%M') + ":00"
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    return




def main(containerList):
    for container in containerList:
        LBCTPost(container)

if __name__=="__main__":
    main(sys.argv[1])