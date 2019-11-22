from datetime import datetime
import os, sys


class DataLoader(object):

    def __init__(self, *args, **kwargs):
        pass

    def download(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass

    def data_dir(self):
        path = os.path.join(os.path.dirname(os.path.abspath(sys.modules[self.__class__.__module__].__file__)), "data_dir")
        if not os.path.exists(path):
            os.mkdir(path)
        return path
