import requests
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QButtonGroup
from deskop_app.system_app_config import url
from deskop_app.ui.generated_code.aptitude_quiz import Ui_MainWindow


class AptitudeQuizWindow(QMainWindow, Ui_MainWindow):
    load_personality_test_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.user_id = None
        self.setupUi(self)
        self.setWindowTitle("Aptitude Quiz")
        self.count = 0
        self.time = 3600
        self.aptitude_score = 0

        self.label_3.setText(self.user_id)
        self.cursor = requests.get(f"{url}/get_aptitude_questions").json()
        self.responses = dict()
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.radioButton_1)
        self.btn_group.addButton(self.radioButton_2)
        self.btn_group.addButton(self.radioButton_3)
        self.btn_group.addButton(self.radioButton_4)
        self.prevButton.hide()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_timer)
        self.radioButton_1.clicked.connect(lambda: self.option_choice(1))
        self.radioButton_2.clicked.connect(lambda: self.option_choice(2))
        self.radioButton_3.clicked.connect(lambda: self.option_choice(3))
        self.radioButton_4.clicked.connect(lambda: self.option_choice(4))
        self.nextButton.clicked.connect(self.display_next_question)
        self.prevButton.clicked.connect(self.display_previous_question)
        self.display_next_question()
        self.timer.start(1000)

    def set_candidate_name(self, user_id):
        self.user_id = user_id

    def show_timer(self):
        if self.time > 0:
            self.time -= 1
            self.lineEdit_2.setText(str(self.time // 60) + "." + str(self.time % 60))
        else:
            self.report_score()

    def display_next_question(self):
        score_reported = False

        if self.count == 1:
            self.prevButton.show()
        elif self.count == len(self.cursor) - 1:
            self.nextButton.setText("Submit and proceed to personality test")
        elif self.count == len(self.cursor):
            self.report_score()
            score_reported = True

        if not score_reported:
            self.question.setText(self.cursor[self.count]["question"])

            for index, radio_button in enumerate(self.btn_group.buttons()):
                radio_button.setText(self.cursor[self.count][f"option_{index + 1}"])

            self.count += 1
            self.uncheck()

    def display_previous_question(self):
        if self.count == 2:
            self.prevButton.hide()
        elif self.count == len(self.cursor):
            self.nextButton.setText("Next")
        self.count -= 1
        self.question.setText(self.cursor[self.count]["question"])
        self.radioButton_1.setText(self.cursor[self.count]["option_1"])
        self.radioButton_2.setText(self.cursor[self.count]["option_2"])
        self.radioButton_3.setText(self.cursor[self.count]["option_3"])
        self.radioButton_4.setText(self.cursor[self.count]["option_4"])
        self.uncheck()

    def uncheck(self):
        if self.btn_group.checkedButton():
            self.btn_group.setExclusive(False)
            self.btn_group.checkedButton().setChecked(False)
            self.btn_group.setExclusive(True)

    def option_choice(self, choice):
        if self.cursor[self.count - 1]["correct_option"] == f"option_{choice}":
            self.aptitude_score += 5
        else:
            self.aptitude_score -= 1

    def report_score(self):
        try:
            _ = requests.get(
                f"{url}/report_score",
                json={
                    "_id": self.user_id,
                    "type": "aptitude",
                    "score": self.aptitude_score,
                    "cursor_len": len(self.cursor),
                },
            )
            self.load_personality_test_signal.emit(self.user_id)
        except:
            pass
