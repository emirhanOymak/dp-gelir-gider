# list.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QComboBox, QVBoxLayout, QFormLayout,
    QDateEdit, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon
from db.queries import (
    get_odeme_turleri,
    get_butce_kalemleri_by_odeme_id,
    get_hesap_adlari_by_kalem_id,
    add_gider
)
import os

class EntryScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gider Giriş Ekranı")
        self.setGeometry(600, 300, 400, 350)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Gider Türü
        self.gider_turu_cb = QComboBox()
        self.gider_turu_cb.currentIndexChanged.connect(self.on_gider_turu_changed)
        form.addRow(QLabel("Ödeme Türü:"), self.gider_turu_cb)

        # Bütçe Kalemi
        self.kalem_cb = QComboBox()
        self.kalem_cb.currentIndexChanged.connect(self.on_kalem_changed)
        form.addRow(QLabel("Bütçe Kalemi:"), self.kalem_cb)

        # Hesap Adı
        self.hesap_cb = QComboBox()
        form.addRow(QLabel("Hesap Adı:"), self.hesap_cb)

        # Açıklama
        self.aciklama_input = QLineEdit()
        form.addRow(QLabel("Açıklama:"), self.aciklama_input)

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

        self.load_odeme_turleri()

    def load_odeme_turleri(self):
        self.gider_turu_cb.clear()
        self.odeme_turu_list = get_odeme_turleri()
        for id, ad in self.odeme_turu_list:
            self.gider_turu_cb.addItem(ad, id)

    def on_gider_turu_changed(self, index):
        self.kalem_cb.clear()
        self.hesap_cb.clear()

        if index < 0:
            return
        odeme_turu_id = self.gider_turu_cb.currentData()
        self.kalem_list = get_butce_kalemleri_by_odeme_id(odeme_turu_id)
        for id, ad in self.kalem_list:
            self.kalem_cb.addItem(ad, id)

    def on_kalem_changed(self, index):
        self.hesap_cb.clear()

        if index < 0:
            return
        kalem_id = self.kalem_cb.currentData()
        self.hesap_list = get_hesap_adlari_by_kalem_id(kalem_id)
        for id, ad in self.hesap_list:
            self.hesap_cb.addItem(ad, id)

    def kaydet(self):
        odeme_turu_id = self.gider_turu_cb.currentData()
        butce_kalemi_id = self.kalem_cb.currentData()
        hesap_adi_id = self.hesap_cb.currentData()
        aciklama = self.aciklama_input.text()
        tarih = self.tarih_edit.date().toString("yyyy-MM-dd")
        tutar_text = self.tutar_input.text()

        if None in (odeme_turu_id, butce_kalemi_id, hesap_adi_id) or not tutar_text:
            QMessageBox.warning(self, "Eksik Veri", "Lütfen tüm alanları doldurun.")
            return

        try:
            tutar = float(tutar_text)
        except ValueError:
            QMessageBox.warning(self, "Hatalı Giriş", "Tutar geçerli bir sayı olmalı.")
            return

        success = add_gider(odeme_turu_id, butce_kalemi_id, hesap_adi_id, aciklama, tarih, tutar)
        if success:
            QMessageBox.information(self, "Başarılı", "Gider başarıyla kaydedildi.")
            self.aciklama_input.clear()
            self.tutar_input.clear()
        else:
            QMessageBox.critical(self, "Hata", "Kayıt sırasında hata oluştu.")
