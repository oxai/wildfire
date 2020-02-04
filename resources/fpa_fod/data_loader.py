from resources.base.data_loader import DataLoader
import sqlite3, os
import pandas as pd
from datetime import timedelta
import numpy as np
from resources.utils.df import latlng_condition, dates_overlap, date_in_range
import pickle


class FpaFodDataLoader(DataLoader):

    def __init__(self, filename="FPA_FOD_20170508.sqlite"):
        super().__init__()
        self.cnx = sqlite3.connect(os.path.join(self.data_dir(), filename))
        self.df = self.load()

    def load(self):
        # Extract relevant info
        df = pd.read_sql_query(
            "SELECT STAT_CAUSE_DESCR, LATITUDE, LONGITUDE, DISCOVERY_DATE, CONT_DATE, FIRE_SIZE FROM 'Fires'", self.cnx
        )
        # Create usable dates
        df['START_DATE'] = pd.to_datetime(df['DISCOVERY_DATE'] - pd.Timestamp(0).to_julian_date(), unit='D')
        df['END_DATE'] = pd.to_datetime(df['CONT_DATE'] - pd.Timestamp(0).to_julian_date(), unit='D')
        df = df.drop(columns=["DISCOVERY_DATE", "CONT_DATE"])
        return df

    def get_records(self, bbox=None, from_date=None, until_date=None, min_fire_size=0.0):
        path = os.path.join(self.data_dir(), f"{bbox}_{from_date}_{until_date}_{min_fire_size}.pk")
        if os.path.exists(path):
            with open(path, "rb") as f:
                df = pickle.load(f)
            return df
        loc_cond = latlng_condition(self.df, bbox)
        date_cond = dates_overlap(self.df, from_date, until_date)
        fire_cond = self.df["FIRE_SIZE"] >= min_fire_size
        df = self.df[loc_cond & date_cond & fire_cond].copy()
        with open(path, "wb") as f:
            pickle.dump(df, f)
        return df

    def get_records_on_day(self, date, bbox=None, min_fire_size=0.0):
        loc_cond = latlng_condition(self.df, bbox)
        date_cond = date_in_range(date, self.df["START_DATE"], self.df["END_DATE"])
        fire_cond = self.df["FIRE_SIZE"] >= min_fire_size
        return self.df[loc_cond & date_cond & fire_cond].copy()

    def get_neg_examples(self, bbox, from_date, until_date, n_samples, date_margin=20, latlng_margin=0.1):
        path = os.path.join(
            self.data_dir(),
            f"{bbox}_{from_date}_{until_date}_{n_samples}_{date_margin}_{latlng_margin}.pk"
        )
        if os.path.exists(path):
            with open(path, "rb") as f:
                df = pickle.load(f)
            return df
        data = []
        date_range = pd.date_range(from_date, until_date).to_pydatetime()
        while len(data) < n_samples:
            print(f"Finding {len(data)}th negative example...")
            index = np.random.choice(np.arange(len(date_range)))
            date = date_range[index].date()
            delta = timedelta(days=date_margin)
            date_cond = dates_overlap(self.df, pd.Timestamp(date - delta), pd.Timestamp(date + delta))

            lng_left, lat_lower, lng_right, lat_upper = bbox
            lat = lat_lower + (lat_upper - lat_lower) * np.random.rand()
            lng = lng_left + (lng_right - lng_left) * np.random.rand()
            bbox_margin = [lng - latlng_margin, lat - latlng_margin, lng + latlng_margin, lat + latlng_margin]
            loc_cond = latlng_condition(self.df, bbox_margin)

            is_positive = any(date_cond & loc_cond)

            if not is_positive:
                data.append({
                    "LATITUDE": lat, "LONGITUDE": lng,
                    "START_DATE": np.datetime64(date - delta), "END_DATE": np.datetime64(date + delta)
                })

        df = pd.DataFrame(data)
        with open(path, "wb") as f:
            pickle.dump(df, f)
        return df
