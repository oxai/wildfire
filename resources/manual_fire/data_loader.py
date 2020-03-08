import pandas as pd
import os
from resources.base.fire_loader import FireLoader


class ManualFireDataLoader(FireLoader):

    def __init__(self, filename="examples/manual_fires.csv"):
        super().__init__(filename)

    def load(self, filename):
        df = pd.read_csv(os.path.join(self.data_dir(), filename))
        df["LATITUDE"] = (df["lat_min"] + df["lat_max"]) / 2
        df["LONGITUDE"] = (df["long_min"] + df["long_max"]) / 2
        df["DATE"] = pd.to_datetime(df["date"])
        print(df.head())
        return df
