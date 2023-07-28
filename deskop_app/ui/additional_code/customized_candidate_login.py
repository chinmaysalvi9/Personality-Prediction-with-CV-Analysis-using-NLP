import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from deskop_app.ui.generated_code.candidate_login import Ui_Dialog
from deskop_app.system_app_config import url


class CandidateLogin(QDialog, Ui_Dialog):
    successful_login = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Quick Hire Candidate Login")
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        self.invalidEmailLabel.setText("")
        self.invalidPasswordLabel.setText("")

        try:
            response = requests.get(
                f"{url}/verify_user",
                json={
                    "email_id": self.emailIdInput.text(),
                    "pass": self.passwordInput.text(),
                    "is_candidate": True,
                },
            )

            if response.status_code != 200 or response.text == "Error":
                raise Exception

            if response.text == "None":
                self.invalidEmailLabel.setText("Please enter valid email")
            elif response.text == "True":
                self.loginAckLabel.setText("Login Successful")
                self.passwordInput.clear()
                self.successful_login.emit(self.emailIdInput.text())
            else:
                self.invalidPasswordLabel.setText("Please enter valid password")

        except:
            self.loginAckLabel.setText(
                "Please check your internet connection and Try Again."
            )
            self.loginAckLabel.setWordWrap(True)
