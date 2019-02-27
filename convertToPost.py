import os
import sys
import json
import copy
import requests
import datetime
import mysql.connector

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

def getSize(size):
    if(size.find("20")):
        return 20
    if(size.find("40")):
        return 40
    if(size.find("53")):
        return 53

def Seattle46Post(terminal, container, postJson, eventCode, eventName):
    postJson["eventName"] = eventName
    postJson["eventCode"] = eventCode
    postJson["signedBy"] = "Gandalf"
    postJson["reportSource"] = "OceanEvent"
    postJson["resolvedEventSource"] = "Seattle T46 RPA"
    #TODO: get work order somehow; hard-coding for now ¯\_(ツ)_/¯
    if(container == 'TRLU9069474'):
        postJson["workOrderNumber"] = "SHI94436109"
    elif(container == 'MSKU0623840'):
        postJson["workOrderNumber"] = "SHI92139404"
    #TODO: get shipment reference number?
    #postJson["shipmentReferenceNumber"] = "ShipRef24336522600"
    postJson["city"] = "Seattle" #mandatory
    postJson["country"] = "US" #mandatory
    postJson["state"] = "WA"
    postJson["location"] = "401 Alaskan Way, Seattle, WA 98104"
    postJson["latitude"] = 45.60
    postJson["longitude"] = -122.34
    #TODO: config file for different databases
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)


def Seattle46(terminal, container):
    with open(r"c:\\Users\\pvanausdeln\\Dropbox (Blume Global)\\Documents\\UiPath\\PortTerminalScraping"+"\\"+terminal+"\\"+container+".json") as jsonData:
        data = json.load(jsonData)
    print(container)
    print(json.dumps(data))
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    postJson["unitId"] = data["Container Number"]
    postJson["vessel"] = data["Vessel"] #mandatory
    postJson["voyageNumber"] = data["Voyage"] #mandatory
    postJson["resolvedEventStatus"] = data["Trouble Transaction"]
    postJson["eventTime"] = data["Appt Time"].split("~")[0]+":00" if (data["Appt Time"].find("~") == 0) else datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    postJson["unitSize"] = getSize(data["Container Type/Length/Height"])
    postJson["reasonName"] = data["Miscellaneous Hold Reason"]
    if(data["Available for Pickup"].find("Yes") == 0):
        Seattle46Post(terminal, container, postJson, "AV", "Available For Pickup")
    if(data["Yard Location"].find("Out-Gated") == 0):
        postJson["eventTime"] = datetime.datetime.strptime(data["Yard Location"].split('(')[1].split(')')[0] + ":00", '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y %H:%M:%S')
        Seattle46Post(terminal, container, postJson, "OA", "Outgate")
    #elif(data["Yard Location"].find("On Ship")):
        #Seattle46Post(terminal, container, postJson, "IT", "In Transit")
    elif(data["Yard Location"].find("Delivered") and data["Appt Time"].find("~") == 0):
        Seattle46Post(terminal, container, postJson, "AFD", "Arrived For Delivery")
    if(data["Hold Reason"].find("Released") == 0):
        print(data["Hold Reason"])
        Seattle46Post(terminal, container, postJson, "CH", "Customs Hold")
    if(data["Customs Status"].find("Released") == 0):
        print(data["Customs Status"])
        Seattle46Post(terminal, container, postJson, "CT", "Customs Release")
    if(data["Freight Status"].find("Released") == 0):
        print(data["Freight Status"])
        Seattle46Post(terminal, container, postJson, "FS", "Freight Release")
    if(data["Carrier Status"].find("Released") == 0):
        print(data["Carrier Status"])
        Seattle46Post(terminal, container, postJson, "CR", "Carrier Release")




def main(terminal, container):
    if(terminal == "SeattleTerminal46"):
        Seattle46(terminal, container)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

#if yard location is on ship
#something with onship/in transit (IT)
#if yard location is delivered
#event type = delivered (AF)
#if no appointment time -> no pickup event