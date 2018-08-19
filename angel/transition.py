# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 19:05:17 2018
    to use this funtion, call "transition()"
@author: onlyjackfrost
"""
import requests
import json
import re
from .ubike import bike
from .weather import weather

# =============================================================================
#       basic method 
# =============================================================================
def Geolocation_request():
    API_key = "AIzaSyBmvshA169XyDvEACKgAgyFbOzbmedBo1k"
    URL = "https://www.googleapis.com/geolocation/v1/geolocate?key="+API_key
#    para={
#      "macAddress": "54:A0:50:6B:86:52"
#    }
    r = requests.post(URL)
    js = json.loads(r.content.decode())
    user_location = (js['location']['lat'],js['location']['lng'])
    return user_location

def direction_request(user_location , destination,transit_mode):
    API_key = "AIzaSyBmvshA169XyDvEACKgAgyFbOzbmedBo1k"
    origin = str(user_location[0])+","+str(user_location[1])
    URL = "https://maps.googleapis.com/maps/api/directions/json?"\
           +"origin="+origin \
           +"&destination="+destination \
           +"&mode=transit" \
           +"&transit_mode="+transit_mode \
           +"&language=zh-TW" \
           +"&key="+API_key
    r = requests.post(URL)
    content = json.loads(r.content.decode())
#    print (json.dumps(content, indent=4, sort_keys=True))
    return content

def cost_parser(detail):
    """
        parse the duration and cost for the transit
    """
    text = "0"
    duration = "不知道多久"
    try:
        text = detail["routes"][0]["fare"]["text"][1:-3]
    except KeyError:
        text = "0"
    try:
        for step in detail["routes"][0]["legs"][0]["steps"]:
            if step["travel_mode"] == "TRANSIT":
                duration =step["duration"]["text"]
    except KeyError:
        duration = "不知道多久"
    finally :
        cost = [text,duration]
    return cost

def bus_detail_parser(bus_detail):
    """
        parse the detail information for the transit
        上車站、下車站、公車代號、該班公車發車間隔時間
    """
    #get route detail
    shortname = []
    town_name_destination = bus_detail["routes"][0]["legs"][0]["end_address"][5:11]
    town_name_destination = re.sub(r'台','臺',town_name_destination)
    for index in range(0,len(bus_detail["routes"][0]["legs"][0]["steps"])):
        step = bus_detail["routes"][0]["legs"][0]["steps"][index]
        try:
            if step["travel_mode"] == "TRANSIT":
                headway = step["transit_details"]["headway"]
                shortname = step["transit_details"]["line"]["short_name"]
                departure_stop = step["transit_details"]["departure_stop"]["name"]
                arrival_stop = step["transit_details"]["arrival_stop"]["name"]
        except KeyError:
            shortname = []
    #write file
    with open("bus_detail.txt",'w')as f:
        if shortname==[]:
            f.write("距離很近，不用搭公車")
        else:
            f.write("請從"+departure_stop+"站，搭"+shortname+"公車到，"+arrival_stop+"站下車")
    return shortname, town_name_destination


def tram_detail_parser(bus_detail):
    """
        parse the detail information for the transit
        上車站、下車站、捷運線
    """
    shortname = []
    #get route detail
    for index in range(0,len(bus_detail["routes"][0]["legs"][0]["steps"])):
        step = bus_detail["routes"][0]["legs"][0]["steps"][index]
        try:
            if step["travel_mode"] == "TRANSIT":
                shortname = step["transit_details"]["line"]["short_name"]
                departure_stop = step["transit_details"]["departure_stop"]["name"]
                arrival_stop = step["transit_details"]["arrival_stop"]["name"]
        except KeyError:
            shortname = []
    #write file
    with open("tram_detail.txt",'w')as f:
        if shortname==[]:
            f.write("距離很近，不用搭捷運")
        else:
            f.write("請從"+departure_stop+"，搭"+shortname+"到，"+arrival_stop+"下車")
    return shortname
  
# =============================================================================
#       transition  method
# =============================================================================
def bus_algorithm(destination):
    user_location = Geolocation_request()
    user_location = (25.022194, 121.535346)  #DEMO用 要刪掉
    transit_mode = "bus"
    #get the user's current location
    user_location = Geolocation_request()
    #get the transit recommandation
    bus_detail = direction_request(user_location,destination,transit_mode)
    #parse for the detail transit information
    bus_shortname , town_name_destination = bus_detail_parser(bus_detail)
    #parse the cost and time 
    cost = cost_parser(bus_detail)
    return cost, bus_detail, bus_shortname, town_name_destination

def tram_algorithm(destination):
    user_location = Geolocation_request()
    user_location = (25.022194, 121.535346)  #DEMO用 要刪掉
    transit_mode = "tram"
    #get the user's current location
    user_location = Geolocation_request()
    #get the transit recommandation
    tram_detail = direction_request(user_location,destination,transit_mode)
    #parse for the detail transit information
    tram_shortname = tram_detail_parser(tram_detail)
    #parse the cost and time 
    cost = cost_parser(tram_detail)
    return cost, tram_detail, tram_shortname

def bike_write_file(start_stop, end_stop):
    with open("bike_detail.txt","w") as f:
        f.write("你可以到"+start_stop+"租共享單車，然後騎到"+end_stop+"還車")
    
def transition(destination):
    bus_cost, bus_detail, bus_shortname, town_name_destination = bus_algorithm(destination)
    tram_cost, tram_detail, tram_shortname = tram_algorithm(destination)
    #ubike 判斷
    start_stop, end_stop = bike(destination)
    if start_stop == end_stop:
        use_bike = 0
    else:
        use_bike = 1
        bike_write_file(start_stop, end_stop)
    #下雨判斷
    dict_avg_rain = weather()
    brocast = dict_avg_rain[town_name_destination]
    
    with open("transition_cost.txt","w") as f:
        condition = [ tram_shortname !=[],  bus_shortname !=[], use_bike]
        print(condition)
        if condition == [False,False,0]:
            f.write("目的地距離很近，你問人然後走路吧"+brocast)
            out = 0
        if condition == [False,False,1]:
            f.write("很抱歉，你只能騎腳踏車到目的地，要騎腳踏車請說腳踏車"+brocast)
            out = 1
        if condition == [False,True,1]:
            f.write("搭公車要"+bus_cost[1]+","+bus_cost[0]+"元"+
                    "你要搭公車、還是騎最環保又健康的腳踏車"+brocast)
            out = 1
        if condition == [False,True,0]:
            f.write("搭公車要"+bus_cost[1]+","+bus_cost[0]+"元"
                    +"要搭公車請說公車兩個字"+brocast)
            out = 1
        if condition == [True,True,0]:
            f.write("搭捷運要"+tram_cost[1]+','+tram_cost[0]+"元"+","
                    "搭公車要"+bus_cost[1]+","+bus_cost[0]+"元"+
                    "你要搭捷運還是公車"+brocast)
            out = 1    
        if condition == [True,False,0]:
            f.write("搭捷運要"+tram_cost[1]+','+tram_cost[0]+"元"+","
                    +"要搭捷運請說捷運兩個字"+brocast)
            out = 1  
        if condition == [True,False,1]:
            f.write("搭捷運要"+tram_cost[1]+','+tram_cost[0]+"元"+","
                    +"你要搭捷運還是騎最環保又健康的腳踏車"+brocast)
            out = 1 
        if condition == [True,True,1]:
            f.write("搭捷運要"+tram_cost[1]+','+tram_cost[0]+"元"+","
                    "搭公車要"+bus_cost[1]+","+bus_cost[0]+"元"+
                    "你要搭捷運、公車、還是騎最環保又健康的腳踏車"+brocast)
            out = 1
    return  out
        
if __name__ == "__main__":
    destination = "台北火車站" #for testing
    out = transition(destination)