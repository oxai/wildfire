import pandas as pd
import os
from resources.base.fire_loader import FireLoader


class ModisFireDataLoader(FireLoader):

    def __init__(self, filenames=None):
        if filenames is None:
            filenames = [
                "fire_archive_M6_2019-01-01_2019-12-31.csv"
            ]
        super().__init__(filenames)

    def load(self, filenames):
        df = pd.concat([pd.read_csv(os.path.join(self.data_dir(), f)) for f in filenames], axis=1)
        df.rename(columns={
            'latitude': 'LATITUDE',
            'longitude': 'LONGITUDE',
            'acq_date': 'DATE',
            'confidence': 'CONFIDENCE'
        }, inplace=True)
        df["DATE"] = pd.to_datetime(df["DATE"])
        print(df.head())
        return df
