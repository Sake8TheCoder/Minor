import os
from ultralytics import YOLO
import cv2
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile


model = YOLO("yolov8l.pt")
class_names = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus",
    "train", "truck", "boat", "traffic light", "fire hydrant",
    "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase",
    "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich",
    "orange", "broccoli", "carrot", "hot dog", "pizza", "donut",
    "cake", "chair", "couch", "potted plant", "bed", "dining table",
    "toilet", "TV", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors",
    "teddy bear", "hair dryer", "toothbrush"
]

def process_image(img_file):
    file_bytes = np.frombuffer(img_file.read(), np.uint8)
    # Decode the byte array into an image using OpenCV
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: Could not read the image from '{img}'.")
        return
    results = model(img)
    highest_conf = 0
    best_box = None
    best_class_id = None
    listObjects = []
    labels = {}
    count = 0
    for box in results[0].boxes:
        confidence = box.conf[0].item()
        class_id_current = int(box.cls[0].item())
        if class_id_current < len(class_names):
            label = class_names[class_id_current]
            if label in labels:
              continue
            labels[label] = True
            listObjects.append([label,confidence])
            count += 1
            if count == 3:
              break
        else:
            label = "Unknown"

    return listObjects
    
