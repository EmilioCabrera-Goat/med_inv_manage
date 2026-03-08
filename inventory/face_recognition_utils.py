import face_recognition
import numpy as np
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# use absolute path so it always finds the folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWN_DIR = os.path.join(BASE_DIR, 'media', 'known_people')
TFLITE_PATH = os.path.join(BASE_DIR, 'detector.tflite')
PERSON_INFO_DIR = os.path.join(BASE_DIR, 'person_info')

known_face_encodings = []
known_face_names = []

print(f"Looking for known faces in: {KNOWN_DIR}")

# create folder if it doesn't exist
os.makedirs(KNOWN_DIR, exist_ok=True)

for filename in os.listdir(KNOWN_DIR):
    path = os.path.join(KNOWN_DIR, filename)
    if not os.path.isfile(path):
        continue
    img = face_recognition.load_image_file(path)
    encodings = face_recognition.face_encodings(img)
    if encodings:
        known_face_encodings.append(encodings[0])
        known_face_names.append(os.path.splitext(filename)[0])
        print(f"Loaded: {filename}")
    else:
        print(f"No face found in: {filename}")

print(f"Total known faces loaded: {len(known_face_names)}")

base_options = python.BaseOptions(model_asset_path=TFLITE_PATH)
options = vision.FaceDetectorOptions(base_options=base_options, min_detection_confidence=0.8)
detector = vision.FaceDetector.create_from_options(options)

def detect_and_recognize(frame_rgb):
    ih, iw, _ = frame_rgb.shape
    cx, cy = iw // 2, ih // 2
    radius = 150

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    detection_result = detector.detect(mp_image)

    print(f"Faces detected: {len(detection_result.detections)}, Known faces: {known_face_names}")

    if not detection_result.detections:
        return None, None

    for detection in detection_result.detections:
        bbox = detection.bounding_box
        x, y, w, h = int(bbox.origin_x), int(bbox.origin_y), int(bbox.width), int(bbox.height)

        face_center_x = x + w // 2
        face_center_y = y + h // 2
        distance = np.sqrt((face_center_x - cx)**2 + (face_center_y - cy)**2)

        print(f"Distance from circle center: {distance:.1f}, radius: {radius}")

        if distance > radius:
            print("Face outside circle")
            continue

        top, right, bottom, left = y, x + w, y + h, x
        top = max(0, top)
        left = max(0, left)
        bottom = min(ih, bottom)
        right = min(iw, right)

        face_encodings = face_recognition.face_encodings(frame_rgb, [(top, right, bottom, left)])
        if not face_encodings:
            continue

        face_encoding = face_encodings[0]
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        print(f"Matches: {matches}, Distances: {face_distances}")

        if True in matches:
            best_match_index = np.argmin(face_distances)
            name = known_face_names[best_match_index]
            info_path = os.path.join(PERSON_INFO_DIR, f"{name}.txt")
            person_info = open(info_path).read().strip() if os.path.exists(info_path) else "No info available."
            return name, person_info

    return None, None