from resources.base.data_loader import DataLoader
from sentinelhub import WcsRequest, CRS, BBox, MimeType


class SentinelHubDetaLoader(DataLoader):
    def __init__(self):
        super().__init__()
        pass

    def request(self, config):
        return WcsRequest(data_folder=self.data_dir(), image_format=MimeType.TIFF_d32f, **config)

    def download(self, config):
        self.request(config).save_data()

    def load(self, config):
        return self.request(config).get_data(save_data=True)

