import sys
from PyQt5.QtGui import QPixmap
from clsCamera import CameraStream
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import ui.main_ui as ui

class MainApp(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)

        self.cam1 = CameraStream(self)
        # self.cam1.setCamera("rtsp://192.168.1.151/?id=1&type=0")
        # self.cam1.setCamera("rtsp://192.168.1.102:8554/live")
        self.cam1.setCamera(0)
        self.cam1.setNameCam("X")
        self.cam1.changePixmap.connect(self.setStreamCam)
        self.cam1.start()
        self.show()
    
    def setStreamCam(self, image):
        self.lbl_cam.setPixmap(QPixmap.fromImage(image))

def main():
    app = QApplication(sys.argv)
    form = MainApp()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()