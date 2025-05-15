# main.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import torch.nn.functional as F

from data_utils import get_transform, load_data
from model_utils import train_model, visualize_results, evaluate_model

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

transformations = get_transform()
dataloaders, dataset_sizes, class_names = load_data("data", transformations)


def setup_model(model_name="resnet50", pretrained=True, freeze_layers=True):
    if model_name == "resnet50":
        model = models.resnet50(weights="IMAGENET1K_V2" if pretrained else None)
        if freeze_layers:
            for param in model.parameters():
                param.requires_grad = False
        num_ftrs = model.fc.in_features
        model.fc = nn.Sequential(nn.Dropout(0.5), nn.Linear(num_ftrs, 3))
    elif model_name == "efficientnet":
        model = models.efficientnet_b0(weights="IMAGENET1K_V1" if pretrained else None)
        if freeze_layers:
            for param in model.parameters():
                param.requires_grad = False
        num_ftrs = model.classifier[1].in_features
        model.classifier = nn.Sequential(nn.Dropout(0.5), nn.Linear(num_ftrs, 3))
    return model.to(device)


model = setup_model(model_name="resnet50", pretrained=True, freeze_layers=False)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.fc.parameters(), lr=0.01, momentum=0.9)
scheduler = lr_scheduler.ReduceLROnPlateau(
    optimizer, mode="max", factor=0.1, patience=3
)

model, history = train_model(
    model,
    criterion,
    optimizer,
    scheduler,
    dataloaders,
    dataset_sizes,
    num_epochs=20,
    device=device,
)

visualize_results(history)

val_acc = evaluate_model(
    model, dataloaders["val"], dataset_sizes["val"], class_names, device=device
)

torch.save(model.state_dict(), "rock_classification_model.pth")

if val_acc < 0.9:
    print("ResNet50 accuracy below 90%. Trying EfficientNet...")
    model = setup_model(model_name="efficientnet", pretrained=True, freeze_layers=False)
    optimizer = optim.SGD(model.classifier.parameters(), lr=0.01, momentum=0.9)
    scheduler = lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="max", factor=0.1, patience=3
    )
    model, history = train_model(
        model,
        criterion,
        optimizer,
        scheduler,
        dataloaders,
        dataset_sizes,
        num_epochs=25,
        device=device,
    )
    visualize_results(history)
    val_acc_eff = evaluate_model(
        model, dataloaders["val"], dataset_sizes["val"], class_names, device=device
    )
    if val_acc_eff > val_acc:
        torch.save(model.state_dict(), "rock_classification_model.pth")
        print(
            f"EfficientNet achieved better accuracy ({val_acc_eff:.4f}) and has been saved."
        )
    else:
        print(f"ResNet50 remains the best model with accuracy {val_acc:.4f}.")
else:
    print(f"Success! Achieved accuracy of {val_acc*100:.2f}% with ResNet50.")


def predict_image(image_path, model, transform, class_names):
    img = plt.imread(image_path)
    plt.imshow(img)
    plt.axis("off")
    plt.show()

    img_tensor = transform(Image.open(image_path)).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(img_tensor)
        _, preds = torch.max(outputs, 1)
        probs = F.softmax(outputs, dim=1)[0]

    pred_class = class_names[preds.item()]
    confidence = probs[preds.item()].item() * 100
    print(f"Prediction: {pred_class} with confidence {confidence:.2f}%")

    for i, (cls, prob) in enumerate(zip(class_names, probs)):
        print(f"{cls}: {prob.item()*100:.2f}%")

    return pred_class, confidence
