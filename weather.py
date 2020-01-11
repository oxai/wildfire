import math
import pandas as pd
import numpy as np
from pdb import set_trace
from wwo_hist import retrieve_hist_data
import requests, json 

frequency = 3
start_date = '11-DEC-2018'
end_date = '11-MAR-2019'
wwo_api_key = 'f56effb3c3f24af2bb4121324201101'
#location_list = ['singapore','california','48.834,2.394']
location_list = ['48.834,2.394']
#hist_weather_data = retrieve_hist_data(wwo_api_key, location_list,start_date,end_date,frequency,location_label = False,export_csv = True,store_df = True)
#def get_weather(lat,lon,appid):
#return requests.get(f"http://samples.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}").json()

#assert len(hist_weather_data)==1
#data = hist_weather_data[0].drop(['sunrise','sunset','moonrise','moonset','moon_illumination','FeelsLikeC','HeatIndexC','WindChillC'],axis=1)
data = pd.read_csv('test_weather.csv')
wu= pd.DataFrame(np.cos(data['windspeedKmph'].to_numpy().astype(np.float32)))
wv= pd.DataFrame(np.sin(data['windspeedKmph'].to_numpy().astype(np.float32)))
data['wind_u'] = wu
data['wind_v'] = wv

print(data)

if __name__ == "__main__":

    lat = 34.06
    lon = -188.82
    owm_appid = '714e7aa2d0366dd763d73046f1889930'
    r = get_weather(lat,lon,appid)
    print(r)
