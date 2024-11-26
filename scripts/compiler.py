import os
import re
import sqlite3
import sys
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QColor, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QAction, QGraphicsDropShadowEffect, QApplication, \
    QMessageBox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
dir = os.path.dirname(__file__)
import webbrowser

class micai(QMainWindow):
    def __init__(self):
        super().__init__()
        self.completed_ = "0"
        self.selected_cooo = None
        self.selected_blood = None
        self.selected_sex = None
        self.age = None
        self.selected_fati = None
        self.selected_cou = None
        self.selected_fever = None
        relative_path = os.path.join(dir, "../_internal/ui/medui.ui")
        ui_path = os.path.abspath(relative_path)
        uic.loadUi(ui_path, self)
        self.drag_start_position = None
        self.setFixedSize(1057, 728)
        self.setStyleSheet("""
            QMainWindow {
                border-radius: 60px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(100)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)
        self.setWindowTitle('Med-AI')
        self.setupui()
        self.loadwelcome()
        self.train_model()

    def train_model(self):
        data = pd.read_csv(os.path.join(dir, "../_internal/scripts/diseases.csv"))
        self.X = data.drop(['Disease'], axis=1)
        self.y = data['Disease']
        encoder = LabelEncoder()
        for col in self.X.select_dtypes(include=['object']).columns:
            self.X[col] = encoder.fit_transform(self.X[col])
        self.disease_encoder = LabelEncoder()
        y = self.disease_encoder.fit_transform(self.y)
        X_train, X_test, y_train, y_test = train_test_split(self.X, y, test_size=0.2, random_state=42)
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train a Random Forest Classifier
        self.forest = RandomForestClassifier(random_state=42)
        self.forest.fit(X_train_scaled, y_train)

        # Print encoder classes to debug

    def setupui(self):
        self.label.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/fever.png")))
        self.label_38.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/m_ai__1_-removebg-preview.png")))
        self.label_45.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/m_ai__1_-removebg-preview.png")))
        self.label_46.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/m_ai__1_-removebg-preview.png")))
        self.label_12.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/cough.png")))
        self.label_16.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/tiredness.png")))
        self.label_20.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/difficulty-breathing.png")))
        self.label_24.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/calendar.png")))
        self.label_28.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/lavatory.png")))
        self.label_32.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/blood-pressure.png")))
        self.label_36.setPixmap(
            QtGui.QPixmap(os.path.join(dir, "../_internal/ui/cholesterol.png")))
        icon = QIcon(os.path.join(dir, "../_internal/ui/quiz.png"))
        self.start.setIcon(icon)
        icon2 = QIcon(os.path.join(dir, "../_internal/ui/file-medical-alt.png"))
        self.report.setIcon(icon2)

    def loadwelcome(self):
        path2 = "../_internal/db/user.db"
        db_dir = os.path.dirname(path2)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        conn = sqlite3.connect(path2)
        local = conn.cursor()
        local.execute('''
                                CREATE TABLE IF NOT EXISTS LocalUser(
                                    Username TEXT,
                                    Password TEXT,
                                    Email TEXT
                                )
                            ''')
        conn.close()
        self.stackedWidget.setCurrentWidget(self.startup)
        self.start.clicked.connect(self.locallogin)
        self.personeel.clicked.connect(self.openlink)
        self.report.clicked.connect(self.openlink)

    def openlink(self):
        url = "https://www.who.int/"
        webbrowser.open(url)

    def create_acc(self):
        self.stackedWidget.setCurrentWidget(self.create)
        self.personeel_3.clicked.connect(self.verify_local)
        self.start_3.clicked.connect(self.locallogin)

    def verify_local(self):
        username = self.userr.text()
        passkey = self.password_.text()
        email = self.email_.text()
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not username:
            self.label_43.setText("Username must not be empty")
            QTimer.singleShot(2000, lambda: self.label_43.setText("Create An Account"))
            return False
        if not email:
            self.label_43.setText("Email must not be empty")
            QTimer.singleShot(2000, lambda: self.label_43.setText("Create An Account"))
            return False
        if not re.match(email_regex, email):
            self.label_43.setText("Invalid email address")
            QTimer.singleShot(2000, lambda: self.label_43.setText("Create An Account"))
            return False
        if not passkey:
            self.label_43.setText("Password must not be empty")
            QTimer.singleShot(2000, lambda: self.label_43.setText("Create An Account"))
            return False
        if len(passkey) < 6:
            self.label_43.setText("Password must be at least 6 characters")
            QTimer.singleShot(2000, lambda: self.label_43.setText("Proceed"))
        try:
            username3 = self.userr.text()
            path2 = "../_internal/db/user.db"
            conn = sqlite3.connect(path2)
            local = conn.cursor()
            local.execute('''
                    SELECT Username FROM LocalUser WHERE Username = ?;
                ''', (username3,))
            existing_user = local.fetchone()
            if existing_user:
                msg_bbbox = QMessageBox(self)
                msg_bbbox.setText("User Exists, Maybe Try Login?")
                msg_bbbox.setWindowTitle('Warning')
                msg_bbbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_bbbox.setDefaultButton(QMessageBox.No)
                msg_bbbox.setStyleSheet("""
                                                QMessageBox {
                                background-color: rgb(34, 34, 34);
                                border-radius: 20px;
                            }
                            QMessageBox QLabel {
                                color: white;
                                font-size: 14px;
                                font: 63 9pt "Work Sans SemiBold";
                            }
                            QMessageBox QPushButton {
                                background-color: rgb(88, 180, 194);
                                border-radius: 10px;
                                color: rgb(255, 255, 255);
                            }
                            QMessageBox QPushButton:hover {
                                background-color: rgba(88, 180, 194, 200);}

                            QMessageBox QPushButton:pressed {
                                background-color: #388E3C;
                            }
                                """)
                reply = msg_bbbox.exec_()
                if reply == QMessageBox.Yes:
                    self.transition_to_login()
            else:
                username = self.userr.text()
                passkey = self.password_.text()
                email = self.email_.text()
                local.execute('''
                                                INSERT INTO LocalUser (Username, Password, Email)
                                                VALUES (?, ?, ?);
                                            ''', (username, passkey, email))
                conn.commit()
                self.locallogin()
        except Exception as d:
            print(d)
        return False

    def locallogin(self):
        self.stackedWidget.setCurrentWidget(self.login)
        self.user.clear()
        self.passwordlocal.clear()
        self.createacc.clicked.connect(self.create_acc)
        self.start_2.clicked.connect(self.logvalid)


    def logvalid(self):
        user = self.user.text()
        passkey = self.passwordlocal.text()
        try:
            path = "../_internal/db/user.db"
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LocalUser WHERE Username = ? AND Password = ?", (user, passkey))
            result = cursor.fetchone()
            if result:
                self.yes()
            else:
                self.no()
            conn.close()
        except Exception as error:
            print({error})

    def no(self):
        self.label_41.setText("Login failed! Incorrect username or password")
        QTimer.singleShot(4000, lambda: self.label_41.setText("Login"))

    def yes(self):
        self.start_test()

    def start_test(self):
        self.show_q1()

    def show_q1(self):
        self.stackedWidget.setCurrentWidget(self.q1)
        self.nextq1.setDisabled(True)
        self.nextq1.clicked.connect(self.submit_q1)
        self.radio1.toggled.connect(lambda: self.q1_radio_state() if self.radio1.isChecked() else None)
        self.radio2.toggled.connect(lambda: self.q1_radio_state() if self.radio2.isChecked() else None)
        if self.completed_ == "1":
            print("Clearing radio buttons")
            radios = [self.radio1, self.radio2, self.radio3, self.radio4, self.radio5,
                      self.radio6, self.radio7, self.radio8, self.radio11, self.radio12,
                      self.radio13, self.radio14, self.radio14_2, self.radio16, self.radio16_2]
            for radio in radios:
                radio.setAutoExclusive(False)
                radio.setChecked(False)
            self.completed_ = "0"

    def q1_radio_state(self):
        if self.radio1.isChecked() and not self.radio2.isChecked():
            self.nextq1.setDisabled(False)
        elif self.radio2.isChecked() and not self.radio1.isChecked():
            self.nextq1.setDisabled(False)
        else:
            self.nextq1.setDisabled(True)

    def submit_q1(self):
        if self.radio1.isChecked():
            self.selected_fever = "1"
        elif self.radio2.isChecked():
            self.selected_fever = "0"
        self.show_q2()

    def show_q2(self):
        self.stackedWidget.setCurrentWidget(self.q2)
        self.nextq2.setDisabled(True)
        self.nextq2.clicked.connect(self.submit_q2)
        self.backq2.clicked.connect(self.show_q1)
        self.radio3.toggled.connect(lambda: self.q2_radio_state() if self.radio3.isChecked() else None)
        self.radio4.toggled.connect(lambda: self.q2_radio_state() if self.radio4.isChecked() else None)

    def q2_radio_state(self):
        if self.radio3.isChecked() and not self.radio4.isChecked():
            self.nextq2.setDisabled(False)
        elif self.radio4.isChecked() and not self.radio3.isChecked():
            self.nextq2.setDisabled(False)
        else:
            self.nextq2.setDisabled(True)

    def submit_q2(self):
        if self.radio3.isChecked():
            self.selected_cou = "1"
        elif self.radio4.isChecked():
            self.selected_cou = "0"
        self.show_q3()  # Move to the third screen

    def show_q3(self):
        self.stackedWidget.setCurrentWidget(self.q3)  # Show the third screen
        self.nextq3.setDisabled(True)  # Disable next button initially
        self.nextq3.clicked.connect(self.submit_q3)  # Connect submit button
        self.backq3.clicked.connect(self.show_q2)  # Connect back button

        # Connect radio buttons
        self.radio5.toggled.connect(lambda: self.q3_radio_state() if self.radio5.isChecked() else None)
        self.radio6.toggled.connect(lambda: self.q3_radio_state() if self.radio6.isChecked() else None)

    def q3_radio_state(self):
        if self.radio5.isChecked() and not self.radio6.isChecked():
            self.nextq3.setDisabled(False)
        elif self.radio6.isChecked() and not self.radio5.isChecked():
            self.nextq3.setDisabled(False)
        else:
            self.nextq3.setDisabled(True)

    def submit_q3(self):
        if self.radio5.isChecked():
            self.selected_fati = "1"
        elif self.radio6.isChecked():
            self.selected_fati = "0"
        self.show_q4()  # Move to the fourth screen

    def show_q4(self):
        self.stackedWidget.setCurrentWidget(self.q4)  # Show the fourth screen
        self.nextq4.setDisabled(True)  # Disable next button initially
        self.nextq4.clicked.connect(self.submit_q4)  # Connect submit button
        self.backq4.clicked.connect(self.show_q3)  # Connect back button

        # Connect radio buttons for q4
        self.radio7.toggled.connect(lambda: self.q4_radio_state() if self.radio7.isChecked() else None)
        self.radio8.toggled.connect(lambda: self.q4_radio_state() if self.radio8.isChecked() else None)

    def q4_radio_state(self):
        if self.radio7.isChecked() and not self.radio8.isChecked():
            self.nextq4.setDisabled(False)
        elif self.radio8.isChecked() and not self.radio7.isChecked():
            self.nextq4.setDisabled(False)
        else:
            self.nextq4.setDisabled(True)

    def submit_q4(self):
        if self.radio7.isChecked():
            self.selected_diff = "1"
        elif self.radio8.isChecked():
            self.selected_diff = "0"
        self.show_q5()  # Move to the fifth screen

    # Continue creating methods for q5, q6, q7, and q8 in the same way...

    def show_q5(self):
        self.stackedWidget.setCurrentWidget(self.q5)  # Show the fifth screen
        self.nextq5.setDisabled(True)  # Disable next button initially
        self.nextq5.clicked.connect(self.submit_q5)  # Connect submit button
        self.backq5.clicked.connect(self.show_q4)
        self.agefield.setMaxLength(3)
        self.agefield.setValidator(QIntValidator(2, 130, self))
        self.agefield.textChanged.connect(self.inputvalidate)

    def inputvalidate(self):
        self.nextq5.setDisabled(False)
        text = self.agefield.text()
        if len(text) == 0:
            self.nextq5.setDisabled(True)

    def submit_q5(self):
        self.age = self.agefield.text()
        self.show_q6()

    def show_q6(self):
        self.stackedWidget.setCurrentWidget(self.q6)
        self.nextq6.setDisabled(True)
        self.nextq6.clicked.connect(self.submit_q6)
        self.backq6.clicked.connect(self.show_q5)
        self.radio11.toggled.connect(lambda: self.q6_radio_state() if self.radio11.isChecked() else None)
        self.radio12.toggled.connect(lambda: self.q6_radio_state() if self.radio12.isChecked() else None)

    def q6_radio_state(self):
        if self.radio11.isChecked() and not self.radio12.isChecked():
            self.nextq6.setDisabled(False)
        elif self.radio12.isChecked() and not self.radio11.isChecked():
            self.nextq6.setDisabled(False)
        else:
            self.nextq6.setDisabled(True)

    def submit_q6(self):
        if self.radio11.isChecked():
            self.selected_sex = "1"
        elif self.radio12.isChecked():
            self.selected_sex = "0"
        self.show_q7()

    def show_q7(self):
        self.stackedWidget.setCurrentWidget(self.q7)  # Show the seventh screen
        self.nextq7.setDisabled(True)  # Disable next button initially
        self.nextq7.clicked.connect(self.submit_q7)  # Connect submit button
        self.backq7.clicked.connect(self.show_q6)  # Connect back button

        # Connect radio buttons for q7
        self.radio13.toggled.connect(lambda: self.q7_radio_state() if self.radio13.isChecked() else None)
        self.radio14.toggled.connect(lambda: self.q7_radio_state() if self.radio14.isChecked() else None)
        self.radio14_2.toggled.connect(lambda: self.q7_radio_state() if self.radio14_2.isChecked() else None)

    def q7_radio_state(self):
        if self.radio13.isChecked() and not self.radio14.isChecked():
            self.nextq7.setDisabled(False)
        elif self.radio14.isChecked() and not self.radio13.isChecked():
            self.nextq7.setDisabled(False)
        elif self.radio14_2.isChecked() and not self.radio14.isChecked():
            self.nextq7.setDisabled(False)
        else:
            self.nextq7.setDisabled(True)

    def submit_q7(self):
        if self.radio13.isChecked():
            self.selected_blood = "0"
        elif self.radio14.isChecked():
            self.selected_blood = "1"
        elif self.radio14_2.isChecked():
            self.selected_blood = "2"
        self.show_q8()

    def show_q8(self):
        self.stackedWidget.setCurrentWidget(self.q8)  # Show the eighth screen
        self.nextq8.setDisabled(True)  # Disable next button initially
        self.nextq8.clicked.connect(self.submit_q8)  # Connect submit button
        self.backq8.clicked.connect(self.show_q7)  # Connect back button

        # Connect radio buttons for q8
        self.radio15.toggled.connect(lambda: self.q8_radio_state() if self.radio15.isChecked() else None)
        self.radio16.toggled.connect(lambda: self.q8_radio_state() if self.radio16.isChecked() else None)
        self.radio16_2.toggled.connect(lambda: self.q8_radio_state() if self.radio16_2.isChecked() else None)

    def q8_radio_state(self):
        if self.radio15.isChecked() and not self.radio16.isChecked():
            self.nextq8.setDisabled(False)
        elif self.radio16.isChecked() and not self.radio15.isChecked():
            self.nextq8.setDisabled(False)
        elif self.radio16_2.isChecked() and not self.radio16.isChecked():
            self.nextq8.setDisabled(False)
        else:
            self.nextq8.setDisabled(True)

    def submit_q8(self):
        if self.radio15.isChecked():
            self.selected_cooo = "0"
        elif self.radio16.isChecked():
            self.selected_cooo = "1"
        elif self.radio16_2.isChecked():
            self.selected_cooo = "2"
        self.results()

    def results(self):
        self.stackedWidget.setCurrentWidget(self.result)
        self.get_user_input()
        self.completed_ = "1"
        self.restart.clicked.connect(self.show_q1)

    def get_user_input(self):
        try:
            fever = self.selected_fever
            cough = self.selected_cou
            fatigue = self.selected_fati
            difficulty_breathing = self.selected_diff
            age = int(self.age)
            gender = self.selected_sex
            blood_pressure = self.selected_blood
            cholesterol_level = self.selected_cooo
        except KeyError as e:
            raise ValueError(f"Invalid input: {e.args[0]}")
        self.user_data = pd.DataFrame({
            'Fever': [fever],
            'Cough': [cough],
            'Fatigue': [fatigue],
            'Difficulty Breathing': [difficulty_breathing],
            'Age': [age],
            'Gender': [gender],
            'Blood Pressure': [blood_pressure],
            'Cholesterol Level': [cholesterol_level]
        })
        self.predict_disease()
        return self.user_data

    def predict_disease(self):
        try:
            user_data = self.user_data.reindex(columns=self.X.columns,
                                               fill_value=0)
            scaled_user_data = self.scaler.transform(user_data)
            prediction = self.forest.predict(scaled_user_data)
            disease_prediction = self.disease_encoder.inverse_transform(prediction)
            self.prediction.setText(disease_prediction[0])
            return disease_prediction[0]
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = micai()
    window.show()
    sys.exit(app.exec_())