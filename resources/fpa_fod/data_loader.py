from resources.base.data_loader import DataLoader
import sqlite3, os
import pandas as pd
from resources.utils.df import latlng_condition, dates_overlap, date_in_df_range


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

    def get_records(self, loc=None, from_date=None, until_date=None, min_fire_size=0.0):
        loc_cond = latlng_condition(self.df, loc)
        date_cond = dates_overlap(self.df, from_date, until_date)
        fire_cond = self.df["FIRE_SIZE"] >= min_fire_size
        return self.df[loc_cond & date_cond & fire_cond].copy()

    def get_records_on_day(self, date, loc=None, min_fire_size=0.0):
        loc_cond = latlng_condition(self.df, loc)
        date_cond = date_in_df_range(date, self.df["START_DATE"], self.df["END_DATE"])
        fire_cond = self.df["FIRE_SIZE"] >= min_fire_size
        return self.df[loc_cond & date_cond & fire_cond].copy()