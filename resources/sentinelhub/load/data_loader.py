from resources.base.data_loader import DataLoader
from sentinelhub import WcsRequest, MimeType
import os


class SentinelHubDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def data_subdir(self, subdir):
        path = os.path.join(self.data_dir(), subdir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def request(self, config, subdir):
        return WcsRequest(data_folder=self.data_subdir(subdir), image_format=MimeType.TIFF_d32f, **config)

    def download(self, config, subdir="tmp"):
        self.request(config, subdir).save_data()

    def load(self, config, subdir="tmp"):
        return self.request(config, subdir).get_data(save_data=True)
