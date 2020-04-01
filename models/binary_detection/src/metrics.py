import torch

def accuracy(out, yb): return (torch.argmax(out, dim=1)==yb).float().mean()
