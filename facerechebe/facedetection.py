import cv2
import mediapipe as mp
import face_recognition
import numpy as np
import os

known_face_encodings = []
known_face_names = []

known_dir = "known_people"

for filename in os.listdir(known_dir):
    path = os.path.join(known_dir, filename)
    if not os.path.isfile(path):
        continue

    img = face_recognition.load_image_file(path)
    encodings = face_recognition.face_encodings(img)

    if len(encodings) > 0:
        known_face_encodings.append(encodings[0])
        name = os.path.splitext(filename)[0]
        known_face_names.append(name)
        print(f"Loaded encoding for {name}")
    else:
        print(f"No faces found in {filename}")

mp_face_detection = mp.solutions.face_detection
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.8) as face_detection:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        ih, iw, _ = frame.shape
        cx, cy = iw // 2, ih // 2   
        radius = 100                 


        cv2.circle(frame, (cx, cy), radius, (0, 255, 0), 2)


        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                face_center_x = x + w // 2
                face_center_y = y + h // 2


                distance = np.sqrt((face_center_x - cx)**2 + (face_center_y - cy)**2)
                if distance > radius:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)
                    cv2.putText(frame, "Fuera del circulo", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
                    continue


                top, right, bottom, left = y, x + w, y + h, x

                top = max(0, top)
                left = max(0, left)
                bottom = min(ih, bottom)
                right = min(iw, right)


                face_encodings = face_recognition.face_encodings(
                    rgb_frame, [(top, right, bottom, left)]
                )
                name = "Unknown"
                if face_encodings:
                    face_encoding = face_encodings[0]
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding, tolerance=0.5
                    )
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding
                    )

                    if True in matches:
                        best_match_index = np.argmin(face_distances)
                        name = known_face_names[best_match_index]

                        info_dir = "person_info"
                        info_path = os.path.join(info_dir, f"{name}.txt")

                        if os.path.exists(info_path):
                            with open(info_path, "r", encoding="utf-8") as f:
                                person_info = f.read().strip()
                        else:
                            person_info = "No info available."
                    else:
                        person_info = "Unknown person"


                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, person_info, (left, bottom + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


        cv2.imshow("Face Recognition (Circle Zone)", frame)


        if cv2.waitKey(5) & 0xFF == ord("q"):
            break


cap.release()
cv2.destroyAllWindows()
