def latlng_condition(df, bbox=None, lat_key="LATITUDE", lng_key="LONGITUDE"):
    if bbox is None:
        return df.apply(lambda x: True, axis=1)
    df_lat = df[lat_key]
    df_lng = df[lng_key]
    lng_left, lat_lower, lng_right, lat_upper = bbox
    lat_cond = (df_lat > lat_lower) & (df_lat < lat_upper)
    lng_cond = (df_lng > lng_left) & (df_lng < lng_right) |\
               (df_lng - 360 > lng_left) & (df_lng - 360 < lng_right) |\
               (df_lng + 360 > lng_left) & (df_lng + 360 < lng_right)
    return lat_cond & lng_cond


def dates_overlap(df, from_date=None, until_date=None, start_date_key="START_DATE", end_date_key="END_DATE"):
    started_before_until_date =\
        df.apply(lambda x: True, axis=1) if until_date is None \
        else df[start_date_key] <= until_date
    ended_after_from_date = \
        df.apply(lambda x: True, axis=1) if from_date is None \
        else df[end_date_key] >= from_date
    return started_before_until_date & ended_after_from_date


def date_in_range(date, start_date, end_date):
    return (date >= start_date) & (date <= end_date)


def df_date_in_range(df_date, start_date=None, end_date=None):
    date_after_start_date =\
        df_date.apply(lambda x: True) if start_date is None \
        else df_date >= start_date
    date_before_end_date =\
        df_date.apply(lambda x: True) if end_date is None \
        else df_date <= end_date
    return date_after_start_date & date_before_end_date
