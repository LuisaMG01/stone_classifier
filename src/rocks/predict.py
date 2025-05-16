import torch
from torchvision import transforms
from PIL import Image
from model import RockResNet  # Make sure it's the same model format used in training
import os

def load_model(model_path, device):
    checkpoint = torch.load(model_path, map_location=device)
    model = RockResNet(checkpoint['num_classes'])
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    return model, checkpoint['class_names']

def predict_image(image_path, model, class_names, device):
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop(224),
        transforms.ToTensor()
    ])

    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)

    return class_names[predicted.item()]

if __name__ == "__main__":
    import sys
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "download.jpeg")

    model_path = "model/rock_cnn_full.pth"

    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
    elif not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model, class_names = load_model(model_path, device)
        prediction = predict_image(image_path, model, class_names, device)
        print(f"Prediction: {prediction}")
