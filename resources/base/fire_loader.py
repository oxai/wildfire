from .data_loader import DataLoader
import sqlite3, os
import pandas as pd
from datetime import timedelta
import numpy as np
from resources.utils.df import latlng_condition, dates_overlap, date_in_range, df_date_in_range
import pickle


class FireLoader(DataLoader):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.df = self.load(*args, **kwargs)
        self.date_range_known = "START_DATE" in self.df or "END_DATE" in self.df

    def load(self, *args, **kwargs):
        """
        returns a pandas dataframe that has the wildfire records,
        with "LATITUDE", "LONGITUDE", either "DATE" or "START_DATE" and "END_DATE",
        "MIN_FIRE_SIZE" (optional), "CONFIDENCE" (optional)
        as its keys
        """
        raise NotImplementedError

    def get_records_in_range(self, bbox=None, from_date=None, until_date=None, min_fire_size=0.0, confidence_thresh=0.0):
        # path = os.path.join(self.data_dir(), f"{bbox}_{from_date}_{until_date}_{min_fire_size}_{confidence_thresh}.pk")
        # if os.path.exists(path):
        #     with open(path, "rb") as f:
        #         df = pickle.load(f)
        #     return df
        loc_cond = latlng_condition(self.df, bbox)
        date_cond = \
            dates_overlap(self.df, from_date, until_date) if self.date_range_known \
            else df_date_in_range(self.df["DATE"], from_date, until_date)
        fire_cond = \
            self.df["FIRE_SIZE"] >= min_fire_size if "FIRE_SIZE" in self.df \
            else self.df.apply(lambda x: True, axis=1)
        conf_cond = \
            self.df["CONFIDENCE"] >= confidence_thresh if "CONFIDENCE" in self.df \
            else self.df.apply(lambda x: True, axis=1)
        df = self.df[loc_cond & date_cond & fire_cond & conf_cond].copy()
        # with open(path, "wb") as f:
        #     pickle.dump(df, f)
        return df

    def get_records_on_date(self, date, bbox=None, min_fire_size=0.0, confidence_thresh=0.0):
        loc_cond = latlng_condition(self.df, bbox)
        date_cond = \
            date_in_range(date, self.df["START_DATE"], self.df["END_DATE"]) if self.date_range_known \
            else self.df["DATE"] == date
        fire_cond = \
            self.df["FIRE_SIZE"] >= min_fire_size if "FIRE_SIZE" in self.df \
            else self.df["index"].apply(lambda x: True)
        conf_cond = \
            self.df["CONFIDENCE"] >= confidence_thresh if "CONFIDENCE" in self.df \
            else self.df["index"].apply(lambda x: True)
        return self.df[loc_cond & date_cond & fire_cond & conf_cond].copy()

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
            print(f"Finding negative example [{len(data) + 1} / {n_samples}]...")
            index = np.random.choice(np.arange(len(date_range)))
            sample_date = date_range[index].date()
            delta = timedelta(days=date_margin)
            sample_start_date = pd.Timestamp(sample_date - delta)
            sample_end_date = pd.Timestamp(sample_date + delta)

            date_cond = \
                dates_overlap(self.df, sample_start_date, sample_end_date) if self.date_range_known \
                else df_date_in_range(self.df["DATE"], sample_start_date, sample_end_date)

            lng_left, lat_lower, lng_right, lat_upper = bbox
            lat = lat_lower + (lat_upper - lat_lower) * np.random.rand()
            lng = lng_left + (lng_right - lng_left) * np.random.rand()
            bbox_margin = [lng - latlng_margin, lat - latlng_margin, lng + latlng_margin, lat + latlng_margin]
            loc_cond = latlng_condition(self.df, bbox_margin)

            is_positive = any(date_cond & loc_cond)

            if not is_positive:
                data.append({
                    "LATITUDE": lat, "LONGITUDE": lng,
                    "START_DATE": sample_start_date, "END_DATE": np.datetime64(sample_date + delta)
                })

        df = pd.DataFrame(data)
        with open(path, "wb") as f:
            pickle.dump(df, f)
        return df
