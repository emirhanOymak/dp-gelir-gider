from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QComboBox, QHBoxLayout
from PySide6.QtCore import Qt
import os

class LogViewerScreen(QWidget):
    def __init__(self, log_file_path="hata_kayitlari.log"):
        super().__init__()
        self.setWindowTitle("Log Görüntüleyici")
        self.setGeometry(500, 200, 800, 500)
        self.log_file_path = log_file_path
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Filtre seçici
        self.filter_box = QComboBox()
        self.filter_box.addItems(["Tüm Loglar", "INFO", "WARNING", "ERROR"])
        self.filter_box.currentIndexChanged.connect(self.load_logs)

        layout.addWidget(self.filter_box)

        # Log alanı
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        # Butonlar
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("🔄 Yenile")
        self.refresh_button.clicked.connect(self.load_logs)

        self.clear_button = QPushButton("🧹 Temizle")
        self.clear_button.clicked.connect(self.clear_logs)

        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.load_logs()

    def clear_logs(self):
        try:
            with open(self.log_file_path, "w") as file:
                file.write("")  # Dosyayı temizle
            self.text_area.setPlainText("🧼 Log dosyası temizlendi.")
            self.load_logs()
        except Exception as e:
            self.text_area.setPlainText(f"❌ Log dosyası silinemedi:\n{str(e)}")

    def load_logs(self):
        if os.path.exists(self.log_file_path):
            try:
                with open(self.log_file_path, "r", encoding="utf-8", errors="replace") as file:
                    logs = file.readlines()

                selected_filter = self.filter_box.currentText()

                if selected_filter != "Tüm Loglar":
                    logs = [line for line in logs if f"- {selected_filter} -" in line]

                self.text_area.setPlainText("".join(logs) if logs else "🔍 Seçilen filtreye ait log bulunamadı.")
            except Exception as e:
                self.text_area.setPlainText(f"❌ Log dosyası okunamadı:\n{str(e)}")
        else:
            self.text_area.setPlainText("📂 Log dosyası bulunamadı.")
