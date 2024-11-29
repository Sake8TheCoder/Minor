import cv2
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile

net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "mobilenet_iter_73000.caffemodel")

with open("class_names.txt", "rt") as f:
    class_names = f.read().strip().split("\n")

def process_image(img_file):
    file_bytes = np.frombuffer(img_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"Error: Could not read the image from '{img_file}'.")
        return
    
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5, (127.5, 127.5, 127.5), False)
    net.setInput(blob)
    detections = net.forward()

    listObjects = []
    labels = {}
    count = 0
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])
            label = class_names[class_id]
            confidence_score = float(confidence)

            if label not in labels:
                labels[label] = True
                listObjects.append((label, confidence_score))
                count += 1

            if count == 3:
                break

    return listObjects
