from PyQt5 import QtGui
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2

class CameraStream(QThread):
        
    changePixmap = pyqtSignal(QImage)

    def setCamera(self, url):
        self.number_of_cam = url
    
    def set_name_of_camera(self, cam_name):
        self.name_of_cam = cam_name

    def run(self):
        # Stream From Camera
        # ==================================================================
        self.cap = cv2.VideoCapture(self.number_of_cam)
        while True:
            self.ret, self.frame = self.cap.read()
            if self.ret:
                # https://stackoverflow.com/a/55468544/6622587
                self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                h, w, ch = self.rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(self.rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(580, 657, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        # (Developing) Stream From Image
        # ==================================================================
        # self.imgCv = cv2.imread(self.number_of_cam)
        # self.imgCv = cv2.resize(self.imgCv, (420,335))
        # self.imgRGB = cv2.cvtColor(self.imgCv, cv2.COLOR_BGR2RGB)
        # qimg = QtGui.QImage(self.imgRGB.data, self.imgRGB.shape[1],self.imgRGB.shape[0], QtGui.QImage.Format_RGB888)
        # p = qimg.scaled(580, 657)
        # self.changePixmap.emit(p)

    def capture(self):
        cv2.imwrite(f"temp_images\capture_cam_{self.name_of_cam}.png", self.frame)
        # cv2.imwrite(f"temp_images\capture_cam_{self.name_of_cam}.png", self.imgCv)
        print(f"oke cam {self.name_of_cam}")

class CameraCapture(QThread):

    changePixmap = pyqtSignal(QImage)

    def set_image(self, image):
        self.image_capture = image

    def run(self):
        imgCv = cv2.imread(self.image_capture)
        imgCv = cv2.resize(imgCv, (420,335))
        self.imgRGB = cv2.cvtColor(imgCv, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(self.imgRGB.data, self.imgRGB.shape[1],self.imgRGB.shape[0], QtGui.QImage.Format_RGB888)
        p = qimg.scaled(580, 657, Qt.KeepAspectRatio)
        self.changePixmap.emit(p)
    
    def drawing_cam(self,num_cam, x, y):
        global coordinate_1, coordinate_2

        p = QtGui.QImage(self.imgRGB.data, self.imgRGB.shape[1],self.imgRGB.shape[0], QtGui.QImage.Format_RGB888)
        self.changePixmap.emit(p)