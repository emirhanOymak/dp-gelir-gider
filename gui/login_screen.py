from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from db.queries.kullanici_queries import check_user_credentials
from models.kullanici import Kullanici
from gui.main_screen import MainScreen
from utils.logger import log_info, log_warning
from PySide6.QtGui import QIcon, QAction, QPixmap


import os

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Platform - Giriş Ekranı")
        self.setGeometry(600, 300, 300, 180)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()


        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adı")

        layout.addWidget(QLabel("Kullanıcı Adı:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.installEventFilter(self) #CapsLock
        self.password_input.returnPressed.connect(self.check_login)

        ##Eye Button
        eye_icon_path = os.path.join(os.path.dirname(__file__), "../assets/eye.png")
        eye_off_icon_path = os.path.join(os.path.dirname(__file__), "../assets/eye-off.png")

        self.toggle_action = QAction(QIcon(eye_icon_path), "Şifre Görünürlüğü", self)
        self.toggle_action.setCheckable(True)
        self.toggle_action.toggled.connect(lambda checked: self.toggle_password_visibility(checked, eye_icon_path, eye_off_icon_path))
        self.password_input.addAction(self.toggle_action, QLineEdit.TrailingPosition)

        layout.addWidget(QLabel("Şifre:"))
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

    def toggle_password_visibility(self, checked, icon_hidden, icon_visible):
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
        self.toggle_action.setIcon(QIcon(icon_visible if checked else icon_hidden))

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()


        kullanici: Kullanici = check_user_credentials(username, password)

        if kullanici:
            log_info(f"Giris basarili - Kullanici: {username}")  # ✅
            self.message_label.setText("✅ Giriş başarılı, yönlendiriliyorsunuz...")
            self.message_label.setStyleSheet("color: green; font-weight: bold;")

            self.hide()
            self.main_screen = MainScreen(kullanici=kullanici)
            self.main_screen.show()
        else:
            self.password_input.setStyleSheet("border: 1px solid red;")
            self.password_input.clear()
            self.password_input.setFocus()
            log_warning(f"Giris basarisiz - Kullanici: {username}")  # ❌
            self.message_label.setText("❌ Kullanıcı adı veya şifre hatalı.")
            self.message_label.setStyleSheet("color: red; font-weight: bold;")
