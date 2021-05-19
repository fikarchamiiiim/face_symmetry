# ===========================================
# Face Detection using Cascade Classifier
# ===========================================
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
mouth_cascade = cv2.CascadeClassifier("mouth.xml")
nose_cascade = cv2.CascadeClassifier("nose.xml")
img = cv2.imread('images/face1_portrait.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face = face_cascade.detectMultiScale(
    gray_img,
    scaleFactor = 1.3,
    minNeighbors = 10
)

eye = eye_cascade.detectMultiScale(
    gray_img,
    scaleFactor = 3,
    minNeighbors = 2
)

nose = nose_cascade.detectMultiScale(
    gray_img,
    scaleFactor = 1.2,
    minNeighbors = 5
)

print(face)
face_x = face[0][0]
face_y = face[0][1]
face_w = face[0][2]
face_h = face[0][3]

if eye[0][0] < eye[1][0]:
    eye_l_x = eye[0][0]
    eye_l_y = eye[0][1]
    eye_l_w = eye[0][2]
    eye_l_h = eye[0][3]

    eye_r_x = eye[1][0]
    eye_r_y = eye[1][1]
    eye_r_w = eye[1][2]
    eye_r_h = eye[1][3]
else:
    eye_r_x = eye[0][0]
    eye_r_y = eye[0][1]
    eye_r_w = eye[0][2]
    eye_r_h = eye[0][3]

    eye_l_x = eye[1][0]
    eye_l_y = eye[1][1]
    eye_l_w = eye[1][2]
    eye_l_h = eye[1][3]

nose_x = nose[0][0]
nose_y = nose[0][1]
nose_w = nose[0][2]
nose_h = nose[0][3]

# ===========================================
# menambahkan kotak deteksi di area face
# ===========================================

for x, y, w, h in face:
    img = cv2.rectangle(
        img,            # image object
        (x,y),          # posisi kotak
        (x+w, y+h),     # posisi kotak
        (0, 255, 0),    # warna kotak RGB
        2             # lebar garis kotak
    )

# for x, y, w, h in eye:
#     img = cv2.rectangle(
#         img,            # image object
#         (x,y),          # posisi kotak
#         (x+w, y+h),     # posisi kotak
#         (0, 255, 255),    # warna kotak RGB
#         2             # lebar garis kotak
#     )

# for x, y, w, h in nose:
#     img = cv2.rectangle(
#         img,            # image object
#         (x,y),          # posisi kotak
#         (x+w, y+h),     # posisi kotak
#         (255, 0, 0),    # warna kotak RGB
#         2             # lebar garis kotak
#     )

v_1_top = (eye_r_x + eye_r_w, face_y)
v_1_bottom = ((eye_r_x + eye_r_w), (face_y + face_h))

v_2_top = (eye_r_x, face_y)
v_2_bottom = (eye_r_x, (face_y + face_h))

v_3_top = (eye_l_x + eye_l_w, face_y)
v_3_bottom = ((eye_l_x + eye_l_w), (face_y + face_h))

v_4_top = (eye_l_x, face_y)
v_4_bottom = (eye_l_x, (face_y + face_h))

h_1_left = (face_x, nose_y + nose_h)
h_1_right = (face_x + face_w, nose_y + nose_h)

h_2_left = (face_x, eye_l_y)
h_2_right = (face_x + face_w, eye_l_y)

w_1 = face_x + face_w - v_1_top[0]
w_2 = v_1_top[0] - v_2_top[0]
w_3 = v_2_top[0] - v_3_top[0]
w_4 = v_3_top[0] - v_4_top[0]
w_5 = v_4_top[0] - face_x

h_1 = face_y + face_h - h_1_left[1]
h_2 = h_1_left[1] - h_2_left[1]
h_3 = h_2_left[1] - face_y


percent_w_1 = ((w_1 / face_w) * 100)
percent_w_2 = ((w_2 / face_w) * 100)
percent_w_3 = ((w_3 / face_w) * 100)
percent_w_4 = ((w_4 / face_w) * 100)
percent_w_5 = ((w_5 / face_w) * 100)

percent_h_1 = ((h_1 / face_h) * 100)
percent_h_2 = ((h_2 / face_h) * 100)
percent_h_3 = ((h_3 / face_h) * 100)


print(f"Persentase w_1: {percent_w_1} %")
print(f"Persentase w_2: {percent_w_2} %")
print(f"Persentase w_3: {percent_w_3} %")
print(f"Persentase w_4: {percent_w_4} %")
print(f"Persentase w_5: {percent_w_5} %")

print(f"Persentase h_1: {percent_h_1} %")
print(f"Persentase h_2: {percent_h_2} %")
print(f"Persentase h_3: {percent_h_3} %")

cv2.line(img, (v_1_top),(v_1_bottom), (20,20,20), 2)
cv2.line(img, (v_2_top),(v_2_bottom), (20,20,20), 2)
cv2.line(img, (v_3_top),(v_3_bottom), (20,20,20), 2)
cv2.line(img, (v_4_top),(v_4_bottom), (20,20,20), 2)

cv2.line(img, (h_1_left),(h_1_right), (20,20,20), 2)
cv2.line(img, (h_2_left),(h_2_right), (20,20,20), 2)

image = cv2.putText(img, "%.2f" % percent_w_1  + "%" , (face_x+face_w-50, face_y), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,255,255), 1, cv2.LINE_AA) 
image = cv2.putText(img, "%.2f" % percent_w_2  + "%" , (v_1_top[0]-50, face_y), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,255,255), 1, cv2.LINE_AA) 
image = cv2.putText(img, "%.2f" % percent_w_3  + "%" , (v_2_top[0]-50, face_y), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,255,255), 1, cv2.LINE_AA) 
image = cv2.putText(img, "%.2f" % percent_w_4  + "%" , (v_3_top[0]-50, face_y), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,255,255), 1, cv2.LINE_AA) 
image = cv2.putText(img, "%.2f" % percent_w_5  + "%" , (v_4_top[0]-50, face_y), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,255,255), 1, cv2.LINE_AA)

image = cv2.putText(img, "%.2f" % percent_h_1  + "%" , (face_x, face_y + face_h - 50), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,0,255), 1, cv2.LINE_AA)
image = cv2.putText(img, "%.2f" % percent_h_2  + "%" , (face_x, h_1_left[1] - 50), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,0,255), 1, cv2.LINE_AA)
image = cv2.putText(img, "%.2f" % percent_h_3  + "%" , (face_x, h_2_left[1] - 50), cv2.FONT_HERSHEY_SIMPLEX ,  0.5, (255,0,255), 1, cv2.LINE_AA)



resized = cv2.resize(img, (1280,720))
cv2.imshow('Gambar Output', img)
cv2.imwrite('tes1.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()