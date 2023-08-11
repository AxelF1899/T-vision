from functools import partial

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import time, datetime, cv2, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class login(QWidget):
    def __init__(self):
        super(login, self).__init__()
        # importando archivo .ui
        uic.loadUi("Login-form.ui", self)
        # *******************************Configurar ventana***********************************************
        self.setWindowTitle("Inicio de sesión")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()

        # agrgando funcionalidad a los botones
        self.btn_salir.clicked.connect(lambda: self.close())
        self.btn_login.clicked.connect(self.entrar)
        self.btn_ayuda.clicked.connect(self.helpmenu)

    # creando funciones
    def helpmenu(self):
        self.window = menuAyuda()
        self.window.show()

    def entrar(self):
        user = self.line_user.text()
        pswrd = self.line_password.text()
        if user == "Mirella" and pswrd == "12345":
            self.close()
            self.window = mainmenu()
            self.window.show()

        elif len(user) == 0 and len(pswrd) == 0:
            self.label_WrongUser.clear()
            self.label_WrongPswd.clear()
        elif user == "Mirella" and pswrd != "12345":
            self.label_WrongPswd.setText("Contraseña incorrecta")
            self.line_user.clear()
            self.line_password.clear()
        elif user != "Mirella" and pswrd == "12345":
            self.label_WrongUser.setText("Usuario incorrecto")
            self.line_user.clear()
            self.line_password.clear()
        else:
            self.label_WrongUser.setText("Usuario incorrecto")
            self.label_WrongPswd.setText("Contraseña incorrecta")
            self.line_user.clear()
            self.line_password.clear()

