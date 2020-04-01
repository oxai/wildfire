from torch.utils.data import Dataset
import torch
from skimage import io, transform
import os
import pandas as pd

class Data(Dataset):
    def __init__(self, df, root_dir, transform = None):
        self.images = df
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.images.iloc[idx, 0])
        input_ = io.imread(img_name)
        input_ = torch.from_numpy(input_)
        class_ = self.images.iloc[idx, 1]

        if self.transform:
            input_ = self.transform(input_)
        return input_, class_

if __name__ == "__main__":
    TRAINING_DATA = os.environ.get("TRAINING_DATA")
    ROOT_DIR = os.environ.get("ROOT_DIR")
    d = Data(df = pd.read_csv(TRAINING_DATA), root_dir=ROOT_DIR)
    print(d[1])