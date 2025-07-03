from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit,
    QPushButton, QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon
import os

from models.recursive_gider import RecursiveGider
from db.queries.recursive_gider_queries import add_recursive_gider
from utils.process_recursive import generate_giderler_from_recursive

from db.queries.odeme_queries import (
    get_odeme_turleri, get_butce_kalemleri_by_odeme_id, get_hesap_adlari_by_kalem_id
)

class AddRecursiveGiderScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Tekrarlı Gider")
        self.setFixedSize(500, 500)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        if os.path.exists(icon_path):
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

        # Başlangıç Tarihi
        layout.addWidget(QLabel("Başlangıç Tarihi:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        # Tutar
        layout.addWidget(QLabel("Tutar (₺):"))
        self.tutar_input = QLineEdit()
        self.tutar_input.setPlaceholderText("Örn: 5000")
        layout.addWidget(self.tutar_input)

        # Tekrar Sayısı
        layout.addWidget(QLabel("Tekrar Sayısı:"))
        self.tekrar_input = QLineEdit()
        self.tekrar_input.setPlaceholderText("Örn: 12")
        layout.addWidget(self.tekrar_input)

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
        if odeme_id is None:
            return
        kalemler = get_butce_kalemleri_by_odeme_id(odeme_id)
        for item in kalemler:
            self.kalem_cb.addItem(item.ad, item.butceKalemiId)

    def load_hesaplar(self, index):
        self.hesap_cb.clear()
        if index < 0:
            return
        kalem_id = self.kalem_cb.currentData()
        if kalem_id is None:
            return
        hesaplar = get_hesap_adlari_by_kalem_id(kalem_id)
        for item in hesaplar:
            self.hesap_cb.addItem(item.ad, item.hesapAdiId)

    def kaydet(self):
        try:
            odeme_id = self.odeme_cb.currentData()
            kalem_id = self.kalem_cb.currentData()
            hesap_id = self.hesap_cb.currentData()
            aciklama = self.aciklama_input.text()
            baslangic = self.date_input.date().toPython()
            tutar = float(self.tutar_input.text().replace(',', '.'))
            tekrar = int(self.tekrar_input.text())

            if None in (odeme_id, kalem_id, hesap_id) or not aciklama:
                QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
                return

            rg = RecursiveGider(
                ad=aciklama,
                toplam_tutar=tutar,
                baslangic_tarihi=baslangic,
                tekrar_sayisi=tekrar,
                odeme_turu_id=odeme_id,
                butce_kalemi_id=kalem_id,
                hesap_adi_id=hesap_id,
                aciklama=aciklama
            )

            # RecursiveGider'ı DB'ye ekle
            inserted_id = add_recursive_gider(rg)
            rg.recursiveGiderId = inserted_id

            # Giderleri oluştur
            generate_giderler_from_recursive(rg)

            QMessageBox.information(self, "Başarılı", "Tekrarlı gider başarıyla eklendi ve giderler oluşturuldu.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Beklenmedik bir hata oluştu: {e}")
