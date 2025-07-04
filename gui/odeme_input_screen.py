from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QMessageBox
from PySide6.QtCore import QDate
from models.odeme import Odeme
from db.queries.gider_queries import get_gider_by_id
from db.queries.odeme_queries import update_status_and_kalan_tutar,add_odeme

class OdemeInputScreen(QWidget):
    def __init__(self, gider, refresh_callback):
        super().__init__()
        self.gider = gider
        self.refresh_callback = refresh_callback

        self.setWindowTitle("Ödeme Girişi")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Gider: {gider.aciklama}"))
        layout.addWidget(QLabel(f"Toplam Tutar: {gider.tutar:.2f} ₺"))

        if self.gider.kalanTutar is None:
            kalan_tutar = self.gider.tutar
        else:
            kalan_tutar = self.gider.kalanTutar

        odenen_toplam = self.gider.tutar - kalan_tutar
        layout.addWidget(QLabel(f"Kalan Tutar: {kalan_tutar:.2f} ₺"))

        # Ödeme Miktarı input
        layout.addWidget(QLabel("Ödeme Miktarı (₺):"))
        self.miktar_input = QLineEdit()
        layout.addWidget(self.miktar_input)

        # Ödeme Tarihi input
        layout.addWidget(QLabel("Ödeme Tarihi:"))
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        # Kaydet butonu
        self.save_btn = QPushButton("💾 Kaydet")
        self.save_btn.clicked.connect(self.kaydet)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def kaydet(self):
        try:
            miktar = float(self.miktar_input.text().replace(',', '.'))
            odeme_tarihi = self.date_input.date().toPython()
        except ValueError:
            QMessageBox.warning(self, "Hatalı Giriş", "Lütfen geçerli bir ödeme miktarı girin.")
            return

        # DB insert – Odeme tablosu
        odeme = Odeme(
            gider_id=self.gider.giderId,
            miktar=miktar,
            odeme_tarihi=odeme_tarihi
        )
        success = add_odeme(odeme)

        if not success:
            QMessageBox.critical(self, "Hata", "Ödeme kaydedilemedi.")
            return

        # Gider kalan ve status update (yeni toplam ödemeyi DB'den sum ile çekmek gerekebilir)
        update_success = update_status_and_kalan_tutar(
            self.gider.giderId,
            self.gider.tutar
        )

        if not update_success:
            QMessageBox.warning(self, "Uyarı", "Ödeme kaydedildi ancak kalan tutar/status güncellenemedi.")

        QMessageBox.information(self, "Başarılı", "Ödeme başarıyla kaydedildi.")
        self.refresh_callback()
        self.close()
