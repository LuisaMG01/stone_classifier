import torch
import time
from sklearn.metrics import classification_report
from utils import load_model
from model import RockResNet

def test_model(test_loader, num_classes, device, model_path="saved_model/rock_cnn.pth", class_names=None):
    model = RockResNet(num_classes).to(device)
    load_model(model, model_path)

    model.eval()
    y_true, y_pred = [], []

    start_time = time.time()
    print("Starting predictions on test set...")

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            y_true.extend(labels.numpy())
            y_pred.extend(preds.cpu().numpy())

    print("\nResults:")
    print(classification_report(y_true, y_pred, target_names=class_names))

    print(f"Evaluated in: {time.time() - start_time:.2f} seconds.")
