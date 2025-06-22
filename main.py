from functools import partial
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import time, datetime, cv2, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from pathlib import Path

class login(QWidget):
    def __init__(self):
        super(login, self).__init__()
        # importando archivo .ui
        uic.loadUi("./templates/Login-form.ui", self)
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
        if user == "user" and pswrd == "password":
            self.close()
            self.window = mainmenu()
            self.window.show()

        elif len(user) == 0 and len(pswrd) == 0:
            self.label_WrongUser.clear()
            self.label_WrongPswd.clear()
            self.label_WrongUser.setText("Introduzca un usuario")
            self.label_WrongPswd.setText("Introduzca una contraseña")
        elif user == "user" and pswrd != "password":
            self.label_WrongPswd.setText("Contraseña incorrecta")
            self.line_user.clear()
            self.line_password.clear()
        elif user != "user" and pswrd == "password":
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
        uic.loadUi("./templates/videoReader.ui", self)
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
        ruta_predeterminada = str(Path.home() / "Videos" / "AUVIS")
        path, _ = QFileDialog.getOpenFileName(self, "Abrir video", ruta_predeterminada, "Videos (*.avi *.mp4 *.mov)")
        if not path:
            return
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.mediaPlayer.play()

    def volver(self):
        self.close()


class mainmenu(QWidget):
    def __init__(self):
        super(mainmenu, self).__init__()
        uic.loadUi("./templates/mainmenu-form.ui", self)
        self.setWindowTitle("AUVIS")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.lbl_led.raise_()
        self.lbl_led.setVisible(True)

        # Botones
        self.btn_salirm.clicked.connect(self.close_app)
        self.btn_cerrarSesion.clicked.connect(self.logOut)
        self.btn_ayudam.clicked.connect(self.abrirAyuda)
        self.btn_grabar.clicked.connect(self.video)
        self.btn_detener.clicked.connect(self.detener)
        self.btn_grabaciones.clicked.connect(self.xplorer)

        self.hilo = None

        self.loading_label = QLabel("Inicializando cámara...", self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("background-color: white; font-size: 16px;")
        self.loading_label.hide()

    def close_app(self):
        if hasattr(self, 'hilo') and self.hilo is not None:
            self.hilo.stop()
            self.hilo.wait() 

        self.close()  
        QApplication.quit()  


    def update_led(self, color):
        colors = {
            "red": "background-color: red; border-radius: 10px;",
            "yellow": "background-color: yellow; border-radius: 10px;",
            "green": "background-color: green; border-radius: 10px;",
            "blue": "background-color: blue; border-radius: 10px;"
        }
        self.lbl_led.setStyleSheet(colors.get(color, "red"))

    def on_detection_change(self, detected):
        if detected == "blue":
            self.update_led("blue")
        elif detected == "green":
            self.update_led("green")

    def on_camera_ready(self):
        self.update_led("yellow")
        self.loading_label.hide()
        self.btn_grabar.setEnabled(True)
        print("Cámara lista - Grabando...")

    def check_camera_timeout(self):
        if not hasattr(self, 'hilo') or not self.hilo.isRunning():
            self.loading_label.setText("Error: No se pudo iniciar la cámara")
            self.btn_grabar.setEnabled(True)
            QTimer.singleShot(3000, lambda: self.loading_label.hide())

    def video(self):
        self.update_led("yellow")
        if hasattr(self, 'hilo') and self.hilo is not None and self.hilo.isRunning():
            return

        self.btn_grabar.setEnabled(False)
        self.loading_label.show()

        self.hilo = hilo()
        self.hilo.Imageupd.connect(self.frameimg)
        self.hilo.started.connect(self.on_camera_ready)
        self.hilo.EstadoLedSignal.connect(self.on_detection_change)
        self.hilo.finished.connect(lambda: self.update_led("red"))  # 🔴 LED al finalizar
        self.hilo.start()

        QTimer.singleShot(15000, self.check_camera_timeout)

    def detener(self):
        if hasattr(self, 'hilo') and self.hilo is not None:
            self.hilo.stop()
            self.label.clear()
            self.btn_grabar.setEnabled(True)

    def logOut(self):
        self.close()
        self.window = login()
        self.window.show()

    def abrirAyuda(self):
        self.window = menuAyuda()
        self.window.show()

    def xplorer(self):
        self.window = videorec()
        self.window.show()

    def frameimg(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))
            
