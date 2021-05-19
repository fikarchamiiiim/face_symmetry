import cv2
import dlib
from imutils import face_utils, resize
import numpy as np
import math

model_path = 'shape_predictor_68_face_landmarks.dat'
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def get_face(img):
    faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    face_x, face_y, face_w, face_h = faces[0]
    face = img[face_y:face_y+face_h, face_x:face_x+face_w]

    return face, faces[0]

file_name="images/face1_white.png"

img = cv2.imread(file_name)  # Load image
img = resize(img, height=500)  # We result in 500px in height
face, face_box = get_face(img)
img_gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
_, binary = cv2.threshold(img_gray, 225, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# img = cv2.drawContours(face, contours, -1, (0, 255, 0), 2)

face_detector = dlib.get_frontal_face_detector()
facial_landmark_predictor = dlib.shape_predictor(model_path)

faces = face_detector(img_gray, 1)

facial_landmarks = facial_landmark_predictor(img_gray, face)
facial_landmarks = face_utils.shape_to_np(facial_landmarks)

# plot facial keypoints if needed
for (i, (x, y)) in enumerate(facial_landmarks):
    cv2.circle(face, (x, y), 1, (0, 0, 255), -1)
    cv2.putText(face, str(i + 1), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

# cnts_x = []
# cnts_y = []
# for i in range(len(contours[0])):
#     x, y = contours[0][i][0]
#     cnts_x.append(x)
#     cnts_y.append(y)
    
# for i in range(len(contours[0])):
#     cv2.circle(face, (cnts_x[i], cnts_y[i]), 1, (0, 255, 0), 1)

# cnts = cv2.findContours(face, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

# cv2.drawContours(face, [cnts[0]], -1, (0, 0, 255), 2)


cv2.imshow("face", face)
cv2.waitKey(0)