class videorec(QWidget):
    def __init__(self):
        super(videorec, self).__init__()
        uic.loadUi("videoReader.ui", self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
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


class mainmenu(QWidget):
    def __init__(self):
        super(mainmenu, self).__init__()
        # importando archivo .ui
        uic.loadUi("mainmenu-form.ui", self)
        self.setWindowTitle("T-Vision")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # agrgando funcionalidad a los botones
        self.btn_salirm.clicked.connect(lambda: self.close())
        self.btn_cerrarSesion.clicked.connect(self.logOut)
        self.btn_ayudam.clicked.connect(self.abrirAyuda)
        self.btn_grabar.clicked.connect(self.video)
        self.btn_detener.clicked.connect(self.detener)
        self.btn_grabaciones.clicked.connect(self.xplorer)

        # métodos
    def xplorer(self):
        self.window = videorec()
        self.window.show()

    def video(self):

        try:
            self.hilo = hilo()
            self.hilo.start()
            self.hilo.Imageupd.connect(self.frameimg)
        finally:
            print('grabando')

    def frameimg(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def detener(self):

        try:
            self.hilo.stop()
            self.label.clear()
        finally:
            print('Presione grabar video')

    def logOut(self):
        self.close()
        self.window = login()
        self.window.show()

    def abrirAyuda(self):
        self.window = menuAyuda()
        self.window.show()


class menuAyuda(QWidget):
    def __init__(self):
        super(menuAyuda, self).__init__()
        # importando archivo .ui
        uic.loadUi("menu-ayuda.ui", self)
        self.setWindowTitle("Ayuda")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_regresar_2.clicked.connect(self.backToLogin)
        self.pushButton_acercade_2.clicked.connect(self.acerca)
        self.pushButton_ayuda_2.clicked.connect(self.manualusuario)

    def backToLogin(self):
        self.close()

    def manualusuario(self):
        self.close()
        self.window = ManualUser1()
        self.window.show()

    def acerca(self):
        self.close()
        self.window = acercaDe()
        self.window.show()


class acercaDe(QWidget):
    def __init__(self):
        super(acercaDe, self).__init__()
        # importando archivo .ui
        uic.loadUi("acerca-de.ui", self)
        self.setWindowTitle("Acerca de")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_aceptar.clicked.connect(self.regresar)

    def regresar(self):
        self.close()
        self.window = menuAyuda()
        self.window.show()


class ManualUser1(QWidget):
    def __init__(self):
        super(ManualUser1, self).__init__()
        # importando archivo .ui
        uic.loadUi("ayuda-inicio-sesion.ui", self)
        self.setWindowTitle("Manual de usuario")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.btn_salirManual.clicked.connect(lambda: self.close())
        self.btn_siguiente.clicked.connect(self.next2)
        self.btn_anterior.clicked.connect(self.back3)

    def next2(self):
        self.close()
        self.window = ManualUser2()
        self.window.show()

    def back3(self):
        self.close()
        self.window = ManualUser3()
        self.window.show()


class ManualUser2(QWidget):
    def __init__(self):
        super(ManualUser2, self).__init__()
        # importando archivo .ui
        uic.loadUi("ayuda-ventana-principal.ui", self)
        self.setWindowTitle("Manual de usuario")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.btn_cerrarAyuda.clicked.connect(lambda: self.close())
        self.btn_siguiente2.clicked.connect(self.next3)
        self.btn_volver1.clicked.connect(self.back1)

    def back1(self):
        self.close()
        self.window = ManualUser1()
        self.window.show()

    def next3(self):
        self.close()
        self.window = ManualUser3()
        self.window.show()


class ManualUser3(QWidget):
    def __init__(self):
        super(ManualUser3, self).__init__()
        # importando archivo .ui
        uic.loadUi("ayuda-grabaciones.ui", self)
        self.setWindowTitle("Manual de usuario")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.btn_cerrarAyuda3.clicked.connect(lambda: self.close())
        self.btn_siguiente3.clicked.connect(self.next1)
        self.btn_anterior3.clicked.connect(self.back2)

    def back2(self):
        self.close()
        self.window = ManualUser2()
        self.window.show()

    def next1(self):
        self.close()
        self.window = ManualUser1()
        self.window.show()


class hilo(QThread):
    Imageupd = pyqtSignal(QImage)


    def run(self):
# ***********************   variables para la detección automática y ajuste del frame en qt
        cap = cv2.VideoCapture(0)
        grabar = False
        deteccion_tiempo_detenido = None
        inicio_timer = False
        SEGUNDOS_DESPUES_DETECTADO = 3
        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        frame_size = (int(cap.get(3)), int(cap.get(4)))

#**********************************************************
        self.hilo_corriendo = True

        faces_casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        bodies_casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
        while self.hilo_corriendo:
            ret, frame = cap.read()
#***************************************bloque de grabación automática y conversión al frame de qt

            Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            flip = cv2.flip(Image, 1)
            convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
            pic = convertir_QT.scaled(744, 500, Qt.KeepAspectRatio)


            cara = faces_casc.detectMultiScale(Image, 1.3, 5)
            cuerpo = bodies_casc.detectMultiScale(Image, 1.3, 5)


            if len(cara) + len(cuerpo) > 0:
                if grabar:
                    inicio_timer = False
                else:
                    grabar = True
                    tiempo_Actual = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                    out = cv2.VideoWriter(f"{tiempo_Actual}.avi", fourcc, 20, frame_size)

                    print("Inicio de la grabación")
            elif grabar:
                if inicio_timer:
                    if time.time() - deteccion_tiempo_detenido >= SEGUNDOS_DESPUES_DETECTADO:
                        grabar = False
                        inicio_timer = False
                        out.release()
                        print("Grabación detenida")
                else:
                    inicio_timer = True
                    deteccion_tiempo_detenido = time.time()

            if grabar:
                out.write(frame)
            if cv2.waitKey(1) == ord('q'):
                break


            self.Imageupd.emit(pic)

        out.release()
        cap.release()

    def stop(self):
        self.hilo_corriendo = False
        self.quit()
#**************************************************************************



# inicializando la ventana
app = QApplication(sys.argv)

app.setWindowIcon(QIcon("tvision.png"))

window = login()
app.exec_()
