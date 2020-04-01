import torch.optim as optim
from functools import partial
from  .dataset import *
from torch.utils.data import DataLoader
import torch

def get_model(model, lr=0.5, nh=50):
    model = model
    return model, optim.SGD(model.parameters(), lr=lr)

import re

_camel_re1 = re.compile('(.)([A-Z][a-z]+)')
_camel_re2 = re.compile('([a-z0-9])([A-Z])')
def camel2snake(name):
    s1 = re.sub(_camel_re1, r'\1_\2', name)
    return re.sub(_camel_re2, r'\1_\2', s1).lower()

from typing import *

def listify(o):
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, str): return [o]
    if isinstance(o, Iterable): return list(o)
    return [o]

def get_stats(df, ROOT_DIR, BS):
    i = 0
    batch_mean = 0
    batch_std = 0
    trainset = Data(df=df, root_dir=ROOT_DIR)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=BS,
                                              shuffle=True)
    for inputs, _ in trainloader:
        i = inputs.shape[0]
        batch_mean += torch.mean(inputs, dim=[0, 2, 3]) * i / len(trainloader.dataset)
        batch_std += torch.std(inputs, dim=[0, 2, 3]) * i / len(trainloader.dataset)
    torch.save(batch_mean, 'input/mean.pt')
    torch.save(batch_std, 'input/std.pt')
    return batch_mean, batch_std