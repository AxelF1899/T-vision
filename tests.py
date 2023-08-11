import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
class mainWin(QWidget):
    def __init__(self):
        super(mainWin, self).__init__()
        uic.loadUi("videoReader.ui",self)
        self.setup()
        self.makeConnections()

    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()

    def makeMediaPlayer(self):
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer

    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.videoWidget.setLayout(vbox)
        return videoOutput

    def makeConnections(self):
        self.b_regresar.clicked.connect(self.volver)
        self.b_abrir.clicked.connect(self.onActionAbrirTriggered)
        self.b_reproducir.clicked.connect(self.mediaPlayer.play)
        self.b_pausa.clicked.connect(self.mediaPlayer.pause)
        self.b_detener.clicked.connect(self.mediaPlayer.stop)

    def onActionAbrirTriggered(self):
        path = QFileDialog.getOpenFileName(self, "Abrir video", r"C:\Users\BIENVENIDO\PycharmProjects\pythonProject"
                                           )
        filepath = path[0]
        if filepath == "":
            return
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()
    def volver(self):
        self.close()


if __name__ =="__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    w = mainWin()
    w.show()
    sys.exit(app.exec_())