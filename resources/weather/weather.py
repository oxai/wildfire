from wwo_hist import retrieve_hist_data
import numpy as np
import pandas as pd


def get_wwo_weather(lat_lon_list, start_date, end_date, frequency, key):
    hist_weather_data = retrieve_hist_data(key, lat_lon_list, start_date, end_date, frequency=frequency,
                                           location_label=False, export_csv=True, store_df=True)
    data = hist_weather_data[0].drop(
        ['sunrise', 'sunset', 'moonrise', 'moonset', 'moon_illumination', 'FeelsLikeC', 'HeatIndexC', 'WindChillC'],
        axis=1)
    wu = pd.DataFrame(np.cos(data['windspeedKmph'].to_numpy().astype(np.float32)))
    wv = pd.DataFrame(np.sin(data['windspeedKmph'].to_numpy().astype(np.float32)))
    data['wind_u'] = wu
    data['wind_v'] = wv
    return hist_weather_data
