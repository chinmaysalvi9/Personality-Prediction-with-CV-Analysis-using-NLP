import requests
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QLabel
from deskop_app.system_app_config import url
from deskop_app.ui.generated_code.candidate_main_window import Ui_MainWindow


class CandidateMainWindow(QMainWindow, Ui_MainWindow):
    load_aptitude_test_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.user_id = None
        self.results = None
        self.setupUi(self)
        self.setWindowTitle("System")
        self.get_jobs()
        self.scrollArea.setWidgetResizable(True)
        self.label_8.setWordWrap(True)
        self.list_of_results = []
        self.view_candidate_result()

        self.actionApply.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.applyForNewJob)
        )
        self.actionGive_Test.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.giveTest)
        )
        self.actionView_Result.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.viewResult)
        )
        self.comboBox.currentTextChanged.connect(self.combo_box_change)
        self.ApplyForJobButton.clicked.connect(self.apply_job)
        self.startTestButton.clicked.connect(self.give_test)

    def set_candidate_name(self, candidate_name):
        self.user_id = candidate_name
        self.label.setText("Welcome" + self.user_id)
        self.label_3.wordWrap()
        self.label_3.setText("Instructions")

    def apply_job(self):
        try:
            application_status_check = requests.get(f"{url}/candidate_apply_job", json={
                "user_id": self.user_id,
                "title": self.comboBox.currentText()
            }).json()

            if application_status_check["alreadyApplied"]:
                self.label_6.setText(f"Already applied for {application_status_check['title']}")
            else:
                self.label_6.setText("Application Successful.")
        except:
            self.label_6.setText("Check your internet connection and try again")

    def view_candidate_result(self):
        try:
            if len(self.list_of_results):
                for i in range(len(self.list_of_results) - 1, -1, -1):
                    self.list_of_results[i].deleteLater()

            test_status_request = requests.get(f"{url}/candidate_test_status", json={
                "user_id": self.user_id
            })

            if test_status_request.json()["gaveTest"]:
                candidate_result = requests.get(f"{url}/candidate_data", json={
                    "user_id": self.user_id
                }).json()

                self.list_of_results = [
                    QLabel(
                        "{}/{}".format(
                            candidate_result["aptitude_score"]["score"],
                            5 * candidate_result["aptitude_score"]["noofquest"],
                        ),
                        self.frame_13,
                    )]

                for criteria in ["agreeableness", "conscientiousness", "extraversion", "openness", "neuroticism"]:
                    self.list_of_results.append(
                        QLabel(
                            str(candidate_result["personality_score"][criteria]), self.frame_12
                        )
                    )

                self.frame_13.layout().addWidget(self.list_of_results[0])
                for item in self.list_of_results[1:]:
                    self.frame_12.layout().addWidget(item)
            else:
                self.list_of_results = [
                    QLabel("Give Aptitude Test", self.frame_13),
                    QLabel("Give Personality Test", self.frame_12),
                    QLabel("Give Personality Test", self.frame_12),
                    QLabel("Give Personality Test", self.frame_12),
                    QLabel("Give Personality Test", self.frame_12),
                    QLabel("Give Personality Test", self.frame_12),
                ]
                self.frame_13.layout().addWidget(self.list_of_results[0])
                for item in self.list_of_results[1:]:
                    self.frame_12.layout().addWidget(item)
        except:
            pass

    def give_test(self):
        try:
            response = requests.get(f"{url}/give_test", json={"user_id": self.user_id})

            if response.status_code != 200:
                self.label_4.setText("Request Error")

            elif response.json()["start_test"]:
                self.load_aptitude_test_signal.emit(self.user_id)
            else:
                self.label_4.setText(f"{self.label_4.text()}\nAlready attempted\nCheck Results")
        except:
            self.label_4.setText("Unable to find candidate")

    def combo_box_change(self, value):
        for i in range(len(self.results)):
            if self.results[i]["title"] == value:
                self.label_2.setText(self.results[i]["title"])
                self.label_7.setText(self.results[i]["location"])
                self.label_9.setText(
                    str(self.results[i]["lastdate"])
                )
                self.label_15.setText(self.results[i]["type"])
                self.label_8.setText(self.results[i]["description"])

    def get_jobs(self):
        try:
            self.results = requests.get(f"{url}/get_jobs", json={
                "document_filter": {"isShortlisted": False}
            }).json()
            for job in self.results:
                self.comboBox.addItem(job["title"])
        except:
            self.label_16.setText("Please check internet connection and Login Again.")
            self.label_16.wordWrap()
