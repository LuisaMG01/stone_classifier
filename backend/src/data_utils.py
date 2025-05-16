import torch
from torchvision import datasets, transforms

def get_transform():
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    return {'train': train_transform, 'val': val_transform}

def load_data(data_dir, transforms):
    train_dataset = datasets.ImageFolder(f'{data_dir}/train', transform=transforms['train'])
    val_dataset = datasets.ImageFolder(f'{data_dir}/val', transform=transforms['val'])

    dataloaders = {
        'train': torch.utils.data.DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=0),
        'val': torch.utils.data.DataLoader(val_dataset, batch_size=16, shuffle=False, num_workers=0)
    }

    dataset_sizes = {
        'train': len(train_dataset),
        'val': len(val_dataset)
    }

    return dataloaders, dataset_sizes, train_dataset.classes
