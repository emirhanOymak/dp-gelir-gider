from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QDateEdit, QPushButton, QMessageBox
from PySide6.QtCore import QDate
from db.queries.gider_queries import update_gider
from db.queries.odeme_queries import get_odeme_turleri, get_butce_kalemleri_by_odeme_id, get_hesap_adlari_by_kalem_id

class EditExpenseScreen(QWidget):
    def __init__(self, gider, on_update_callback=None):
        super().__init__()
        self.setWindowTitle("İşlem Düzenle")
        self.setGeometry(600, 300, 400, 350)
        self.gider = gider
        self.on_update_callback = on_update_callback
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI, sans-serif;
                font-size: 13px;
            }

            QFormLayout {
                padding: 10px;
            }

            QComboBox, QLineEdit, QDateEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #fdfdfd;
            }

            QPushButton {
                padding: 8px;
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #27ae60;
            }

            QLabel {
                font-weight: bold;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.odeme_cb = QComboBox()
        self.kalem_cb = QComboBox()
        self.hesap_cb = QComboBox()
        self.aciklama_input = QLineEdit(self.gider.aciklama)
        self.tarih_edit = QDateEdit(QDate.fromString(self.gider.tarih.strftime("%Y-%m-%d"), "yyyy-MM-dd"))
        self.tarih_edit.setCalendarPopup(True)
        self.tutar_input = QLineEdit(str(self.gider.tutar))

        self.odeme_cb.currentIndexChanged.connect(self.odeme_changed)
        self.kalem_cb.currentIndexChanged.connect(self.kalem_changed)

        form.addRow("Ödeme Türü:", self.odeme_cb)
        form.addRow("Bütçe Kalemi:", self.kalem_cb)
        form.addRow("Hesap Adı:", self.hesap_cb)
        form.addRow("Açıklama:", self.aciklama_input)
        form.addRow("Tarih:", self.tarih_edit)
        form.addRow("Tutar:", self.tutar_input)

        self.save_btn = QPushButton("Güncelle")
        self.save_btn.clicked.connect(self.update_expense)
        layout.addLayout(form)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)

        self.load_odeme_turleri()

    def load_odeme_turleri(self):
        self.odeme_list = get_odeme_turleri()
        for odeme in self.odeme_list:
            self.odeme_cb.addItem(odeme.ad, odeme.odemeTuruId)

        # önceki seçimleri yükle
        index = self.odeme_cb.findData(self.gider.odemeTuruId)
        if index != -1:
            self.odeme_cb.setCurrentIndex(index)

    def odeme_changed(self, index):
        self.kalem_cb.clear()
        if index < 0: return
        odeme_id = self.odeme_cb.currentData()
        self.kalem_list = get_butce_kalemleri_by_odeme_id(odeme_id)
        for kalem in self.kalem_list:
            self.kalem_cb.addItem(kalem.ad, kalem.butceKalemiId)
        idx = self.kalem_cb.findData(self.gider.butceKalemiId)
        if idx != -1: self.kalem_cb.setCurrentIndex(idx)

    def kalem_changed(self, index):
        self.hesap_cb.clear()
        if index < 0: return
        kalem_id = self.kalem_cb.currentData()
        self.hesap_list = get_hesap_adlari_by_kalem_id(kalem_id)
        for hesap in self.hesap_list:
            self.hesap_cb.addItem(hesap.ad, hesap.hesapAdiId)
        idx = self.hesap_cb.findData(self.gider.hesapAdiId)
        if idx != -1: self.hesap_cb.setCurrentIndex(idx)

    def update_expense(self):
        odeme_id = self.odeme_cb.currentData()
        kalem_id = self.kalem_cb.currentData()
        hesap_id = self.hesap_cb.currentData()
        aciklama = self.aciklama_input.text()
        tarih = self.tarih_edit.date().toString("yyyy-MM-dd")
        try:
            tutar = float(self.tutar_input.text())
        except ValueError:
            QMessageBox.warning(self, "Hata", "Tutar geçersiz.")
            return

        success = update_gider(self.gider.giderId, odeme_id, kalem_id, hesap_id, aciklama, tarih, tutar)
        if success:
            QMessageBox.information(self, "Başarılı", "Gider güncellendi.")
            if self.on_update_callback:
                self.on_update_callback()
            self.close()
        else:
            QMessageBox.critical(self, "Hata", "Güncelleme başarısız.")
