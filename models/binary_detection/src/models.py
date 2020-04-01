import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(10, 20, kernel_size=(2, 2))
        self.fc1 = nn.Linear(4500, 2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = x.view(-1, 20 * 15 * 15)
        x = self.fc1(x)

        return x