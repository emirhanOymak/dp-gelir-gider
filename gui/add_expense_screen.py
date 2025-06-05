from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit,
    QPushButton, QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon
from db.queries.odeme_queries import (
    get_odeme_turleri, get_butce_kalemleri_by_odeme_id, get_hesap_adlari_by_kalem_id
)
from db.queries.gider_queries import add_gider
import os

class AddExpenseScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Gider Girişi")
        self.setFixedSize(500, 400)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ödeme Türü
        layout.addWidget(QLabel("Ödeme Türü:"))
        self.odeme_cb = QComboBox()
        layout.addWidget(self.odeme_cb)

        # Bütçe Kalemi
        layout.addWidget(QLabel("Bütçe Kalemi:"))
        self.kalem_cb = QComboBox()
        layout.addWidget(self.kalem_cb)

        # Hesap Adı
        layout.addWidget(QLabel("Hesap Adı:"))
        self.hesap_cb = QComboBox()
        layout.addWidget(self.hesap_cb)

        # Açıklama
        layout.addWidget(QLabel("Açıklama:"))
        self.aciklama_input = QLineEdit()
        layout.addWidget(self.aciklama_input)

        # Tarih
        layout.addWidget(QLabel("Tarih:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        # Tutar
        layout.addWidget(QLabel("Tutar (₺):"))
        self.tutar_input = QLineEdit()
        self.tutar_input.setPlaceholderText("Örn: 750.50")
        layout.addWidget(self.tutar_input)

        # Kaydet Butonu
        self.save_btn = QPushButton("💾 Kaydet")
        self.save_btn.clicked.connect(self.kaydet)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # Etkileşimler
        self.odeme_cb.currentIndexChanged.connect(self.load_kalemler)
        self.kalem_cb.currentIndexChanged.connect(self.load_hesaplar)

        self.load_odeme_turleri()

    def load_odeme_turleri(self):
        self.odeme_cb.clear()
        self.odeme_list = get_odeme_turleri()
        for item in self.odeme_list:
            self.odeme_cb.addItem(item.ad, item.odemeTuruId)
        self.kalem_cb.clear()
        self.hesap_cb.clear()

    def load_kalemler(self, index):
        self.kalem_cb.clear()
        self.hesap_cb.clear()
        if index < 0:
            return
        odeme_id = self.odeme_cb.currentData()
        kalemler = get_butce_kalemleri_by_odeme_id(odeme_id)
        for item in kalemler:
            self.kalem_cb.addItem(item.ad, item.butceKalemiId)

    def load_hesaplar(self, index):
        self.hesap_cb.clear()
        if index < 0:
            return
        kalem_id = self.kalem_cb.currentData()
        hesaplar = get_hesap_adlari_by_kalem_id(kalem_id)
        for item in hesaplar:
            self.hesap_cb.addItem(item.ad, item.hesapAdiId)

    def kaydet(self):
        try:
            odeme_id = self.odeme_cb.currentData()
            kalem_id = self.kalem_cb.currentData()
            hesap_id = self.hesap_cb.currentData()
            aciklama = self.aciklama_input.text()
            tarih = self.date_input.date().toString("yyyy-MM-dd")
            tutar = float(self.tutar_input.text())

            if None in (odeme_id, kalem_id, hesap_id) or not aciklama:
                QMessageBox.warning(self, "Eksik Bilgi", "Tüm alanları doldurun.")
                return

            success = add_gider(odeme_id, kalem_id, hesap_id, aciklama, tarih, tutar)
            if success:
                QMessageBox.information(self, "Başarılı", "Gider eklendi.")
                if self.gider_eklendi_callback:
                    self.gider_eklendi_callback()
                self.close()
            else:
                QMessageBox.critical(self, "Hata", "Veritabanı hatası oluştu.")
        except ValueError:
            QMessageBox.warning(self, "Hatalı Tutar", "Lütfen geçerli bir tutar girin.")
