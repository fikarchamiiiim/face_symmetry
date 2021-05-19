import cv2
import dlib
from imutils import face_utils, resize
import numpy as np
import math

model_path = 'shape_predictor_68_face_landmarks.dat'
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)


def get_head_mask(img):
    """
    Find face in pic and remove background
    :param img:
    :return:
    """
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))    # Find faces
    if len(faces) != 0:
        x, y, w, h = faces[0]
        (x, y, w, h) = (x - 40, y - 100, w + 80, h + 200)
        rect1 = (x, y, w, h)
        cv2.grabCut(img, mask, rect1, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)     #Crop BG around the head
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # Take the mask from BG

    return mask2, faces

#############################
file_name="images/face4.jpg"

img1 = cv2.imread(file_name)     # Load image
img1 = resize(img1, height=500)  # We result in 500px in height
mask, faces = get_head_mask(img1)    # We get the mask of the head (without BG)

# Find the contours, take the largest one and memorize its upper point as the top of the head
cnts = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

face_x, face_y, face_w, face_h = faces[0]
print(face_x, face_y, face_w, face_h)

cnts_x = []
cnts_y = []
for i in range(len(cnts[0])):
    x, y = cnts[0][i][0]
    cnts_x.append(x)
    cnts_y.append(y)


# Plot head contours
# cv2.drawContours(img1, [cnts[0]], -1, (0, 0, 255), 2)

# Find main facial keypoints
face_detector = dlib.get_frontal_face_detector()
facial_landmark_predictor = dlib.shape_predictor(model_path)

# convert to grayscale
grayImage = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
faces = face_detector(grayImage, 1)

# for all faces detect facial keypoints (if on pic will be one person - use without loop)
for (i, face) in enumerate(faces):

    facial_landmarks = facial_landmark_predictor(grayImage, face)
    facial_landmarks = face_utils.shape_to_np(facial_landmarks)

    upper_nose_x, upper_nose_y = facial_landmarks[28-1]

    # cv2.rectangle(img1, (0, upper_nose_y-20), ())

    # plot facial keypoints if needed
    # for (i, (x, y)) in enumerate(facial_landmarks):
    #     cv2.circle(img1, (x, y), 1, (0, 0, 255), -1)
    #     cv2.putText(img1, str(i + 1), (x - 10, y - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # # find right ear
    # coor_right_ear_x, coor_right_ear_y = facial_landmarks[1-1][0], facial_landmarks[1-1][1]
   
    # for i in range(len(cnts_y)):
    #     if coor_right_ear_y in cnts_y:
    #         idx_coor_ear_r_y = [i for i, e in enumerate(cnts_y) if e == coor_right_ear_y]
    #     else:
    #         coor_right_ear_y -= 1
    
    # coor_right_ear_x = cnts_x[idx_coor_ear_r_y[0]] - 2
    # coor_right_ear_y = cnts_y[idx_coor_ear_r_y[0]]

    # # find left ear
    # coor_left_ear_x, coor_left_ear_y = facial_landmarks[17-1][0], facial_landmarks[17-1][1]

    # for i in range(len(cnts_y)):
    #     if coor_left_ear_y in cnts_y:
    #         idx_coor_ear_l_y = [i for i, e in enumerate(cnts_y) if e == coor_left_ear_y]
    #     else:
    #         coor_left_ear_y -= 1

    # coor_left_ear_x = cnts_x[idx_coor_ear_l_y[1]] + 2
    # coor_left_ear_y = cnts_y[idx_coor_ear_l_y[1]]

    # for i in range(len(cnts_x)):
    #     cv2.circle(img1, (cnts_x[i], cnts_y[i]), 2, (0,255,0), 2)

    # Vertical Lines
    for i in [37, 40, 43, 46]:
        cv2.line(img1, (facial_landmarks[i-1][0], face_y),(facial_landmarks[i-1][0], face_y+face_h), (0, 0, 0), 1)
    
    # Horizontal Lines
    for i in [22, 34]:
        cv2. line(img1, (face_x, facial_landmarks[i-1][1]), (face_x+face_w, facial_landmarks[i-1][1]), (0, 0, 0), 1)

    cv2.rectangle(img1, (face_x, face_y), (face_x+face_w, face_y+face_h), (0,255,0), 1)

    # cv2.circle(img1, (coor_right_ear_x, coor_right_ear_y), 2, (0,255,0), 2)
    # cv2.circle(img1, (coor_left_ear_x,coor_left_ear_y), 2, (0,255,0), 2)    

while True:
    cv2.imshow("image1", img1)
    if cv2.waitKey(5) == 27:
        break