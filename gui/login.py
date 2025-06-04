# gui/login_screen.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from gui.list import EntryScreen
from PySide6.QtGui import QIcon

import os

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Platform - Giriş Ekranı")
        self.setGeometry(600, 300, 300, 180)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        # Kullanıcı Adı
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adı")
        layout.addWidget(QLabel("Kullanıcı Adı:"))
        layout.addWidget(self.username_input)

        # Şifre
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Şifre:"))
        layout.addWidget(self.password_input)

        # Giriş Butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        # Geri Bildirim Mesajı (popup yerine)
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "1234":
            self.message_label.setText("✅ Giriş başarılı, yönlendiriliyorsunuz...")
            self.message_label.setStyleSheet("color: green; font-weight: bold;")

            # Ekranı geçiş biraz gecikmeli yapabilirsin istersen (QTimer ile)
            self.hide()
            self.EntryScreen = EntryScreen()
            self.EntryScreen.show()
        else:
            self.message_label.setText("❌ Kullanıcı adı veya şifre hatalı.")
            self.message_label.setStyleSheet("color: red; font-weight: bold;")
