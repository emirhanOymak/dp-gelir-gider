from PySide6.QtWidgets import (
    QWidget, QLabel, QComboBox, QVBoxLayout, QFormLayout,
    QDateEdit, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon
from db.queries import (
    get_odeme_turleri,
    get_butce_kalemleri_by_odeme_id,
    get_hesap_adlari_by_kalem_id,
    add_gider, get_all_giderler, delete_gider
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

        # Kayıtları Gör Butonu
        self.list_button = QPushButton("Kayıtları Gör")
        self.list_button.clicked.connect(self.gider_listesini_ac)
        form.addRow(self.list_button)

        layout.addLayout(form)
        self.setLayout(layout)

        self.load_odeme_turleri()


    def load_odeme_turleri(self):
        self.gider_turu_cb.clear()
        self.odeme_turu_list = get_odeme_turleri()
        for id, ad in self.odeme_turu_list:
            self.gider_turu_cb.addItem(ad, id)

    def gider_listesini_ac(self):
        self.list_screen = GiderListesi()
        self.list_screen.show()

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

class GiderListesi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gider Listesi")
        self.setGeometry(600, 300, 800, 400)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.load_data()

    def load_data(self):
        giderler = get_all_giderler()
        self.table.setRowCount(len(giderler))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Ödeme Türü", "Bütçe Kalemi", "Hesap Adı", "Açıklama", "Tarih", "Tutar", "", ""
        ])

        for row_idx, row_data in enumerate(giderler):
            gider_id = row_data[0]
            for col_idx, value in enumerate(row_data[1:]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            sil_btn = QPushButton("Sil")
            sil_btn.clicked.connect(lambda _, id=gider_id: self.sil_gider(id))
            self.table.setCellWidget(row_idx, 6, sil_btn)

            guncelle_btn = QPushButton("Güncelle")
            self.table.setCellWidget(row_idx, 7, guncelle_btn)

    def sil_gider(self, gider_id):
        reply = QMessageBox.question(self, "Silme Onayı", "Bu kaydı silmek istiyor musunuz?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            success = delete_gider(gider_id)
            if success:
                QMessageBox.information(self, "Silindi", "Kayıt başarıyla silindi.")
                self.load_data()
            else:
                QMessageBox.critical(self, "Hata", "Kayıt silinemedi.")