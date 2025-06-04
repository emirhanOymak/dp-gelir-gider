# gui/login_screen.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from gui.list import EntryScreen

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")
        self.setGeometry(600, 300, 300, 150)

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

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "1234":
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")

            self.hide()
            self.EntryScreen = EntryScreen()
            self.EntryScreen.show()

        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı.")
