from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from deskop_app.ui.generated_code.splash_screen import Ui_splashScreen


class SplashScreen(QtWidgets.QMainWindow, Ui_splashScreen):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 225, 225, 100))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.counter = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)
        self.softwareDescription.setText("Welcome")
        QtCore.QTimer.singleShot(
            3000, lambda: self.softwareDescription.setText("Hire candidates easily")
        )

    def progress(self):
        self.progressBar.setValue(self.counter)
        if self.counter > 100:
            self.timer.stop()
            self.close()
        self.counter += 1
