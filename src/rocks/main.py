import torch
import time
from dataloader import get_dataloaders
from train import train_model, get_weighted_sampler
from evaluate import test_model
from torch.utils.data import DataLoader

def main():
    start_time = time.time()
    print("🔄 Loading data...")

    data_dir = "data/rocks"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_dataset, val_dataset, test_dataset, class_names = get_dataloaders(data_dir, return_datasets=True)

    print(f" Data loaded. Detected classes: {class_names}")
    print(" Starting training...\n")

    sampler = get_weighted_sampler(train_dataset)

    train_loader = DataLoader(train_dataset, batch_size=32, sampler=sampler)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    model = train_model(train_loader, val_loader, len(class_names), device)

    print("\n Evaluating final model on test set...")
    test_model(test_loader, len(class_names), device, class_names=class_names)


if __name__ == "__main__":
    main()
