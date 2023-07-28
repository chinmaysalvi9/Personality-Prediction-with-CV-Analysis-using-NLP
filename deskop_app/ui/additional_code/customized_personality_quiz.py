import requests
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QButtonGroup
from deskop_app.system_app_config import url
from deskop_app.ui.generated_code.personality_quiz import Ui_MainWindow


class PersonalityQuizWindow(QMainWindow, Ui_MainWindow):
    personality_test_end_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Personality Quiz")
        self.showMaximized()
        self.user_id = None
        self.count = 0
        self.time = 720
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_timer)
        self.label_3.setText(self.user_id)
        self.questions = requests.get(f"{url}/get_personality_questions").json()
        self.responses = dict()
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.radioButton_1)
        self.btn_group.addButton(self.radioButton_2)
        self.btn_group.addButton(self.radioButton_3)
        self.btn_group.addButton(self.radioButton_4)
        self.btn_group.addButton(self.radioButton_5)
        self.prevButton.hide()

        self.radioButton_1.clicked.connect(lambda: self.response(0))
        self.radioButton_2.clicked.connect(lambda: self.response(1))
        self.radioButton_3.clicked.connect(lambda: self.response(2))
        self.radioButton_4.clicked.connect(lambda: self.response(3))
        self.radioButton_5.clicked.connect(lambda: self.response(4))
        self.display_next_question()
        self.nextButton.clicked.connect(self.display_next_question)
        self.prevButton.clicked.connect(self.display_prev_question)

    def set_candidate_name(self, user_id):
        self.user_id = user_id
        self.timer.start(1000)

    def show_timer(self):
        if self.time > 0:
            self.time -= 1
            self.lineEdit_2.setText(str(self.time // 60) + "." + str(self.time % 60))
        else:
            self.compute_score()

    def display_next_question(self):
        computed_score = False

        if self.count == 1:
            self.prevButton.show()
        elif self.count == 49:
            self.nextButton.setText("Submit")
        elif self.count == 50:
            computed_score = True
            self.compute_score()

        if not computed_score:
            self.question.setText(self.questions[self.count]["question"])
            self.count += 1
            self.uncheck()

    def display_prev_question(self):
        if self.count == 2:
            self.prevButton.hide()
        elif self.count == 50:
            self.nextButton.setText("Next")
        self.count -= 1
        self.question.setText(self.questions[self.count]["question"])
        self.uncheck()

    def response(self, val):
        if val == 2 or bool(int(self.questions[self.count - 1]["ispositive"])):
            self.responses[self.questions[self.count - 1]["type"]] = 5 - val
        else:
            self.responses[self.questions[self.count - 1]["type"]] = 1 + val

    def uncheck(self):
        if self.btn_group.checkedButton():
            self.btn_group.setExclusive(False)
            self.btn_group.checkedButton().setChecked(False)
            self.btn_group.setExclusive(True)

    def compute_score(self):
        escore = nscore = ascore = cscore = oscore = 0

        for k, v in self.responses.items():
            if k.startswith("E"):
                escore += v
            elif k.startswith("N"):
                nscore += v
            elif k.startswith("A"):
                ascore += v
            elif k.startswith("C"):
                cscore += v
            else:
                oscore += v
        try:
            response = requests.get(
                f"{url}/report_score",
                json={
                    "_id": self.user_id,
                    "type": "personality",
                    "extraversion": escore / 5,
                    "neuroticism": nscore / 5,
                    "conscientiousness": cscore / 5,
                    "agreeableness": ascore / 5,
                    "openness": oscore / 5,
                },
            )
        except:
            pass

        self.personality_test_end_signal.emit(f"{self.user_id}#{self.time}")
