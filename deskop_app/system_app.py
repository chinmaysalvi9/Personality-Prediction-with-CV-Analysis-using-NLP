import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from deskop_app.ui.additional_code.customized_admin_main_window import AdminMainWindow
from deskop_app.ui.additional_code.customized_candidate_login import CandidateLogin
from deskop_app.ui.additional_code.customized_admin_login import AdminLogin
from deskop_app.ui.additional_code.customized_candidate_register import CandidateRegister
from deskop_app.ui.additional_code.customized_candidate_main_window import CandidateMainWindow
from deskop_app.ui.additional_code.customized_aptitude_quiz import AptitudeQuizWindow
from deskop_app.ui.additional_code.customized_personality_quiz import PersonalityQuizWindow
from deskop_app.ui.additional_code.customized_personality_quiz_end import PersonalityQuizEndWindow
from deskop_app.ui.additional_code.customized_splash_screen import SplashScreen
from deskop_app.ui.additional_code.helper_function import center_window


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")

        # Create a stacked widget to hold different UI screens
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Create instances of each UI screen
        self.candidate_login_ui = CandidateLogin()
        self.admin_login_ui = AdminLogin()
        self.candidate_register_ui = CandidateRegister()
        self.candidate_main_window = CandidateMainWindow()
        self.admin_main_window = AdminMainWindow()
        self.aptitude_quiz_window = AptitudeQuizWindow()
        self.personality_quiz_window = PersonalityQuizWindow()
        self.personality_quiz_end_window = PersonalityQuizEndWindow()

        # Add UI screens to the stacked widget
        self.stacked_widget.addWidget(self.candidate_login_ui)
        self.stacked_widget.addWidget(self.admin_login_ui)
        self.stacked_widget.addWidget(self.candidate_register_ui)
        self.stacked_widget.addWidget(self.candidate_main_window)
        self.stacked_widget.addWidget(self.admin_main_window)
        self.stacked_widget.addWidget(self.aptitude_quiz_window)
        self.stacked_widget.addWidget(self.personality_quiz_window)
        self.stacked_widget.addWidget(self.personality_quiz_end_window)

        # Connect signals from each UI screen to handle navigation
        self.candidate_login_ui.createAccountButton.clicked.connect(self.show_candidate_register_ui)
        self.candidate_login_ui.adminUIButton.clicked.connect(self.show_admin_login_ui)
        self.candidate_login_ui.successful_login.connect(self.show_candidate_main_window)

        self.candidate_register_ui.backButton.clicked.connect(self.show_candidate_login_ui)

        self.candidate_main_window.actionLogout.triggered.connect(lambda x: self.logout(True))
        self.candidate_main_window.load_aptitude_test_signal.connect(self.show_aptitude_test_window)

        self.aptitude_quiz_window.load_personality_test_signal.connect(self.show_personality_test_window)

        self.personality_quiz_window.personality_test_end_signal.connect(self.show_personality_test_end_window)

        self.personality_quiz_end_window.personality_test_end_signal.connect(self.show_candidate_main_window)

        self.admin_login_ui.candidateUIButton.clicked.connect(self.show_candidate_login_ui)
        self.admin_login_ui.successful_login.connect(self.show_admin_main_window)

        self.admin_main_window.actionLogout.triggered.connect(lambda x: self.logout(False))

        # Show the initial UI screen (Candidate Login UI)
        self.stacked_widget.setCurrentWidget(self.candidate_login_ui)

    def show_candidate_register_ui(self):
        self.stacked_widget.setCurrentWidget(self.candidate_register_ui)

    def show_admin_login_ui(self):
        self.stacked_widget.setCurrentWidget(self.admin_login_ui)

    def show_candidate_login_ui(self):
        self.stacked_widget.setCurrentWidget(self.candidate_login_ui)

    def show_candidate_main_window(self, user_id):
        self.candidate_main_window.set_candidate_name(user_id)
        self.stacked_widget.setCurrentWidget(self.candidate_main_window)

    def show_aptitude_test_window(self, user_id):
        self.aptitude_quiz_window.set_candidate_name(user_id)
        self.stacked_widget.setCurrentWidget(self.aptitude_quiz_window)

    def show_personality_test_window(self, user_id):
        self.personality_quiz_window.set_candidate_name(user_id)
        self.stacked_widget.setCurrentWidget(self.personality_quiz_window)

    def show_personality_test_end_window(self, data):
        self.personality_quiz_end_window.set_data(data)
        self.stacked_widget.setCurrentWidget(self.personality_quiz_end_window)

    def show_admin_main_window(self):
        self.stacked_widget.setCurrentWidget(self.admin_main_window)

    def logout(self, is_candidate):
        if is_candidate:
            self.candidate_login_ui.loginAckLabel.setText("Logout Successful")
            self.show_candidate_login_ui()
        else:
            self.admin_login_ui.loginAckLabel.setText("Logout Successful")
            self.show_admin_login_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ss = SplashScreen()
    center_window(ss)
    ss.show()
    app.exec_()

    main_app = MainApp()
    main_app.show()

    sys.exit(app.exec_())
