import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
import numpy as np
import cv2
import redis
import time
import uuid
from utils.minio_client import download_image
from utils.es_client import index_feature_vector

# Redis subscriber
r = redis.Redis(host='redis', port=6379, decode_responses=True)
p = r.pubsub()
p.subscribe("image_uploads")

# Load model
model = resnet18(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def extract_features(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        features = model(tensor).squeeze().numpy()
    return features.tolist()

print("Listening for new images...")

while True:
    message = p.get_message()
    if message and message["type"] == "message":
        file_name = message["data"]
        print(f"Received image: {file_name}")

        local_path = download_image("images", file_name)
        features = extract_features(local_path)
        print(f"Extracted features for {file_name}: {features}")
        index_feature_vector("images", str(uuid.uuid4()), features, {"file_name": file_name})

    time.sleep(1)
