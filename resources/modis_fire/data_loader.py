import pandas as pd
import os
from resources.base.fire_loader import FireLoader


class ModisFireDataLoader(FireLoader):

    def __init__(self, filename="fire_archive_M6_87061.csv"):
        super().__init__(filename)

    def load(self, filename):
        df = pd.read_csv(os.path.join(self.data_dir(), filename))
        df.rename(columns={
            'latitude': 'LATITUDE',
            'longitude': 'LONGITUDE',
            'acq_date': 'DATE',
            'confidence': 'CONFIDENCE'
        }, inplace=True)
        df["DATE"] = pd.to_datetime(df["DATE"])
        print(df.head())
        return df
