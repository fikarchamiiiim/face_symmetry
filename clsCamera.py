from PyQt5 import QtGui
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2

class CameraStream(QThread):
        
    changePixmap = pyqtSignal(QImage)

    def setNameCam(self, name):
        self.nameOfCam = name

    def setCamera(self, url):
        self.number_of_cam = url

    def run(self):
        self.cap = cv2.VideoCapture(self.number_of_cam)
        self.coordinate = (0,0)
        while True:
            self.ret, self.frame = self.cap.read()
            if self.ret:
                # https://stackoverflow.com/a/55468544/6622587
                self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                h, w, ch = self.rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(self.rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(501, 631)
                self.changePixmap.emit(p)
    
    def capture(self):
        cv2.imwrite(f"temp_images/capture_cam{self.nameOfCam}.png", self.frame)

class CameraCapture(QThread):

    changePixmap = pyqtSignal(QImage)

    def set_image(self, image):
        self.image_capture = image

    def run(self):
        imgCv = cv2.imread(self.image_capture)
        imgCv = cv2.resize(imgCv, (420,335))
        self.imgRGB = cv2.cvtColor(imgCv, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(self.imgRGB.data, self.imgRGB.shape[1],self.imgRGB.shape[0], QtGui.QImage.Format_RGB888)
        self.changePixmap.emit(qimg)

        # qimg = QtGui.QImage(self.imgRGB.data, self.imgRGB.shape[1],self.imgRGB.shape[0], QtGui.QImage.Format_RGB888)
        # self.changePixmap.emit(qimg)