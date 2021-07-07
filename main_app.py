import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from keypoint_front import CalculateKeypointsFront, CalculateKeypointsSide

from PyQt5.QtGui import QPixmap
from clsCamera import CameraStream, CameraCapture
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import cv2

import ui.main_ui as ui

class MainApp(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        # self.cam_front.setCamera("rtsp://192.168.1.103:8554/live")
        # self.cam_front.setCamera(0)

        # Stream Front
        # ====================================================================
        self.cam_front = CameraStream(self)
        self.cam_front.set_name_of_camera("front")
        # self.cam_front.setCamera("rtsp://admin:0R4150ml38u@192.168.1.64/live")
        self.cam_front.setCamera("rtsp://192.168.88.31:8554/live")
        # self.cam_front.setCamera("images\\face4.jpg")
        self.cam_front.changePixmap.connect(self.set_stream_cam_front)
        self.cam_front.start()

        # Stream Side
        # ====================================================================
        self.cam_side = CameraStream(self)
        self.cam_side.set_name_of_camera("side")
        # self.cam_side.setCamera("rtsp://admin:0R4150ml38u@192.168.88.64/live")
        self.cam_side.setCamera("rtsp://192.168.88.31:8554/live")
        # self.cam_side.setCamera("images\\face4.jpg")
        self.cam_side.changePixmap.connect(self.set_stream_cam_side)
        self.cam_side.start()
        
        self.btn_capture_front.clicked.connect(self.capture_front)
        self.btn_capture_side.clicked.connect(self.capture_side)
        self.btn_calculate.clicked.connect(self.image_calculate)

        self.show()
    
    def set_stream_cam_front(self, image):
        self.lbl_cam_front.setPixmap(QPixmap.fromImage(image))

    def set_stream_cam_side(self, image):
        self.lbl_cam_side.setPixmap(QPixmap.fromImage(image))

    # Capture Front
    def capture_front(self):
        self.cam_front.capture()
        self.sc_front = CameraCapture(self)
        self.sc_front.set_image("temp_images\capture_cam_front.png")
        self.sc_front.changePixmap.connect(self.set_image_front)
        self.sc_front.start()

    def set_image_front(self, image):
        self.cam_front.terminate()
        self.lbl_cam_front.setPixmap(QPixmap.fromImage(image))
    
    # Capture Side
    def capture_side(self):
        self.cam_side.capture()
        self.sc_side = CameraCapture(self)
        self.sc_side.set_image("temp_images\capture_cam_side.png")
        self.sc_side.changePixmap.connect(self.set_image_side)
        self.sc_side.start()

    def set_image_side(self, image):
        self.cam_side.terminate()
        self.lbl_cam_side.setPixmap(QPixmap.fromImage(image))

    def image_calculate(self):
        image_obj_front = CalculateKeypointsFront()
        image_obj_front.set_pic(self.sc_front.image_capture)
        results_front = image_obj_front.calculate_image()
        print(results_front)

        image_obj_side = CalculateKeypointsSide()
        image_obj_side.set_pic(self.sc_side.image_capture)
        image_obj_side.calculate_image()
        

        self.imgCv_front = cv2.imread("results\\temp_front.png")
        self.imgCv_front = cv2.resize(self.imgCv_front, (420,335))
        self.imgRGB_front = cv2.cvtColor(self.imgCv_front, cv2.COLOR_BGR2RGB)
        qimg_front = QtGui.QImage(self.imgRGB_front.data, self.imgRGB_front.shape[1],self.imgRGB_front.shape[0], QtGui.QImage.Format_RGB888)
        p_front = qimg_front.scaled(580, 657, Qt.KeepAspectRatio)
        self.lbl_cam_front.setPixmap(QPixmap.fromImage(p_front))

        self.imgCv_side = cv2.imread("results\\temp_side.png")
        self.imgCv_side = cv2.resize(self.imgCv_side, (420,335))
        self.imgRGB_side = cv2.cvtColor(self.imgCv_side, cv2.COLOR_BGR2RGB)
        qimg_side = QtGui.QImage(self.imgRGB_side.data, self.imgRGB_side.shape[1],self.imgRGB_side.shape[0], QtGui.QImage.Format_RGB888)
        p_side = qimg_side.scaled(580, 657, Qt.KeepAspectRatio)
        self.lbl_cam_side.setPixmap(QPixmap.fromImage(p_side))

def main():
    app = QApplication(sys.argv)
    form = MainApp()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()