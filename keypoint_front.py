import cv2
import dlib
import numpy as np
from imutils import resize, face_utils
import face_alignment
from skimage import io

class CalculateKeypointsFront:

    MODEL_PATH = 'shape_predictor_68_face_landmarks.dat'
    CASCADE_PATH = "haarcascade_frontalface_default.xml"
    FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)

    def set_pic(self, image_file):
        self.image_file = image_file

    def calculate_image(self):
        image = cv2.imread(self.image_file)     # Load image
        image = resize(image, height=500)  # We result in 500px in height
        mask, faces = self.get_head_mask(image)    # We get the mask of the head (without BG)

        # Find the contours, take the largest one and memorize its upper point as the top of the head
        cnts = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        face_x, face_y, face_w, face_h = faces[0]
        cnts_x = []
        cnts_y = []
        for i in range(len(cnts[0])):
            x, y = cnts[0][i][0]
            cnts_x.append(x)
            cnts_y.append(y)

        # Find main facial keypoints
        face_detector = dlib.get_frontal_face_detector()
        facial_landmark_predictor = dlib.shape_predictor(self.MODEL_PATH)

        # convert to grayscale
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_detector(grayImage, 1)

        # for all faces detect facial keypoints (if on pic will be one person - use without loop)
        for (i, face) in enumerate(faces):

            facial_landmarks = facial_landmark_predictor(grayImage, face)
            facial_landmarks = face_utils.shape_to_np(facial_landmarks)

            # Vertical Lines
            for i in [37, 40, 43, 46]:
                cv2.line(image, (facial_landmarks[i-1][0], face_y),(facial_landmarks[i-1][0], face_y+face_h), (0, 0, 0), 1)
            
            # Horizontal Lines
            for i in [22, 34]:
                cv2. line(image, (face_x, facial_landmarks[i-1][1]), (face_x+face_w, facial_landmarks[i-1][1]), (0, 0, 0), 1)

            cv2.rectangle(image, (face_x, face_y), (face_x+face_w, face_y+face_h), (0,255,0), 1)

            cv2.imwrite("results\\temp_front.png",image)

            results_coordinate = {
                1 : (face_x, face_y),
                2 : (facial_landmarks[37][0], face_y),
                3 : (facial_landmarks[40][0], face_y),
                4 : (facial_landmarks[43][0], face_y),
                5 : (facial_landmarks[46][0], face_y),
                6 : (face_x + face_w, face_y),
                7 : (face_x, facial_landmarks[22][1]),
                8 : (face_x, facial_landmarks[34][1]),
                9 : (face_x, face_y + face_h),
            }

        return results_coordinate

    def get_head_mask(self,img):
        """
        Find face in pic and remove background
        :param img:
        :return:
        """
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        faces = self.FACE_CASCADE.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))    # Find faces
        if len(faces) != 0:
            x, y, w, h = faces[0]
            (x, y, w, h) = (x - 40, y - 100, w + 80, h + 200)
            rect1 = (x, y, w, h)
            cv2.grabCut(img, mask, rect1, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)     #Crop BG around the head
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # Take the mask from BG

        return mask2, faces


class CalculateKeypointsSide():
    
    def set_pic(self, image_file):
        self.image = image_file

    def calculate_image(self):
        fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False)

        image = io.imread(self.image)
        preds = fa.get_landmarks(image)
        image_color = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for i, coor in enumerate(preds[0]):
            cv2.circle(image_color, tuple(coor), 1, (0, 255, 0), 1)
        
        cv2.imwrite("results\\temp_side.png",image_color)
