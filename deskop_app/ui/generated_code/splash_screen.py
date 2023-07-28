# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/designer_files/splashScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_splashScreen(object):
    def setupUi(self, splashScreen):
        splashScreen.setObjectName("splashScreen")
        splashScreen.resize(680, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(splashScreen.sizePolicy().hasHeightForWidth())
        splashScreen.setSizePolicy(sizePolicy)
        splashScreen.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(splashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("background-color: rgb(56, 58, 89);\n"
"color: rgb(220, 220, 220);\n"
"border-radius: 25px")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.softwareName = QtWidgets.QLabel(self.dropShadowFrame)
        self.softwareName.setGeometry(QtCore.QRect(0, 110, 661, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(40)
        self.softwareName.setFont(font)
        self.softwareName.setStyleSheet("color: rgb(0, 175, 175);")
        self.softwareName.setAlignment(QtCore.Qt.AlignCenter)
        self.softwareName.setObjectName("softwareName")
        self.softwareDescription = QtWidgets.QLabel(self.dropShadowFrame)
        self.softwareDescription.setGeometry(QtCore.QRect(0, 170, 661, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.softwareDescription.setFont(font)
        self.softwareDescription.setStyleSheet("color: rgb(255, 181, 61);")
        self.softwareDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.softwareDescription.setObjectName("softwareDescription")
        self.progressBar = QtWidgets.QProgressBar(self.dropShadowFrame)
        self.progressBar.setGeometry(QtCore.QRect(80, 260, 501, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(200, 200, 200);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.466, x2:1, y2:0.5, stop:0 rgba(202, 0, 0, 255), stop:1 rgba(255, 0, 127, 255));\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.loadingLabel = QtWidgets.QLabel(self.dropShadowFrame)
        self.loadingLabel.setGeometry(QtCore.QRect(0, 290, 661, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.loadingLabel.setFont(font)
        self.loadingLabel.setAutoFillBackground(False)
        self.loadingLabel.setStyleSheet("color: rgb(255, 181, 61);")
        self.loadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loadingLabel.setObjectName("loadingLabel")
        self.verticalLayout.addWidget(self.dropShadowFrame)
        splashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(splashScreen)
        QtCore.QMetaObject.connectSlotsByName(splashScreen)

    def retranslateUi(self, splashScreen):
        _translate = QtCore.QCoreApplication.translate
        splashScreen.setWindowTitle(_translate("splashScreen", "MainWindow"))
        self.softwareName.setText(_translate("splashScreen", "<html><head/><body><p><span style=\" font-weight:600;\">Quick </span>Hire</p></body></html>"))
        self.softwareDescription.setText(_translate("splashScreen", "<html><head/><body><p>Welcome</p></body></html>"))
        self.progressBar.setFormat(_translate("splashScreen", "%p%"))
        self.loadingLabel.setText(_translate("splashScreen", "<html><head/><body><p>loading....</p></body></html>"))