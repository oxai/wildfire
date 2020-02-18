import sqlite3, os
import pandas as pd
from resources.base.fire_loader import FireLoader


class FpaFodDataLoader(FireLoader):

    def __init__(self, filename="FPA_FOD_20170508.sqlite"):
        self.cnx = sqlite3.connect(os.path.join(self.data_dir(), filename))
        super().__init__()

    def load(self):
        # Extract relevant info
        df = pd.read_sql_query(
            "SELECT LATITUDE, LONGITUDE, DISCOVERY_DATE, CONT_DATE, FIRE_SIZE FROM 'Fires'", self.cnx
        )
        # Create usable dates
        df['START_DATE'] = pd.to_datetime(df['DISCOVERY_DATE'] - pd.Timestamp(0).to_julian_date(), unit='D')
        df['END_DATE'] = pd.to_datetime(df['CONT_DATE'] - pd.Timestamp(0).to_julian_date(), unit='D')
        df = df.drop(columns=["DISCOVERY_DATE", "CONT_DATE"])
        return df
