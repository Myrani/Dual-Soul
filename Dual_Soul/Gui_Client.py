
import threading
import sys
import Client
import PyQt_Server_Worker
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Create the main Qt app, passing command line arguments



class ClientWindow(QMainWindow):
    def __init__(self):
        super(ClientWindow,self).__init__()
        self.setWindowTitle('Client')
        self.resize(400, 600)
        self.initServer()
        self.initUI()

    def initServer(self):
        self.threadpool = QThreadPool()
        self.client = Client.Client()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def initUI(self):

        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WA_TranslucentBackground  )
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        #self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.setWindowOpacity(0.6)
        self.blur_effect = QGraphicsBlurEffect()


        self.label_background = QLabel("transparent ",self)
        self.label_background.setGraphicsEffect(self.blur_effect)
        self.label_background.setText("Bite")
        self.label_background.setGeometry(0,0,400,600)
        self.label_background.move(0,0)
        pixmap = QPixmap("Lucian.jpg").scaled(self.size())
        self.label_background.setPixmap(pixmap)


        self.quit = QPushButton(self)
        self.quit.setText("X")
        self.quit.clicked.connect(self.close)
        self.quit.setGeometry(360,20,20,20)


        self.onoffbutton = QPushButton(self)
        self.onoffbutton.setText("Start")
        self.onoffbutton.clicked.connect(self.startstop)
        self.onoffbutton.setGeometry(50,500,80,30)

        self.label_serverstatus = QLabel(self)
        self.label_serverstatus.setStyleSheet("background-color: red")
        #self.label_serverstatus.setGraphicsEffect(self.blur_effect)
        self.label_serverstatus.setGeometry(0,0,15,15)
        self.label_serverstatus.move(150,510)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()




    def startstop(self):
        if self.onoffbutton.text() == "Start":
            

            self.onoffbutton.setText("Stop")
            self.worker = PyQt_Server_Worker.Worker(self.client.start)
            self.threadpool.start(self.worker)
            self.label_serverstatus.setStyleSheet("background-color: green")


        else:
            self.onoffbutton.setText("Start")
            self.client.stop()
            self.threadpool.waitForDone(100)
            self.worker.quit()
            self.label_serverstatus.setStyleSheet("background-color: red")

    def hello(self,mot):
        time.sleep(10)
        print(mot)
        return None

def window():
    app = QApplication(sys.argv)
    win = ClientWindow()
    win.show()

    sys.exit(app.exec_())


#thread_gui = threading.Thread(target=window)
#thread_gui.start()
window()

# Run the app, passing it's exit code back through `sys.exit()`
# The app will exit when the close button is pressed on the main window.
