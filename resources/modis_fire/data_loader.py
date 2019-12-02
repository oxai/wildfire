from resources.base.data_loader import DataLoader
import pandas as pd
import os
from resources.utils.df import latlng_condition, date_in_range


class ModisFireDataLoader(DataLoader):

    def __init__(self, filename="fire_archive_M6_87061.csv"):
        super().__init__()
        self.df = pd.read_csv(os.path.join(self.data_dir(), filename))
        self.df.rename(columns={
            'latitude': 'LATITUDE',
            'longitude': 'LONGITUDE',
            'acq_date': 'DATE'
        }, inplace=True)
        print(self.df.head())

    def get_records(self, loc=None, from_date=None, until_date=None):
        loc_cond = latlng_condition(self.df, loc)
        date_cond = date_in_range(self.df, "DATE", from_date, until_date)
        return self.df[loc_cond & date_cond].copy()
