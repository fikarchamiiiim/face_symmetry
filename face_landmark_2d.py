import cv2
import face_alignment
from skimage import io

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False)

input = io.imread('images\\from_side3.jpg')
preds = fa.get_landmarks(input)
# print(preds)

image_color = cv2.cvtColor(input, cv2.COLOR_RGB2BGR)

for i, coor in enumerate(preds[0]):
    cv2.circle(image_color, tuple(coor), 1, (0, 255, 0), 1)
    cv2.putText(image_color, str(i), tuple(coor), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
while True:
    cv2.imshow("image1", image_color)
    if cv2.waitKey(5) == 27:
        break