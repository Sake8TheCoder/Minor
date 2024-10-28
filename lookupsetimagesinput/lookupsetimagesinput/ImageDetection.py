import os
from ultralytics import YOLO
import cv2
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile

model = YOLO("yolov8l.pt")
class_names = model.names


def process_image(img_file):
    file_bytes = np.frombuffer(img_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: Could not read the image from '{img}'.")
        return
    results = model(img)
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
            listObjects.append([label, confidence])
            count += 1
            if count == 3:
                break
    return listObjects
