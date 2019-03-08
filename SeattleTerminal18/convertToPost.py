import sys
import os
import requests
import json
import copy
import datetime

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

def getEvent(data, postJson):
    if(data["Event"] == "LOAD"):
        postJson["eventCode"] = "AE"
        postJson["eventName"] = "Loaded on Vessel"
    elif(data["Event"] == "UNLOAD"):
        postJson["eventCode"] = "UV"
        postJson["eventName"] = "Unloaded on Vessel"
    elif(data["Event"] == "FULL IN" or data["Event"] == "EMPTY IN"):
        postJson["eventCode"] = "I"
        postJson["eventName"] = "INGATE"
    elif(data["Event"] == "FULL OUT"):
        postJson["eventCode"] = "OA"
        postJson["eventNAme"] = "OUTGATE"
    elif(data["Event"] == "EMPTY OUT"):
        postJson["eventCode"] = "EE"
        postJson["eventCode"] = "Empty Equipment Dispatched"
    return postJson

def Seattle18Post(container):
    if(os.path.isfile(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\SeattleTerminal18\\ContainerInformation\\"+container+"Vessel.json") == False): #is there a Vessel event
        return

    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    with open(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\SeattleTerminal18\\ContainerInformation\\"+container+"Vessel.json") as jsonData:
        data = json.load(jsonData)
    if(data["Event"] == ""):
        return
    postJson["unitId"] = container
    postJson["vessel"] = data["Vessel"]
    postJson["voyageNumber"] = data["Voyage"]
    postJson["workOrderNumber"] = data["WONumber"]
    postJson["shipmentReferenceNumber"] = data["ReferenceNumber"]
    postJson["billOfLadingNumber"] = data["BOLNumber"]
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "Seattle T18 RPA"
    postJson["city"] = "Seattle" #mandatory
    postJson["country"] = "US" #mandatory
    postJson["state"] = "WA"
    postJson["location"] = "1050 SW Spokane St, Seattle, WA 98134"
    postJson["latitude"] = 47.57
    postJson["longitude"] = -122.34
    postJson["terminalCode"] = "Seattle Terminal 18"
    postJson["unitState"] = data["Status"]
    postJson["unitSize"] = data["Size"].split("'")[0]
    postJson["unitTypeCode"] = data["Type Code"].replace('(', '').replace(')', '')

    loadPostJson = None
    loadData = None
    if(os.path.isfile(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\SeattleTerminal18\\ContainerInformation\\"+container+"Load.json") == True): #is there a Load event
        loadPostJson = copy.deepcopy(postJson)
        with open(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping\\SeattleTerminal18\\ContainerInformation\\"+container+"Load.json") as loadJsonData:
            loadData = json.load(loadJsonData)

    postJson["eventTime"] = datetime.datetime.strptime(data["Time"][:-3] + ":00", '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
    postJson = getEvent(data, postJson)
    print(json.dumps(postJson))
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)

    if(loadPostJson != None):
        loadPostJson["eventTime"] = datetime.datetime.strptime(loadData["Time"][:-3] + ":00", '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
        loadPostJson = getEvent(loadData, loadPostJson)
        headers = {'content-type':'application/json'}
        r = requests.post(baseInfo.postURL, data = json.dumps(loadPostJson), headers = headers, verify = False)
        print(r)

def main(containerList):
    for container in containerList:
        Seattle18Post(container)

if __name__ == "__main__":
    main(sys.argv[1])