from resources.weather.weather import get_wwo_weather

lat = 34.06
lon = -188.82
wwo_key = 'f56effb3c3f24af2bb4121324201101'
start_date = '11-DEC-2018'
end_date = '11-MAR-2019'
lat_lon_list = ['48.834,2.394']
freq = 12
r = get_wwo_weather(lat_lon_list, start_date, end_date, freq, wwo_key)
print(r[0].head())
