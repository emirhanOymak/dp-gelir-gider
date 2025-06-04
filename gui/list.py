# gui/entry_screen.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QComboBox, QVBoxLayout, QFormLayout,
    QDateEdit, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDate

class EntryScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gider Giriş Ekranı")
        self.setGeometry(600, 300, 400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Gider Türü
        self.gider_turu_cb = QComboBox()
        self.gider_turu_cb.addItem("Seçiniz")  # Geçici sabit veri
        self.gider_turu_cb.addItems(["Ulaşım", "Yemek", "Ofis Malzemeleri"])
        self.gider_turu_cb.currentIndexChanged.connect(self.on_gider_turu_changed)
        form.addRow(QLabel("Gider Türü:"), self.gider_turu_cb)

        # Hesap Adı
        self.hesap_cb = QComboBox()
        form.addRow(QLabel("Hesap Adı:"), self.hesap_cb)

        # Bütçe Kalemi
        self.kalem_cb = QComboBox()
        form.addRow(QLabel("Bütçe Kalemi:"), self.kalem_cb)

        # Tarih
        self.tarih_edit = QDateEdit()
        self.tarih_edit.setDate(QDate.currentDate())
        self.tarih_edit.setCalendarPopup(True)
        form.addRow(QLabel("Tarih:"), self.tarih_edit)

        # Tutar
        self.tutar_input = QLineEdit()
        self.tutar_input.setPlaceholderText("Örn: 150.75")
        form.addRow(QLabel("Tutar:"), self.tutar_input)

        # Kaydet Butonu
        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.kaydet)
        form.addRow(self.save_button)

        layout.addLayout(form)
        self.setLayout(layout)

    def on_gider_turu_changed(self, index):
        # Seçilen gider türüne göre hesap adlarını güncelle (şimdilik sabit)
        self.hesap_cb.clear()
        self.kalem_cb.clear()
        if index == 1:  # Ulaşım
            self.hesap_cb.addItems(["Yakıt", "Toplu Taşıma"])
        elif index == 2:  # Yemek
            self.hesap_cb.addItems(["Restoran", "Market"])
        elif index == 3:  # Ofis Malzemeleri
            self.hesap_cb.addItems(["Kırtasiye", "Elektronik"])

    def kaydet(self):
        gider_turu = self.gider_turu_cb.currentText()
        hesap = self.hesap_cb.currentText()
        kalem = self.kalem_cb.currentText()
        tarih = self.tarih_edit.date().toString("yyyy-MM-dd")
        tutar = self.tutar_input.text()

        # Basit validasyon
        if not gider_turu or not hesap or not tutar:
            QMessageBox.warning(self, "Eksik Veri", "Lütfen tüm alanları doldurun.")
            return

        try:
            tutar_float = float(tutar)
            QMessageBox.information(self, "Başarılı", f"Gider kaydedildi:\n{gider_turu} - {tutar_float} TL")
            # TODO: Veritabanına yaz
        except ValueError:
            QMessageBox.warning(self, "Hatalı Giriş", "Tutar sayısal bir değer olmalı.")
