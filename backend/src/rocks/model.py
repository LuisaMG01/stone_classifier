import torch.nn as nn
import torchvision.models as models

class RockResNet(nn.Module):
    def __init__(self, num_classes):
        super(RockResNet, self).__init__()
        self.model = models.resnet18(pretrained=True)

        for param in self.model.parameters():
            param.requires_grad = False
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        return self.model(x)
