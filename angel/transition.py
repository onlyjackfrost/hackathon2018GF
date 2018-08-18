# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 19:05:17 2018
    to use this funtion, call "transition()"
@author: onlyjackfrost
"""
import requests
import json

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
    cost = [text,duration]
    return cost

def bus_detail_parser(bus_detail):
    """
        parse the detail information for the transit
        上車站、下車站、公車代號、該班公車發車間隔時間
    """
    #get route detail
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
        if not shortname:
            f.write("距離很近，不用搭公車")
        else:
            f.write("請從"+departure_stop+"站，搭"+shortname+"公車到，"+arrival_stop+"站下車")
    return shortname


def tram_detail_parser(bus_detail):
    """
        parse the detail information for the transit
        上車站、下車站、捷運線
    """
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
        if not shortname:
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
    bus_shortname = bus_detail_parser(bus_detail)
    #parse the cost and time 
    cost = cost_parser(bus_detail)
    return cost, bus_detail, bus_shortname

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

def transition(destination):
    bus_cost, bus_detail, bus_shortname = bus_algorithm(destination)
    tram_cost, tram_detail, tram_shortname = tram_algorithm(destination)
    with open("transition_cost.txt","w") as f:
        if not tram_shortname or not bus_shortname:
            f.write("距離很近，你問人然後走路吧")
        if bus_shortname and tram_shortname:
            f.write("搭捷運要"+tram_cost[1]+','+tram_cost[0]+"元"+","
                    "搭公車要"+bus_cost[1]+","+bus_cost[0]+"元"+
                    "你要搭捷運還是公車")
    return bus_detail, tram_detail, bus_shortname, tram_shortname
        
if __name__ == "__main__":
    destination = "台北車站"
    bus_detail, tram_detail, bus_shortname, tram_shortname = transition(destination)