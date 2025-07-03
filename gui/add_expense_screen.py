from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit,
    QPushButton, QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon
# --- YENİ ---
# Tekrarlı gider ekleme ekranımızı içeri aktarıyoruz
from gui.recursive_gider_screen import AddRecursiveGiderScreen
# --- BİTTİ ---
from db.queries.odeme_queries import (
    get_odeme_turleri, get_butce_kalemleri_by_odeme_id, get_hesap_adlari_by_kalem_id
)
from db.queries.gider_queries import add_gider
import os
from utils.logger import log_info, log_error

class AddExpenseScreen(QWidget):
    # Orijinal yapıya sadık kalmak için callback parametresini ekliyoruz.
    def __init__(self, gider_eklendi_callback=None):
        super().__init__()
        self.setWindowTitle("Yeni Gider Girişi")
        self.setFixedSize(500, 420) # Pencereyi biraz büyüttük
        self.gider_eklendi_callback = gider_eklendi_callback

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ödeme Türü, Bütçe Kalemi vb. alanlar (Değişiklik yok)
        layout.addWidget(QLabel("Ödeme Türü:"))
        self.odeme_cb = QComboBox()
        layout.addWidget(self.odeme_cb)
        layout.addWidget(QLabel("Bütçe Kalemi:"))
        self.kalem_cb = QComboBox()
        layout.addWidget(self.kalem_cb)
        layout.addWidget(QLabel("Hesap Adı:"))
        self.hesap_cb = QComboBox()
        layout.addWidget(self.hesap_cb)
        layout.addWidget(QLabel("Açıklama:"))
        self.aciklama_input = QLineEdit()
        layout.addWidget(self.aciklama_input)
        layout.addWidget(QLabel("Tarih:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)
        layout.addWidget(QLabel("Tutar (₺):"))
        self.tutar_input = QLineEdit()
        self.tutar_input.setPlaceholderText("Örn: 750.50")
        layout.addWidget(self.tutar_input)

        button_layout = QHBoxLayout()

        self.recursive_btn = QPushButton("🔁 Tekrarlı Gider Tanımla")
        self.recursive_btn.setToolTip("Bu gideri bir kurala bağlamak için (örn: kredi taksiti, kira) tıklayın.")
        self.recursive_btn.clicked.connect(self.open_recursive_gider_screen)
        button_layout.addWidget(self.recursive_btn) # Butonu yatay layout'a ekle

        self.save_btn = QPushButton("💾 Kaydet")
        self.save_btn.clicked.connect(self.kaydet)
        button_layout.addWidget(self.save_btn) # Mevcut butonu da yatay layout'a ekle

        # Ana dikey layout'a butonları içeren yatay layout'u ekliyoruz
        layout.addLayout(button_layout)
        # --- BİTTİ ---

        self.setLayout(layout)

        # Etkileşimler
        self.odeme_cb.currentIndexChanged.connect(self.load_kalemler)
        self.kalem_cb.currentIndexChanged.connect(self.load_hesaplar)
        self.load_odeme_turleri()

    # --- YENİ ---
    # Tekrarlı gider ekranını açan fonksiyon
    def open_recursive_gider_screen(self):
        # Pencereyi bir değişkende tutarak çöp toplayıcı tarafından silinmesini engelliyoruz
        self.recursive_gider_window = AddRecursiveGiderScreen()
        self.recursive_gider_window.show()
    # --- BİTTİ ---

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
        if odeme_id is None: return
        kalemler = get_butce_kalemleri_by_odeme_id(odeme_id)
        for item in kalemler:
            self.kalem_cb.addItem(item.ad, item.butceKalemiId)

    def load_hesaplar(self, index):
        self.hesap_cb.clear()
        if index < 0:
            return
        kalem_id = self.kalem_cb.currentData()
        if kalem_id is None: return
        hesaplar = get_hesap_adlari_by_kalem_id(kalem_id)
        for item in hesaplar:
            self.hesap_cb.addItem(item.ad, item.hesapAdiId)

    def kaydet(self):
        try:
            odeme_id = self.odeme_cb.currentData()
            kalem_id = self.kalem_cb.currentData()
            hesap_id = self.hesap_cb.currentData()
            aciklama = self.aciklama_input.text()
            tarih = self.date_input.date().toPython() # toPython() kullanmak daha güvenli
            tutar_str = self.tutar_input.text().replace(',', '.') # Virgülü noktaya çevir
            tutar = float(tutar_str)

            if None in (odeme_id, kalem_id, hesap_id) or not aciklama:
                QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm kategori ve açıklama alanlarını doldurun.")
                return

            from models.gider import Gider
            new_gider = Gider(
                odeme_turu_id=odeme_id,
                butce_kalemi_id=kalem_id,
                hesap_adi_id=hesap_id,
                aciklama=aciklama,
                tarih=tarih,
                tutar=tutar
            )

            success = add_gider(new_gider)
            if success:
                log_info(f"Gider eklendi - Tutar: {tutar}, Aciklama: {aciklama}")
                QMessageBox.information(self, "Basarili", "Gider başarıyla eklendi.")
                if self.gider_eklendi_callback:
                    self.gider_eklendi_callback()
                self.close()
            else:
                log_error("Gider eklenemedi", "Veritabanı hatası")
                QMessageBox.critical(self, "Hata", "Gider eklenirken bir veritabanı hatası oluştu.")
        except ValueError:
            log_error("Gider eklenirken hata", "Geçersiz tutar formatı")
            QMessageBox.warning(self, "Hatalı Tutar", "Lütfen geçerli bir sayısal tutar girin (örn: 750.50).")
        except Exception as e:
            log_error("Gider eklenirken beklenmedik hata", str(e))
            QMessageBox.critical(self, "Beklenmedik Hata", f"Beklenmedik bir hata oluştu: {e}")