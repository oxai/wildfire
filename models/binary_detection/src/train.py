import torch.nn as nn
from  .dataset import *
from .metrics import accuracy
from torch.utils.data import DataLoader
from .data_bunch import *
from .learner import *
from .runner import *
from . import dispatcher
from torchvision import transforms

TRAINING_DATA = os.environ.get("TRAINING_DATA")
TEST_DATA = os.environ.get("TEST_DATA")
MODEL = os.environ.get("MODEL")
ROOT_DIR = os.environ.get("ROOT_DIR")
c = int(os.environ.get("c"))
N_EPOCHS = int(os.environ.get("N_EPOCHS"))
LR = float(os.environ.get("LR"))
BS = int(os.environ.get("BS"))


if __name__ == "__main__":
    train_df = pd.read_csv(TRAINING_DATA)
    valid_df = pd.read_csv(TEST_DATA)
    if os.path.isfile("input/mean.pt") and os.path.isfile("input/std.pt"):
        mean = torch.load('input/mean.pt')
        std = torch.load("input/std.pt")
    else:
        mean, std = get_stats(train_df, ROOT_DIR, BS)

    transform = transforms.Compose([transforms.Normalize(mean, std)])

    trainset = Data(df=train_df, root_dir=ROOT_DIR, transform=transform)
    testset = Data(df=valid_df, root_dir=ROOT_DIR, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=BS,
                                              shuffle=True)
    testloader = torch.utils.data.DataLoader(testset, batch_size=2*BS,
                                             shuffle=True)
    ytrain = train_df.target.values
    yvalid = valid_df.target.values

    model = dispatcher.MODELS[MODEL]
    if os.path.isfile(f"models/{MODEL}.pth"):
        model.load_state_dict(torch.load(f"models/{MODEL}.pth"))

    loss_func = nn.CrossEntropyLoss()
    data = DataBunch(trainloader, testloader, c=c)
    learn = Learner(*get_model(model, lr=LR), loss_func, data)
    stats = AvgStatsCallback([accuracy])
    run = Runner(cbs=stats)
    run.fit(N_EPOCHS, learn)

    torch.save(model.state_dict(), f"models/{MODEL}.pth")