class menuAyuda(QWidget):
    def __init__(self):
        super(menuAyuda, self).__init__()
        # importando archivo .ui
        uic.loadUi("./templates/menu-ayuda.ui", self)
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
        uic.loadUi("./templates/acerca-de.ui", self)
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
        uic.loadUi("./templates/ayuda-inicio-sesion.ui", self)
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
        uic.loadUi("./templates/ayuda-ventana-principal.ui", self)
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
        uic.loadUi("./templates/ayuda-grabaciones.ui", self)
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
    EstadoLedSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.hilo_corriendo = False
        self.cap = None
        self.out = None
        self.grabar = False

    def run(self):
        self.hilo_corriendo = True
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.EstadoLedSignal.emit("red")
            return

        self.EstadoLedSignal.emit("yellow")

        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        faces_casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        bodies_casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

        deteccion_tiempo_detenido = None
        inicio_timer = False
        SEGUNDOS_DESPUES_DETECTADO = 3

        try:
            while self.hilo_corriendo:
                ret, frame = self.cap.read()
                if not ret:
                    self.EstadoLedSignal.emit("red")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(rgb_image, 1)
                qt_image = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
                pic = qt_image.scaled(744, 500, Qt.KeepAspectRatio)

                cara = faces_casc.detectMultiScale(gray, 1.3, 5)
                cuerpo = bodies_casc.detectMultiScale(gray, 1.3, 5)
                deteccion_activa = len(cara) + len(cuerpo) > 0

                if deteccion_activa:
                    if not self.grabar:
                        self.grabar = True
                        tiempo_Actual = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

                        # Crear carpeta AUVIS dentro de Videos del usuario
                        
                        video_dir = Path.home() / "Videos" / "AUVIS"
                        video_dir.mkdir(parents=True, exist_ok=True)

                        # Ruta final del archivo de video
                        video_path = video_dir / f"{tiempo_Actual}.avi"

                        # Crear objeto de escritura de video
                        self.out = cv2.VideoWriter(str(video_path), fourcc, 20, frame_size)
                        print(f"Inicio de grabación (detección) en: {video_path}")

                    self.EstadoLedSignal.emit("blue")
                    inicio_timer = False
                elif self.grabar:
                    if inicio_timer:
                        if time.time() - deteccion_tiempo_detenido >= SEGUNDOS_DESPUES_DETECTADO:
                            self.grabar = False
                            inicio_timer = False
                            if self.out is not None:
                                self.out.release()
                                self.out = None
                            print("Grabación detenida (fin detección)")
                            self.EstadoLedSignal.emit("green")
                    else:
                        inicio_timer = True
                        deteccion_tiempo_detenido = time.time()

                if self.grabar and self.out is not None:
                    self.out.write(frame)

                self.Imageupd.emit(pic)

                if cv2.waitKey(1) == ord('q'):
                    break

        except Exception as e:
            print(f"Error en el hilo: {e}")
            self.EstadoLedSignal.emit("red")
        finally:
            self.liberar_recursos()

    def liberar_recursos(self):
        if self.out is not None:
            self.out.release()
            self.out = None
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.EstadoLedSignal.emit("red")


    def stop(self):
        self.hilo_corriendo = False
        self.wait()  

#**************************************************************************



# inicializando la ventana
app = QApplication(sys.argv)

app.setWindowIcon(QIcon("tvision.png"))

window = login()
app.exec_()
