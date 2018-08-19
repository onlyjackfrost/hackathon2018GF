# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 07:27:20 2018
    weather broacast
@author: user
"""
import pandas as pd
import json


def sum_rain(df, town):
    total_rain = 0.0
    cnt = 0.0
    for i in range(0,len(df)):
        if df["town_name"][i] == town:
            total_rain += df["h_24r"][i]
            cnt += 1
    avg_rain = total_rain / cnt
    return avg_rain

def weather():
    with open("weather.txt",'r') as f:
        content = f.read()
        dict_avg_rain = json.loads(content)
    
#    dict_avg_rain=dict()
#    for town in town_name:
#        avg_rain = sum_rain(df,town)
#        if avg_rain > 4:
#            broacast = "提醒您今天目的地可能會下雨"
#        else :
#            broacast = "提醒您今天目的地不會下雨"
#        dict_avg_rain[town] = broacast
    return dict_avg_rain
if __name__ == "__main__":
    dict_avg_rain = weather()
        

