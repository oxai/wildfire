from resources.sentinelhub.show import plot_image
from resources.base.data_loader import DataLoader
from sentinelhub import WmsRequest, CRS, BBox


class SentinelHubDetaLoader(DataLoader):
    def __init__(self):
        super().__init__()
        pass

    def download(self, config):
        wms_request = WmsRequest(**config)
        wms_img = wms_request.get_data()

        plot_image(wms_img[-1])

    def load(self, config):
        pass
