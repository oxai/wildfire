from resources.base.data_loader import DataLoader
from sentinelhub import WcsRequest, MimeType
import os


class SentinelHubDataLoader(DataLoader):
    def __init__(self, subdir="tmp"):
        super().__init__()
        self.subdir = subdir

    def set_subdir(self, subdir="tmp"):
        self.subdir = subdir

    def data_subdir(self):
        path = os.path.join(self.data_dir(), self.subdir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def request(self, config):
        return WcsRequest(data_folder=self.data_subdir(), image_format=MimeType.TIFF_d32f, **config)

    def download(self, config):
        self.request(config).save_data()

    def load(self, config):
        return self.request(config).get_data(save_data=True)
