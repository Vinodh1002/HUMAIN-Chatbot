# importing Packages
from flask import Flask
from flask import request
from flask import make_response
import json
import requests

# flask set up
app = Flask(__name__)

# handling the webhook request
@app.route('/webhook', methods=["GET","POST"])

def webhook():
    # getting the request from dialogflow
    req=request.get_json(silent=True, force=True)
    # getting the intent name
    intent_name = req["queryResult"]["intent"]["displayName"]
    print(intent_name)
    # handling the intents
    if(intent_name == "TrainInformation"):
        return traininformation(req)
    elif (intent_name == "CodeToName"):
        return codetoname(req)
    elif (intent_name == "Location"):
        return location(req)
    elif (intent_name == "PNRNumber"):
        return pnrnumber(req)
    elif (intent_name == "StationSearchCode"):
        return stationsearchcode(req)
    elif (intent_name == "NameToCode"):
        return nametocode(req)
    elif (intent_name == "FogAffectedTrain"):
        return fogaffectedtrain(req)
    elif (intent_name == "LiveTrainStatus"):
        return livetrainstatus(req)
    elif (intent_name == "StationSearchName"):
        return stationsearchname(req)
    return {}

# this function is for train information
def traininformation(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]
    
    # getting the train number from the request
    num = int(data["queryResult"]["parameters"]["trainnumber"])
    
    # base url for train information
    url = "http://indianrailapi.com/api/v2/TrainInformation/apikey/78019cd30144e844e5602a55a58f08c5/TrainNumber/" + str(num) + "/"
    
    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    train_name = obj["TrainName"]
    source_stationcode = obj["Source"]["Code"]
    source_time = obj["Source"]["Arrival"]
    dest_stationcode = obj["Destination"]["Code"]
    dest_time = obj["Destination"]["Arrival"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse1(train_name, source_stationcode, source_time, dest_stationcode, dest_time)
    return {}

# this function is for sending train information to dialogflow
def MakeTextResponse1(train_name, source_stationcode, source_time, dest_stationcode, dest_time):
    return {
        "fulfillmentText": "Train Name: " + train_name + "\nSource Station Code: " + source_stationcode + "\nSource Time: " + source_time + "\nDestinaton Station Code: " + dest_stationcode + "\nDestination Timr: " + dest_time
    }


# this function is for station name
def codetoname(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # getting the station code from the request
    station_code = data["queryResult"]["parameters"]["stationcode"]

    # base url for station name
    url="http://indianrailapi.com/api/v2/StationCodeToName/apikey/78019cd30144e844e5602a55a58f08c5/StationCode/" + station_code + "/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    station_name_en = obj["Station"]["NameEn"]
    station_name_hn = obj["Station"]["NameHn"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse2(station_name_en, station_name_hn)
    return {}

# this function is for sending station name to dialogflow
def MakeTextResponse2(station_name_en, station_name_hn):
    return {
        "fulfillmentText": "Station Name in English: " + station_name_en + "\nStation name in Hindi: " + station_name_hn
    }


# this function is for station location(map url)
def location(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # getting the station code from the request
    station_code = data["queryResult"]["parameters"]["stationcode"]

    # base url for station location
    url="http://indianrailapi.com/api/v2/StationLocationOnMap/apikey/78019cd30144e844e5602a55a58f08c5/StationCode/" + station_code + "/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    station_code = obj["StationCode"]
    station_name = obj["StationName"]
    map_url = obj["URL"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse3(station_code, station_name, map_url)
    return {}

# this function is for sending map url to dialogflow
def MakeTextResponse3(station_code, station_name, map_url):
    return {
        "fulfillmentText": "Station Code: " + station_code + "\nStation Name: " + station_name + "\nMap URL: " + map_url
    }


# this function is for train details
def pnrnumber(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # getting the pnr number from the request
    pnr_number = data["queryResult"]["parameters"]["pnr"]

    # base url for train details
    url="http://indianrailapi.com/api/v2/PNRCheck/apikey/78019cd30144e844e5602a55a58f08c5/PNRNumber/" + pnr_number + "/Route/1/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    pnr_number = obj["PnrNumber"]
    train_no = obj["TrainNumber"]
    train_name = obj["TrainName"]
    journey_class =  obj["JourneyClass"]
    fron = obj["From"]
    to = obj["To"]
    joureny_date = obj["JourneyDate"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse4(pnr_number, train_no, train_name, journey_class, fron, to, joureny_date)
    return {}

# this function is for sending train details to dialogflow
def MakeTextResponse4(pnr_number, train_no, train_name, journey_class, fron, to, joureny_date):
    return {
        "fulfillmentText": "PNR Number: " + pnr_number + "\nTrain No: " + train_no + "\nTrain Name: " + train_name + "\nJourney Class: " + journey_class + "\nFrom: " + fron + " To: " + to + "\nJourney Date: " + joureny_date
    }


# this function is for station location(lat & long)
def stationsearchcode(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # getting the station code from the request
    station_code = data["queryResult"]["parameters"]["stationcode"]

    # base url for station location
    url="http://indianrailapi.com/api/v2/AutoCompleteStation/apikey/78019cd30144e844e5602a55a58f08c5/StationCodeOrName/" + station_code + "/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    nameen = obj["Station"]["NameEn"]
    namehn = obj["Station"]["NameHn"]
    station_code = obj["Station"]["StationCode"]
    longi = obj["Station"]["Longitude"]
    lat = obj["Station"]["Latitude"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse5(nameen, namehn, station_code, longi, lat)
    return {}

# this function is for sending station location to dialogflow
def MakeTextResponse5(nameen, namehn, station_code, longi, lat):
    return {
        "fulfillmentText": "NameEn: " + nameen + "\nNameHn: " + namehn + "\nSation code: " + station_code + "\nLongitude: " + longi + "\nLatitude: " + lat
    }


# this function is for station code
def nametocode(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # getting the station name from the request
    station_name = data["queryResult"]["parameters"]["stationname"]

    # base url for train code
    url="http://indianrailapi.com/api/v2/StationNameToCode/apikey/78019cd30144e844e5602a55a58f08c5/StationName/" + station_name + "/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    station_code = obj["Station"]["StationCode"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse6(station_code)
    return {}

# this function is for sending station code to dialogflow
def MakeTextResponse6(station_code):
    return {
        "fulfillmentText": "Sation code: " + station_code
    }


# this function is for fog affected train
def fogaffectedtrain(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # base url for fog affected train
    url="https://indianrailapi.com/api/v2/FogAffectedTrains/apikey/78019cd30144e844e5602a55a58f08c5/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    train_no = obj["Trains"]["TrainNo"]
    train_name = obj["Trains"]["TrainName"]
    last_station = obj["Trains"]["LastStation"]
    status = obj["Trains"]["Status"]
    expected_arrival = obj["Trains"]["ExpectedArrival"]
    last_update =  obj["LastUpdate"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse7(train_no, train_name, last_station, status, expected_arrival, last_update)
    return {}

# this function is for sending fog affected train to dialogflow
def MakeTextResponse7(train_no, train_name, last_station, status, expected_arrival, last_update):
    return {
        "fulfillmentText": "Train No: " + train_no + "\nTrain Name: " + train_name + "\nLast Station: " + last_station + "\nStatus: " + status + "\nExpected Arrival: " + expected_arrival + "\nLast Update:" + last_update
    }


# this function is for live status of the train
def livetrainstatus(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # getting the station code from the request
    station_code = data["queryResult"]["parameters"]["stationcode"]

    # base url for live status of the train
    url="http://indianrailapi.com/api/v2/livetrainstatus/apikey/78019cd30144e844e5602a55a58f08c5/trainnumber/" + station_code + "/date/20190930/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    start_date = obj["StartDate"]
    train_no = obj["TrainNumber"]
    current_station = obj["CurrentStation"]["StationName"]
    station_code = obj["CurrentStation"]["StationCode"]
    
    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse8(start_date, train_no, current_station, station_code)
    return {}

    for x in obj["TrainRoute"]:
        station_name = x["StationName"]
        stations_code = x["StationCode"]
        return MakeTextResponse(station_name, stations_code)
    

# this function is for sending live train status to dialogflow
def MakeTextResponse(station_name, stations_code):
    return {
        "fulfillmentText": "\nStation Name: " + station_name + "\nStation Code: " + stations_code
    }

def MakeTextResponse8(start_date, train_no, current_station, station_code):
        return {
            "fulfillmentText": "Start Date: " + start_date + "\nTrain No: " + train_no + "\nCurrent Station: " + current_station + "\nStation Code: " + station_code
        }


# this function is for station location
def stationsearchname(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]

    # getting the station name from the request
    station_name = data["queryResult"]["parameters"]["stationname"]

    # base url for station location
    url="http://indianrailapi.com/api/v2/AutoCompleteStation/apikey/78019cd30144e844e5602a55a58f08c5/StationCodeOrName/" + station_name + "/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(url).json()

    # getting the data from the response
    nameen = obj["Station"]["NameEn"]
    namehn = obj["Station"]["NameHn"]
    station_code = obj["Station"]["StationCode"]
    longi = obj["Station"]["Longitude"]
    lat = obj["Station"]["Latitude"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse9(nameen, namehn, station_code, longi, lat)
    return {}

# this function is for sending station location to dialogflow
def MakeTextResponse9(nameen, namehn, station_code, long, lat):
    return {
        "fulfillmentText": "NameEn: " + nameen + "\nNameHn: " + namehn + "\nSation code: " + station_code + "\nLongitude: " + long + "\nLatitude: " + lat
    }


if __name__ == '__main__':
    app.run(port=3000, debug=True)
