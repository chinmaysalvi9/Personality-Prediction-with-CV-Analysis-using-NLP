import nltk
import requests
import textract
import unidecode
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
from deskop_app.system_app_config import url
from deskop_app.ui.generated_code.candidate_register import Ui_Dialog


class CandidateRegister(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Register")
        self.createPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registerButton.clicked.connect(self.register)
        self.browseButton.clicked.connect(self.browse_files)
        self.filename = None

    def browse_files(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "..\\")
        self.browseInput.setText(file_name[0])
        self.filename = self.browseInput.text()

    def process_file(self):
        if self.filename is None:
            return ""

        if self.filename.endswith((".pdf", ".PDF")):
            input_text = extract_text(self.filename)
        else:
            input_text = textract.process(self.filename)

        soup = BeautifulSoup(input_text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        input_text = unidecode.unidecode(stripped_text)
        input_text = input_text.replace("\n", " ").lower()

        return " ".join(
            [
                w
                for w in nltk.tokenize.word_tokenize(input_text)
                if w not in set(nltk.corpus.stopwords.words("english"))
            ]
        )

    def register(self):
        if self.createPasswordInput.text() == self.confirmPasswordInput.text():
            try:
                self.ProcessFile()

                response = requests.get(
                    f"{url}/register",
                    json={
                        "_id": self.emailIdInput.text(),
                        "first_name": self.firstNameInput.text(),
                        "last_name": self.lastNameInput.text(),
                        "password": self.createPasswordInput.text(),
                        "alreadyApplied": False,
                        "gender": self.genderInput.text(),
                        "graduation_date": self.graduationDateInput.text(),
                        "major": self.majorInput.text(),
                        "degree": self.degreeInput.text(),
                        "place_of_study": self.placeOfStudyInput.text(),
                        "gaveTest": False,
                        "university_name": self.universityNameInput.text(),
                        "file": self.ProcessFile(),
                    },
                )
            except:
                pass
            self.backButton.click()
