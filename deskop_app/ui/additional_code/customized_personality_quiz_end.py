from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from deskop_app.ui.generated_code.personality_quiz_end import Ui_MainWindow


class PersonalityQuizEndWindow(QMainWindow, Ui_MainWindow):
    personality_test_end_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.user_id = None
        self.setupUi(self)

    def set_data(self, data):
        data = data.split('#')

        time = 720 - int(data[1])
        self.user_id = data[0]
        self.setWindowTitle("Personality Quiz")
        self.label_3.setText(
            "Your responses have been successfully submitted\nLoading Main Window"
        )
        self.lineEdit_2.setText(str(time // 60) + "." + str(time % 60))
        self.label_4.setText(self.user_id)
        self.showMaximized()
        QtCore.QTimer.singleShot(3000, lambda: self.personality_test_end_signal.emit(self.user_id))
