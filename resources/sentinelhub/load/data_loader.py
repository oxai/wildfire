from resources.base.data_loader import DataLoader
from sentinelhub import WmsRequest, WcsRequest, MimeType
import os


class SentinelHubDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def request(self, config, subdir):
        request = WmsRequest if "width" in config else WcsRequest
        return request(data_folder=self.data_subdir(subdir), image_format=MimeType.TIFF_d32f, **config)

    def download(self, config, subdir="tmp"):
        self.request(config, subdir).save_data()

    def load(self, config, subdir="tmp"):
        return self.request(config, subdir).get_data(save_data=True)
