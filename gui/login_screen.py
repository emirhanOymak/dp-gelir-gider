from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QIcon
from db.queries.kullanici_queries import check_user_credentials
from models.kullanici import Kullanici
from gui.main_screen import MainScreen

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
        layout.addWidget(QLabel("Şifre:"))
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        kullanici: Kullanici = check_user_credentials(username, password)

        if kullanici:
            self.message_label.setText("✅ Giriş başarılı, yönlendiriliyorsunuz...")
            self.message_label.setStyleSheet("color: green; font-weight: bold;")

            self.hide()
            self.main_screen = MainScreen()
            self.main_screen.show()
        else:
            self.message_label.setText("❌ Kullanıcı adı veya şifre hatalı.")
            self.message_label.setStyleSheet("color: red; font-weight: bold;")
