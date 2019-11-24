import numpy as np


def latlng_condition(df, loc=None, lat_key="LATITUDE", lng_key="LONGITUDE"):
    if loc is None:
        return df[lat_key].apply(lambda x: True)
    df_lat = df[lat_key]
    df_lng = df[lng_key]
    lat, lng, delta = [loc[k] for k in ["lat", "lng", "delta"]]
    lat_cond = (df_lat > lat - delta) & (df_lat < lat + delta)
    lng_cond = (df_lng > lng - delta) & (df_lng < lng + delta) |\
               (df_lng - 360 > lng - delta) & (df_lng - 360 < lng + delta) |\
               (df_lng + 360 > lng - delta) & (df_lng + 360 < lng + delta)
    return lat_cond & lng_cond


def dates_overlap(df, from_date=None, until_date=None, start_date_key="START_DATE", end_date_key="END_DATE"):
    started_before_until_date =\
        df[start_date_key].apply(lambda x: True) if until_date is None \
        else df[start_date_key] <= until_date
    ended_after_from_date = \
        df[end_date_key].apply(lambda x: True) if from_date is None \
        else df[end_date_key] >= from_date
    return started_before_until_date & ended_after_from_date


def date_in_range(date, start_date, end_date):
    return (date > start_date) & (date < end_date)
