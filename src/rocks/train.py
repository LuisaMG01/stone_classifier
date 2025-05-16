import torch
import torch.nn as nn
import torch.optim as optim
import time
from model import RockResNet
from utils import save_model
from torch.utils.data import WeightedRandomSampler
import numpy as np

def get_weighted_sampler(dataset):
    class_counts = {}
    for _, label in dataset.samples:
        class_counts[label] = class_counts.get(label, 0) + 1

    weights = [1.0 / class_counts[label] for _, label in dataset.samples]
    sampler = WeightedRandomSampler(weights, len(weights), replacement=True)
    return sampler

def train_model(train_loader, val_loader, num_classes, device, model_path="model/rock_cnn.pth"):
    model = RockResNet(num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    best_val_loss = float('inf')

    print("Starting training...\n")

    for epoch in range(20):
        epoch_start = time.time()
        model.train()
        running_loss = 0.0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        val_loss = evaluate(model, val_loader, criterion, device)
        duration = time.time() - epoch_start

        print(f"🧠 Epoch {epoch+1}/10 - Training Loss: {running_loss:.4f} | "
              f"Validation Loss: {val_loss:.4f} | Time: {duration:.2f}s")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_model(model, model_path)
            print("Improved model saved.")

    return model

def evaluate(model, val_loader, criterion, device):
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
    return val_loss
