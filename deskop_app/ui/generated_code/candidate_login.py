# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/designer_files/candidateLogin.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 620)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Dialog.setStyleSheet("color: rgb(255, 255, 255); \n"
"background-color: #412A65;")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QFrame(Dialog)
        self.header.setMaximumSize(QtCore.QSize(16777215, 150))
        self.header.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.header.setFrameShadow(QtWidgets.QFrame.Plain)
        self.header.setObjectName("header")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.header)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 90, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.header)
        self.label.setStyleSheet("QLabel {\n"
"    font: 22pt \"Lucida Sans\";\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.verticalLayout.addWidget(self.header)
        self.body = QtWidgets.QFrame(Dialog)
        self.body.setStyleSheet("color: rgb(255,255,255);")
        self.body.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.body.setFrameShadow(QtWidgets.QFrame.Plain)
        self.body.setObjectName("body")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.body)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.body)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.candidateUILabel = QtWidgets.QLabel(self.frame_2)
        self.candidateUILabel.setStyleSheet("QLabel {\n"
"    font: 19pt \"Calibri\";\n"
"}")
        self.candidateUILabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.candidateUILabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.candidateUILabel.setAlignment(QtCore.Qt.AlignCenter)
        self.candidateUILabel.setObjectName("candidateUILabel")
        self.horizontalLayout.addWidget(self.candidateUILabel)
        self.adminUIButton = QtWidgets.QPushButton(self.frame_2)
        self.adminUIButton.setStyleSheet("QPushButton {\n"
"    border-radius: 10px;\n"
"    background-color: #27233A;\n"
"    padding: 15px 25px;\n"
"    border: none;\n"
"    font: 13pt \"Calibri\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(48, 43, 71);\n"
"    font: 13pt \"Calibri\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(56, 50, 80);\n"
"    font: 13pt \"Calibri\";\n"
"}")
        self.adminUIButton.setObjectName("adminUIButton")
        self.horizontalLayout.addWidget(self.adminUIButton)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.body)
        self.frame.setStyleSheet("QLineEdit {\n"
"    border-style: solid;\n"
"    border-color:rgb(255,255,255);\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(9, 9, 9, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.passwordInput = QtWidgets.QLineEdit(self.frame)
        self.passwordInput.setStyleSheet("")
        self.passwordInput.setObjectName("passwordInput")
        self.gridLayout.addWidget(self.passwordInput, 5, 1, 1, 1)
        self.invalidEmailLabel = QtWidgets.QLabel(self.frame)
        self.invalidEmailLabel.setStyleSheet("QLabel {\n"
"    font: 12pt \"Lucida Sans\";\n"
"    text-align: center;\n"
"}")
        self.invalidEmailLabel.setText("")
        self.invalidEmailLabel.setObjectName("invalidEmailLabel")
        self.gridLayout.addWidget(self.invalidEmailLabel, 0, 1, 1, 1)
        self.invalidPasswordLabel = QtWidgets.QLabel(self.frame)
        self.invalidPasswordLabel.setStyleSheet("QLabel {\n"
"    font: 12pt \"Lucida Sans\";\n"
"    text-align: center;\n"
"}")
        self.invalidPasswordLabel.setText("")
        self.invalidPasswordLabel.setObjectName("invalidPasswordLabel")
        self.gridLayout.addWidget(self.invalidPasswordLabel, 3, 1, 1, 1)
        self.emailIdLabel = QtWidgets.QLabel(self.frame)
        self.emailIdLabel.setStyleSheet("QLabel {\n"
"    font: 14pt \"Lucida Sans\";\n"
"    text-align: center;\n"
"}")
        self.emailIdLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.emailIdLabel.setObjectName("emailIdLabel")
        self.gridLayout.addWidget(self.emailIdLabel, 2, 0, 1, 1)
        self.emailIdInput = QtWidgets.QLineEdit(self.frame)
        self.emailIdInput.setStyleSheet("")
        self.emailIdInput.setObjectName("emailIdInput")
        self.gridLayout.addWidget(self.emailIdInput, 2, 1, 1, 1)
        self.passwordLabel = QtWidgets.QLabel(self.frame)
        self.passwordLabel.setStyleSheet("QLabel {\n"
"    font: 14pt \"Lucida Sans\";\n"
"    text-align: center;\n"
"}")
        self.passwordLabel.setObjectName("passwordLabel")
        self.gridLayout.addWidget(self.passwordLabel, 5, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_6 = QtWidgets.QFrame(self.body)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_6.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.loginButton = QtWidgets.QPushButton(self.frame_6)
        self.loginButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.loginButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.loginButton.setStyleSheet("QPushButton{\n"
"    background-color: #0BD5CB;\n"
"    font: 12pt \"Lucida Sans\";\n"
"    border-width: 2px;    \n"
"    border-color: #DBD9E8;\n"
"    border-style: solid;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    border-radius: 7px;\n"
"}")
        self.loginButton.setObjectName("loginButton")
        self.horizontalLayout_2.addWidget(self.loginButton)
        spacerItem2 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.loginAckLabel = QtWidgets.QLabel(self.body)
        self.loginAckLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.loginAckLabel.setStyleSheet("QLabel {\n"
"    font: 12pt \"Lucida Sans\";\n"
"    text-align: center;\n"
"}")
        self.loginAckLabel.setText("")
        self.loginAckLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loginAckLabel.setObjectName("loginAckLabel")
        self.verticalLayout_2.addWidget(self.loginAckLabel)
        self.verticalLayout.addWidget(self.body)
        self.footer = QtWidgets.QFrame(Dialog)
        self.footer.setMaximumSize(QtCore.QSize(16777215, 125))
        self.footer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.footer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.footer.setObjectName("footer")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout_3.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.createAccountLabel = QtWidgets.QLabel(self.footer)
        self.createAccountLabel.setStyleSheet("QLabel {\n"
"    font: 10pt \"Lucida Sans\";\n"
"    text-align: center;\n"
"}")
        self.createAccountLabel.setObjectName("createAccountLabel")
        self.horizontalLayout_3.addWidget(self.createAccountLabel)
        self.createAccountButton = QtWidgets.QPushButton(self.footer)
        self.createAccountButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.createAccountButton.setStyleSheet("QPushButton{\n"
"    color: rgb(0, 255, 0);\n"
"    font: 10pt \"Lucida Sans\";\n"
"    border-width: 2px;    \n"
"    border-color: #DBD9E8;\n"
"    border-style: groove;\n"
"    border-radius: 5px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}\n"
"\n"
"")
        self.createAccountButton.setObjectName("createAccountButton")
        self.horizontalLayout_3.addWidget(self.createAccountButton)
        self.verticalLayout.addWidget(self.footer)
        self.emailIdLabel.setBuddy(self.emailIdInput)
        self.passwordLabel.setBuddy(self.passwordInput)
        self.createAccountLabel.setBuddy(self.createAccountButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.emailIdInput, self.passwordInput)
        Dialog.setTabOrder(self.passwordInput, self.loginButton)
        Dialog.setTabOrder(self.loginButton, self.createAccountButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "LOGIN"))
        self.candidateUILabel.setText(_translate("Dialog", "Candidate"))
        self.adminUIButton.setText(_translate("Dialog", "Administrator"))
        self.emailIdLabel.setText(_translate("Dialog", "Email Id"))
        self.passwordLabel.setText(_translate("Dialog", "Password"))
        self.loginButton.setText(_translate("Dialog", "Login"))
        self.createAccountLabel.setText(_translate("Dialog", "Don\'t have an account ?"))
        self.createAccountButton.setText(_translate("Dialog", "Create account"))
