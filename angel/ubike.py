# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 20:19:11 2018

@author: user
"""
#import pandas as pd
import json
import requests
from math import radians, cos, sin, asin, sqrt
import os

PJ = os.path.join
this_dir = os.path.dirname(os.path.abspath(__file__))

def haversine(place_A, place_B): 
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lat1,lon1 = place_A
    lat2,lon2 = place_B
    # 十進位轉弧度
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

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

def direction_request_bike(user_location , destination):
    API_key = "AIzaSyBmvshA169XyDvEACKgAgyFbOzbmedBo1k"
    origin = str(user_location[0])+","+str(user_location[1])
    URL = "https://maps.googleapis.com/maps/api/directions/json?"\
           +"origin="+origin \
           +"&destination="+destination \
           +"&mode=walk" \
           +"&language=zh-TW" \
           +"&key="+API_key
    r = requests.post(URL)
    content = json.loads(r.content.decode())
#    print (json.dumps(content, indent=4, sort_keys=True))
    return content

# =============================================================================
# def process_data():
#     df = pd.read_csv("YouBike.csv",encoding='big5')
#     stop_info = []
#     for i in range(0,len(df)):
#         sna = df["sna"][i]
#         lat = df["lat"][i]
#         lng = df["lng"][i]
#         ar = df["ar"][i]
#         info = [sna,[lat,lng],ar]
#         stop_info.append(info)
#     a = json.dumps(stop_info)
#     with open('ubike_stop_info.txt','w')as f:
#         f.write(a) 
# =============================================================================
    
def bike(destination):
    with open(PJ(this_dir,'ubike_stop_info.txt'),'r')as f:
        r = f.read()
        stop_info = json.loads(r)
    user_location = Geolocation_request()
    #get the response of the direction recommandtion
    content = direction_request_bike(user_location, destination)
    #get the lat,lng of destination
    destination_lat_lng = content["routes"][0]["legs"][0]["end_location"]
    destination_lat_lng = [destination_lat_lng['lat'],destination_lat_lng['lng']]
    
    #calculate the nearest stop from user's location and destination
    tmp_distance_start = 0
    tmp_distance_end = 0
    distance_start = 100000000
    distance_end = 10000000
    index_start = 0
    index_end = 0
    for i in range(0,len(stop_info)):
        if stop_info[i][1][0] != 'null':
            tmp_distance_start = haversine(user_location, stop_info[i][1])
            tmp_distance_end = haversine(destination_lat_lng, stop_info[i][1])
            if tmp_distance_start < distance_start:
                distance_start = tmp_distance_start
                index_start = i
            if tmp_distance_end < distance_end:
                distance_end = tmp_distance_end
                index_end = i
    start_stop = stop_info[index_start][2]
    end_stop = stop_info[index_end][2]
    
    return start_stop, end_stop
    

if __name__ == "__main__":
    stop_info, destination_lat_lng = bike()
#    stop_info = process_data()
#    user_location = Geolocation_request()
#    destination = "臺灣師範大學"
#    content = direction_request(user_location, destination)
#    destination_lat_lng = content["routes"][0]["legs"][0]["end_location"]
#    destination_lat_lng = [destination_lat_lng['lat'],destination_lat_lng['lng']]
    
    
    

    



