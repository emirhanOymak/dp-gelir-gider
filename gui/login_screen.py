from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from db.queries.kullanici_queries import check_user_credentials
from models.kullanici import Kullanici
from gui.main_menu_screen import MainMenuScreen
from utils.logger import log_info, log_warning
import os

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Platform - Giriş Ekranı")
        self.setGeometry(600, 300, 300, 200)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        # Kullanıcı Adı
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adı")
        layout.addWidget(QLabel("Kullanıcı Adı:"))
        layout.addWidget(self.username_input)

        # Şifre Alanı + Show/Hide Button
        layout.addWidget(QLabel("Şifre:"))
        pw_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.check_login)
        pw_layout.addWidget(self.password_input)

        self.show_password_btn = QPushButton("👁️")
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.setFixedWidth(40)
        self.show_password_btn.toggled.connect(self.toggle_password)
        pw_layout.addWidget(self.show_password_btn)

        layout.addLayout(pw_layout)



        # Giriş Butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_login)
        self.login_button.setDefault(True)
        layout.addWidget(self.login_button)

        # Mesaj Label
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def toggle_password(self, checked):
        mode = QLineEdit.Normal if checked else QLineEdit.Password
        self.password_input.setEchoMode(mode)



    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()



        try:
            kullanici: Kullanici = check_user_credentials(username, password)

            if kullanici:
                log_info(f"Giris basarili - Kullanici: {username}")
                self.message_label.setText("✅ Giriş başarılı, yönlendiriliyorsunuz...")
                self.message_label.setStyleSheet("color: green; font-weight: bold;")

                self.hide()
                self.main_screen = MainMenuScreen(kullanici)
                self.main_screen.show()
            else:
                log_warning(f"Giris basarisiz - Kullanici: {username}")
                self.message_label.setText("❌ Kullanıcı adı veya şifre hatalı.")
                self.message_label.setStyleSheet("color: red; font-weight: bold;")
                # Future: self.shake_widget(self) → input shake animation
        except Exception as e:
            log_warning(f"Giris sırasında hata: {e}")
            self.message_label.setText("⚠️ Giriş sırasında hata oluştu.")
            self.message_label.setStyleSheet("color: orange; font-weight: bold;")
