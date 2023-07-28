import nltk
import datetime
import requests
import unidecode
import pandas as pd
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QTableView,
    QHeaderView,
    QFileDialog,
    QFormLayout
)
from bs4 import BeautifulSoup
from deskop_app.system_app_config import url
from deskop_app.ui.additional_code.pandas_model import PandasModel
from deskop_app.ui.generated_code.admin_main_window import Ui_MainWindow


class AdminMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.candidate_list = None
        self.df = None
        self.scrollAreaLay = None
        self.jobs = None
        self.setupUi(self)
        self.setWindowTitle("System")
        self.label_list = []
        self.exception_label_added = False
        self.view = None
        self.view2 = None
        self.currently_shortlisting = None
        self.admin_list_layout = QFormLayout(self.frame_11)
        self.actionAddNewJob.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.addNewJobs)
        )
        self.actionViewDetails.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.viewDetails)
        )
        self.actionViewResults.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.viewResults)
        )
        self.actionShortlistCandidates.triggered.connect(
            self.shortlisting_status_update
        )
        self.actionAptitude.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.aptitude)
        )
        self.actionPersonality.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.personality)
        )
        self.actionAdd_new_Admin.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.addAdmin)
        )
        self.actionManage_Admins.triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.manageAdmin)
        )

        self.comboBox.currentTextChanged.connect(self.change_spin_box_range)
        self.comboBox_2.currentTextChanged.connect(self.display_candidates)
        self.comboBox_3.currentTextChanged.connect(self.view_results_of_candidate)

        self.AddJobButton.clicked.connect(self.add_new_job)
        self.AddAptitudeQuestionButton.clicked.connect(self.add_new_aptitude_question)
        self.AddPersonalityQuestionButton.clicked.connect(
            self.add_new_personality_question
        )
        self.ShortlistButton.clicked.connect(self.shortlist)
        self.createNewAdminButton.clicked.connect(self.add_admin)
        self.pushButton.clicked.connect(self.save_df)
        self.get_jobs()
        self.get_admins()

    def add_new_job(self):
        try:
            self.label_5.setText("Adding...")
            response = requests.get(
                f"{url}/add_new_job",
                json={
                    "title": self.jobTitle.text(),
                    "location": self.jobLocation.text(),
                    "isShortlisted": False,
                    "lastdate": datetime.datetime.combine(
                        self.dateEdit.date().toPyDate(), datetime.datetime.min.time()
                    ),
                    "description": self.jobDescription.toPlainText(),
                    "type": self.jobType.currentText(),
                    "file": self.process_file(),
                },
            )
            if response.text == "True" and response.status_code == 200:
                self.label_5.setText("Successfully Added")
            else:
                self.label_5.setText("Problem while sending addition request.")
            self.get_jobs()
        except:
            self.label_5.setText("Unable to add. Please try again")

    def process_file(self):
        soup = BeautifulSoup(self.jobDescription.toPlainText(), "html.parser")
        stripped_text = soup.get_text(separator=" ")
        input_text = unidecode.unidecode(stripped_text)
        input_text = input_text.replace("\n", " ").lower()
        stop_words = set(nltk.corpus.stopwords.words("english"))
        word_tokens = nltk.tokenize.word_tokenize(input_text)

        output_text = ""
        for w in word_tokens:
            if w not in stop_words:
                output_text = output_text + " " + w

        return output_text

    def display_candidates(self):
        self.label_27.setText(
            "Candidate for {} are:".format(self.comboBox_2.currentText())
        )
        self.candidate_list = self.scrollAreaWidgetContents_2.layout()

        try:
            if len(self.label_list) != 0:
                for l in range(len(self.label_list) - 1, -1, -1):
                    self.label_list[l].deleteLater()

            self.label_26.setText("Searching database")

            self.label_list = []
            candidates = requests.get(
                f"{url}/candidates", json={"job": self.comboBox_2.currentText()}
            ).json()

            for index, candidate in enumerate(candidates):
                self.label_list.append(
                    QLabel(
                        f"{str(index + 1)}.\t{candidate['_id']}",
                        self.scrollAreaWidgetContents_2,
                    )
                )
                self.candidate_list.addRow(self.label_list[index])

            self.label_26.setText("")
        except:
            if self.exception_label_added:
                self.exceptionLabel.setText(
                    "Please check internet connection and Login Again."
                )
            else:
                self.exceptionLabel = QLabel(
                    "Please check internet connection and Login Again."
                )
                self.exception_label_added = True
                self.candidate_list.addWidget(self.exceptionLabel)

    def view_results_of_candidate(self):
        if self.view2:
            self.view2.deleteLater()
        if not self.scrollAreaWidgetContents_3.layout():
            self.scrollAreaLay2 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        try:
            candidates = requests.get(
                f"{url}/candidates", json={"job": self.comboBox_3.currentText()}
            ).json()

            df = pd.DataFrame(
                columns=[
                    "Email ID",
                    "Aptitude Score",
                    "Extraversion",
                    "Neuroticism",
                    "Conscientiousness",
                    "Agreeableness",
                    "Openness",
                ]
            )
            for candidate in candidates:
                if candidate["gaveTest"]:
                    df.loc[df.shape[0]] = (
                        candidate["_id"],
                        f"{candidate['aptitude_score']['score']}/{5 * candidate['aptitude_score']['noofquest']}",
                        round(candidate["personality_score"]["extraversion"], 2),
                        round(candidate["personality_score"]["neuroticism"], 2),
                        round(candidate["personality_score"]["conscientiousness"], 2),
                        round(candidate["personality_score"]["agreeableness"], 2),
                        round(candidate["personality_score"]["openness"], 2),
                    )
                else:
                    df.loc[df.shape[0]] = [candidate["_id"]] + [None] * 6

            df.fillna(0)
            model = PandasModel(df)
            self.view2 = QTableView()
            self.view2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.view2.setStyleSheet(
                u"background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);"
            )
            self.view2.setModel(model)
            self.scrollAreaLay2.addWidget(self.view2)
        except:
            self.label_30.setText("Unable to reach server")

    def change_spin_box_range(self):
        response = requests.get(
                f"{url}/candidate_count",
                json={"title": self.comboBox.currentText()},
            )
        response_data = response.json()

        if response.status_code != 200:
            print("error")
        elif "error" in response_data:
            print(response_data["error"])
        else:
            self.spinBox.setRange(
                1,
                response_data["count"],
            )

    def shortlisting_changes(self, enable):
        self.comboBox.setEditable(enable)
        self.spinBox.setDisabled(not enable)
        self.ShortlistButton.setEnabled(enable)
        self.pushButton.setEnabled(enable)

    def shortlist(self):
        try:
            if self.comboBox.currentText() is not None:
                self.shortlisting_changes(False)

                if self.view:
                    self.view.deleteLater()
                if not self.scrollAreaWidgetContents.layout():
                    self.scrollAreaLay = QVBoxLayout(self.scrollAreaWidgetContents)

                response = requests.get(
                    f"{url}/calculate_scores",
                    json={"title": self.comboBox.currentText()},
                )
                response_data = response.json()

                if response.status_code != 200 or not response_data["status"]:
                    self.label_18.setText("Server Error")
                    self.shortlisting_changes(True)
                    self.currently_shortlisting = None
                else:
                    self.label_18.setText("Shortlisting")
                    self.currently_shortlisting = self.comboBox.currentText()

        except Exception as e:
            self.shortlisting_changes(True)
            self.label_18.setText(f"Error occurred {e}")

    def save_df(self):
        if self.df:
            directory = QFileDialog.getExistingDirectory(
                self, "Select Folder To Store Spreadsheet", "."
            )
            self.df.to_excel(
                directory
                + "\\Shortlisted {} Candidates.xlsx".format(self.comboBox.currentText())
            )

    def add_new_aptitude_question(self):
        try:
            self.label_14.setText("Adding...")
            response = requests.get(
                f"{url}/add_aptitude_question",
                json={
                    "question_data": [
                        self.aptitudeQuestion.text(),
                        self.correctOption.currentText(),
                        self.option1.text(),
                        self.option2.text(),
                        self.option3.text(),
                        self.option4.text(),
                    ]
                },
            )
            if response.text == "True" and response.status_code == 200:
                self.label_14.setText("Successfully Added")
            else:
                self.label_14.setText("Problem while sending addition request.")
        except:
            self.label_14.setText("Unable to add. Please try again later")

    def add_new_personality_question(self):
        try:
            self.label_15.setText("Adding...")
            response = requests.get(
                f"{url}/add_personality_question",
                json={
                    "question": self.personalityQuestion.text(),
                    "type": self.type.currentText(),
                    "ispositive": str(self.isPositiveQuestion.currentText())
                },
            )
            if response.text == "True" and response.status_code == 200:
                self.label_15.setText("Successfully Added")
            else:
                self.label_15.setText("Problem while sending addition request.")
            self.label_15.setText("Successfully Added")
        except:
            self.label_15.setText("Unable to add. Please try again later")

    def add_admin(self):

        if len(self.emailIdInput.text()) == 0:
            self.label_22.setText("Please enter email address.")

            if len(self.createPasswordInput.text()) == 0:
                self.label_22.setText("Please enter password")

                if len(self.confirmPasswordInput.text()) == 0:
                    self.label_22.setText("Please enter email address and password.")

        elif self.createPasswordInput.text() == self.confirmPasswordInput.text():
            try:
                self.label_22.setText("Adding new administrator...")
                response = requests.get(
                    f"{url}/add_admin",
                    json={
                        "credentials": (
                            self.emailIdInput.text(),
                            self.createPasswordInput.text(),
                        )
                    },
                )
                if response.text == "True" and response.status_code == 200:
                    self.label_22.setText("Successfully Added")
                else:
                    self.label_22.setText("Problem while sending addition request.")
                self.get_admins()
            except:
                self.label_22.setText(
                    "Unable to add. Please check internet connection."
                )
        else:
            self.label_22.setText("Please enter same password in both fields.")

    def get_jobs(self):
        try:
            if self.comboBox.count():
                self.comboBox.clear()
            if self.comboBox_2.count():
                self.comboBox_2.clear()
            if self.comboBox_3.count():
                self.comboBox_3.clear()

            self.jobs = requests.get(f"{url}/get_jobs", json=dict()).json()

            for job in self.jobs:
                if not job["isShortlisted"]:
                    self.comboBox.addItem(job["title"])
                self.comboBox_2.addItem(job["title"])
                self.comboBox_3.addItem(job["title"])
        except:
            self.label_18.setText("Please check internet connection and Login Again.")

    def get_admins(self):
        self.admin_list_layout.addRow(
            QLabel("Administrators Email List", self.frame_11)
        )
        try:
            response = requests.get(f"{url}/get_admins")
            for index, admin_name in enumerate(response.json()):
                self.admin_list_layout.addRow(
                    QLabel(f"{index + 1}.\t{admin_name}", self.frame_11)
                )
        except:
            self.admin_list_layout.addWidget(
                QLabel("Please check internet connection and Login Again.")
            )

    def shortlisting_status_update(self):
        self.stackedWidget.setCurrentWidget(self.shortlistCandidates)

        if not self.ShortlistButton.isEnabled():
            response = requests.get(
                f"{url}/check_shortlisting_status",
                json={"title": self.comboBox.currentText()},
            )
            response_data = response.json()

            if response.status_code != 200:
                self.label_18.setText("Error has occurred")
                self.shortlisting_changes(True)

            elif response_data["status"] == "Error":
                self.label_18.setText("Server error has occurred")
                self.shortlisting_changes(True)

            elif response_data["status"] == "Successful":
                try:
                    personality_criteria = [
                        "Extraversion",
                        "Neuroticism",
                        "Conscientiousness",
                        "Agreeableness",
                        "Openness",
                    ]
                    data = []
                    for c in requests.get(
                        f"{url}/candidates", json={"job": self.comboBox.currentText()}
                    ):
                        if c["gaveTest"]:
                            row = {
                                "Email ID": c["_id"],
                                "CV Score": c["file_score"],
                                "Aptitude Score": round(
                                    c["aptitude_score"]["score"]
                                    / 5
                                    * c["aptitude_score"]["noofquest"],
                                    2,
                                ),
                            }

                            for criteria in personality_criteria:
                                row[criteria] = round(
                                    c["personality_score"][criteria.lower()], 2
                                )

                            data.append(row)

                    self.df = (
                        pd.DataFrame(
                            data=data,
                            columns=["Email ID", "CV Score", "Aptitude Score"]
                            + personality_criteria,
                        )
                        .sort_values(
                            by=[
                                "CV Score",
                                "Aptitude Score",
                                "Conscientiousness",
                                "Agreeableness",
                                "Openness",
                            ],
                            ascending=False,
                        )
                        .head(self.spinBox.value())
                    )

                    response = requests.get(
                        f"{url}/shortlist", json={"ids": self.df["Email ID"].to_list()}
                    )

                    if response.status_code != 200 or response.text == "False":
                        self.label_18.setText("Error has occurred")

                    self.view = QTableView()
                    self.view.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch
                    )
                    self.view.setModel(PandasModel(self.df))
                    self.view.setStyleSheet(
                        u"background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);"
                    )
                    self.scrollAreaLay.addWidget(self.view)
                    self.label_18.setText(
                        "Shortlisted {} candidates for {}".format(
                            self.spinBox.value(), self.comboBox.currentText()
                        )
                    )
                except:
                    self.label_18.setText("Error has occurred")

                self.get_jobs()
                self.shortlisting_changes(True)
