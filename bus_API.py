# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 20:51:36 2018

@author: admin123
"""
import json

def get_data(root_dir):
    with open(root_dir+"GetRoute",encoding="utf8") as f:
        print('load GetRoute file...')
        content = f.read()
    GetRoute = json.loads(content)
    
    with open(root_dir+"GetStop",encoding="utf8") as f:
        print('load GetStop file...')
        content = f.read()
    GetStop = json.loads(content)
    return GetRoute,GetStop

def get_route_list(GetRoute):
    #從GetRoute["BusInfo"]裡找公車路線(ID)，然後新增到RouteNumbList
    RouteNumbList = list()
    for businfo in GetRoute["BusInfo"]:
        id1 = businfo["Id"]
        if id1 in RouteNumbList:
            continue
        else:
            RouteNumbList.append(id1)
    print("RouteNumbList :",RouteNumbList[0:5]," ...")
    return RouteNumbList

def stops_in_route(RouteNumbList,GetStop):
    #找出各個路線的STOP(站)
    routelist = {}
    for route in RouteNumbList:
        routelist[route] = []
        for stop in GetStop["BusInfo"]:
            if stop["routeId"] == route:
                #新增
                routelist[route].append([stop["seqNo"],stop["Id"]])
        print(route ," finished...")
    return routelist

def sort_stops(routelist):
    #對公車路線裡的站依"前進順序"做排序
    for route in routelist:
        routelist[route] = sorted(routelist[route])
    print("... finish sorting")
    return routelist

if __name__=='__main__':
    root_dir = '20180706_Data.Taipei_TP/'
    GetRoute,GetStop = get_data(root_dir)
    RouteNumbList = get_route_list(GetRoute)
    routelist = stops_in_route(RouteNumbList,GetStop)
    routelist = sort_stops(routelist)  
