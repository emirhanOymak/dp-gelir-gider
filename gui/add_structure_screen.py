from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QLineEdit, QMessageBox, QDialog
)
from PySide6.QtGui import QIcon
from db.queries.odeme_queries import get_odeme_turleri, get_butce_kalemleri_by_odeme_id, get_hesap_adlari_by_kalem_id
from db.queries.structure_queries import create_odeme_turu, create_butce_kalemi, create_hesap_adi
import os

class AddStructureScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yapı Oluştur")
        self.setFixedSize(500, 300)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ödeme Türü
        layout.addWidget(QLabel("Ödeme Türü:"))
        self.odeme_cb = QComboBox()
        self.btn_add_odeme = QPushButton("➕ Yeni Ödeme Türü")
        self.btn_add_odeme.clicked.connect(lambda: self.popup_yeni_kayit("odeme"))
        layout.addLayout(self._row(self.odeme_cb, self.btn_add_odeme))

        # Bütçe Kalemi
        layout.addWidget(QLabel("Bütçe Kalemi:"))
        self.kalem_cb = QComboBox()
        self.btn_add_kalem = QPushButton("➕ Yeni Kalem")
        self.btn_add_kalem.clicked.connect(lambda: self.popup_yeni_kayit("kalem"))
        layout.addLayout(self._row(self.kalem_cb, self.btn_add_kalem))

        # Hesap Adı
        layout.addWidget(QLabel("Hesap Adı:"))
        self.hesap_cb = QComboBox()
        self.btn_add_hesap = QPushButton("➕ Yeni Hesap")
        self.btn_add_hesap.clicked.connect(lambda: self.popup_yeni_kayit("hesap"))
        layout.addLayout(self._row(self.hesap_cb, self.btn_add_hesap))

        # Kapat Butonu
        self.close_button = QPushButton("✅ Tamamla ve Kapat")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        # Etkileşim
        self.odeme_cb.currentIndexChanged.connect(self.load_kalemler)
        self.kalem_cb.currentIndexChanged.connect(self.load_hesaplar)

        self.load_odeme_turleri()

    def _row(self, combo, button):
        row = QHBoxLayout()
        combo.setMinimumWidth(250)
        row.addWidget(combo)
        row.addWidget(button)
        return row

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
        if index < 0: return
        odeme_id = self.odeme_cb.currentData()
        kalemler = get_butce_kalemleri_by_odeme_id(odeme_id)
        for item in kalemler:
            self.kalem_cb.addItem(item.ad, item.butceKalemiId)

    def load_hesaplar(self, index):
        self.hesap_cb.clear()
        if index < 0: return
        kalem_id = self.kalem_cb.currentData()
        hesaplar = get_hesap_adlari_by_kalem_id(kalem_id)
        for item in hesaplar:
            self.hesap_cb.addItem(item.ad, item.hesapAdiId)

    def popup_yeni_kayit(self, tur):
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni " + tur.capitalize())
        dialog.setFixedSize(300, 120)
        layout = QVBoxLayout()

        input_field = QLineEdit()
        input_field.setPlaceholderText(f"Yeni {tur} adı girin...")
        layout.addWidget(input_field)

        btn_ok = QPushButton("Ekle")
        layout.addWidget(btn_ok)
        dialog.setLayout(layout)

        def kaydet():
            text = input_field.text().strip()
            if not text:
                QMessageBox.warning(self, "Uyarı", "Boş değer girilemez.")
                return

            if tur == "odeme":
                create_odeme_turu(text)
                self.load_odeme_turleri()
            elif tur == "kalem":
                odeme_id = self.odeme_cb.currentData()
                if not odeme_id:
                    QMessageBox.warning(self, "Eksik Seçim", "Önce bir ödeme türü seçin.")
                    return
                create_butce_kalemi(text, odeme_id)
                self.load_kalemler(self.odeme_cb.currentIndex())
            elif tur == "hesap":
                kalem_id = self.kalem_cb.currentData()
                if not kalem_id:
                    QMessageBox.warning(self, "Eksik Seçim", "Önce bir bütçe kalemi seçin.")
                    return
                create_hesap_adi(text, kalem_id)
                self.load_hesaplar(self.kalem_cb.currentIndex())

            dialog.accept()

        btn_ok.clicked.connect(kaydet)
        dialog.exec()
