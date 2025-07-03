from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from gui.main_screen import MainScreen  # Gider ekranı
import os

class MainMenuScreen(QWidget):
    def __init__(self, kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.setWindowTitle("Ana Menü - Gelir & Gider Seçimi")
        self.setGeometry(500, 250, 350, 200)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        hosgeldin = QLabel(f"👋 Hoş geldiniz, {self.kullanici.kullaniciAdi} ({self.kullanici.rol.upper()})")
        hosgeldin.setAlignment(Qt.AlignCenter)
        hosgeldin.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(hosgeldin)

        self.giderler_btn = QPushButton("📉 Giderler")
        self.giderler_btn.setFixedHeight(40)
        self.giderler_btn.clicked.connect(self.giderleri_ac)
        layout.addWidget(self.giderler_btn)

        self.gelirler_btn = QPushButton("📈 Gelirler")
        self.gelirler_btn.setFixedHeight(40)
        self.gelirler_btn.setEnabled(False)  # Şimdilik pasif
        layout.addWidget(self.gelirler_btn)

        self.setLayout(layout)

    def giderleri_ac(self):
        self.hide()
        self.main_screen = MainScreen(kullanici=self.kullanici)
        self.main_screen.show()
