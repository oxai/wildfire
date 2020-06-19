from datetime import datetime
import os, sys


class DataLoader(object):
    dir_path = None

    def data_subdir(self, subdir):
        path = os.path.join(self.data_dir(), subdir)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def load(self, *args, **kwargs):
        raise NotImplementedError

    def data_dir(self):
        if self.dir_path is None:
            self.dir_path = os.path.join("data",
                os.path.basename(os.path.dirname(sys.modules[self.__class__.__module__].__file__)))
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        return self.dir_path
