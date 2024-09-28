import os
from ultralytics import YOLO
import cv2
import numpy as np

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
    if isinstance(img_file, InMemoryUploadedFile):
      # Read the file into a NumPy array
        file_bytes = np.fromstring(img_file.read(), np.uint8)
        Image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    img = cv2.imread(Image)
    if img is None:
        print(f"Error: Could not read the image from '{Image}'.")
        return
    results = model(Image)
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
    
