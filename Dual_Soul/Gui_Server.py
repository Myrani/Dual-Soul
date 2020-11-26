
import threading
import sys
import Server
import PyQt_Server_Worker
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Create the main Qt app, passing command line arguments



class ServerWindow(QMainWindow):
    def __init__(self):
        super(ServerWindow,self).__init__()
        self.setWindowTitle('Server')
        self.resize(400, 600)
        self.initServer()
        self.initUI()

    def initServer(self):
        self.threadpool = QThreadPool()
        self.server = Server.server()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def initUI(self):

        flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        self.setWindowFlags(flags)
        self.setWindowOpacity(0.6)
        self.blur_effect = QGraphicsBlurEffect()
        self.setStyleSheet( """QLabel {
        border: 5px solid black ;
        }""")


        #Background
        self.label_background = QLabel("transparent ",self)
        self.label_background.setGraphicsEffect(self.blur_effect)
        self.label_background.setGeometry(0,0,400,600)
        self.label_background.move(0,0)
        pixmap = QPixmap("Yuumi.jpg").scaled(self.size())
        self.label_background.setPixmap(pixmap)

        #Preference Menu

        self.label_menu = QLabel("transparent ",self.label_background)
        self.label_menu.setFixedSize(0,0)
        self.label_menu.move(0,0)
        self.label_menu.menu_preference = self.menuBar()
        self.label_menu.menu_preference.setFixedSize(130,25)
        self.label_menu.menu_preference.setStyleSheet( """
        QMenuBar {
        background-color: black;
        color:red;
        opacity:0.6;
        border: 1px solid;
        }
        QMenuBar::selected {
        background-color: black;
        color:white;
        border: 1px solid;

        }

        QMenuBar::item {
        background-color: black;
        color: white;

        }

        QMenuBar::item::selected {
        background-color: white;
        color: black;

        }

        QMenu {
        background-color:white;
        color:white;
        background:transparent;
        }
        QMenu::item {

        background-color:black;
        color:white;


        }
        QMenu::item::selected {
        background-color:white;
        color:black;

        }

        """)

        bar_des_menus = self.label_menu.menu_preference
        menu_settings = bar_des_menus.addMenu("Settings")

        menu_settings.addAction("Key Binding")
        menu_settings.addAction("Credits")

        menu_help =  bar_des_menus.addMenu("Help")
        menu_help.addAction("How to Set up")
        menu_help.addAction("Controls")

        #Start Button
        self.onoffbutton = QPushButton(self)
        self.onoffbutton.setText("Start")
        self.onoffbutton.clicked.connect(self.startstop)
        self.onoffbutton.setGeometry(50,500,80,30)

        self.quit = QPushButton(self)
        self.quit.setText("X")
        self.quit.clicked.connect(self.close)
        self.quit.setGeometry(360,20,20,20)

        self.label_serverstatus = QLabel(self)
        self.label_serverstatus.setStyleSheet("background-color: red")
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
            worker = PyQt_Server_Worker.Worker(self.server.start)
            self.threadpool.start(worker)
            self.label_serverstatus.setStyleSheet("background-color: green")



        else:
            self.onoffbutton.setText("Start")
            self.server.stop()
            self.threadpool.waitForDone(100)
            self.label_serverstatus.setStyleSheet("background-color: red")

    def hello(self,mot):
        time.sleep(10)
        print(mot)
        return None

def window():
    app = QApplication(sys.argv)
    win = ServerWindow()
    win.show()

    sys.exit(app.exec_())


#thread_gui = threading.Thread(target=window)
#thread_gui.start()
window()

# Run the app, passing it's exit code back through `sys.exit()`
# The app will exit when the close button is pressed on the main window.
