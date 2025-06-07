from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QMessageBox, QTableWidget, QTableWidgetItem
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from gui.add_structure_screen import AddStructureScreen
from gui.add_expense_screen import AddExpenseScreen
from db.queries.gider_queries import get_all_giderler, delete_gider
from gui.edit_expense_screen import EditExpenseScreen
from utils.logger import log_info, log_error
from gui.log_viewer_screen import LogViewerScreen
from gui.monthly_summary_screen import MonthlySummaryScreen
from openpyxl import Workbook
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QDateEdit, QLineEdit
from PySide6.QtCore import QDate
from gui.calendar_view_screen import CalendarViewScreen
import pandas as pd
from PySide6.QtWidgets import QFileDialog
from db.queries.gider_queries import add_gider
from db.queries.odeme_queries import (
    get_odeme_turleri,
    get_butce_kalemleri,
    get_hesap_adlari
)


import os

class MainScreen(QWidget):
    def __init__(self , kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.setWindowTitle("DP Muhasebe Paneli")
        self.setGeometry(400, 150, 1000, 600)
        self.setFixedSize(self.width(), self.height())
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.selected_gider_id = None
        self.filtered_giderler = []
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # ========== Sol Menü ==========
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(15)

        title_label = QLabel("  Data Platform")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.menu_layout.addWidget(title_label)

        # Butonlar
        self.create_button = QPushButton("➕ Yapı Ekle")
        self.expense_button = QPushButton("💸 Yeni Gider Ekle")
        self.edit_button = QPushButton("✏️ İşlem Düzenle")
        self.delete_button = QPushButton("🗑️ İşlemi Sil")
        self.log_button = QPushButton("📄 Logları Gör")
        self.summary_button = QPushButton("📊 Aylık Özet")
        self.export_button = QPushButton("📤 Giderleri Excel’e Aktar")
        self.import_button = QPushButton("📥 Excel'den İçe Aktar")
        self.calendar_button = QPushButton("📅 Takvim Görünümüne Geç")

        # Rol bazlı buton kısıtlamaları
        if self.kullanici.rol == "kullanici":
            self.delete_button.setEnabled(False)  # sadece admin silebilir
            self.log_button.setEnabled(False)

        if self.kullanici.rol == "izleyici":
            self.expense_button.setEnabled(False)
            self.create_button.setEnabled(False)
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.log_button.setEnabled(False)

        for btn in [self.create_button, self.expense_button, self.edit_button, self.delete_button,self.log_button, self.summary_button,self.export_button,self.import_button,self.calendar_button]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(35)

        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        self.menu_layout.addWidget(self.create_button)
        self.menu_layout.addWidget(self.expense_button)
        self.menu_layout.addWidget(self.edit_button)
        self.menu_layout.addWidget(self.delete_button)
        self.menu_layout.addWidget(self.log_button)
        self.menu_layout.addWidget(self.summary_button)
        self.menu_layout.addWidget(self.export_button)
        self.menu_layout.addWidget(self.import_button)
        self.menu_layout.addWidget(self.calendar_button)
        self.menu_layout.addStretch()

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/icon.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaledToWidth(80, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(logo_label)

        # Sol Panel Stil
        left_panel = QWidget()
        left_panel.setLayout(self.menu_layout)
        left_panel.setFixedWidth(200)
        left_panel.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
                font-size: 13px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3e5871;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        # ========== Sağ Panel: Tablo ==========
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Ödeme Türü", "Bütçe Kalemi", "Hesap Adı", "Açıklama", "Tarih", "Tutar"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f9f9f9;
                alternate-background-color: #e8f0fe;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.table.cellClicked.connect(self.on_row_selected)

        # Kullanıcı bilgi etiketi
        user_info_label = QLabel(f"Giriş Yapan: {self.kullanici.kullaniciAdi}  ({self.kullanici.rol.upper()})")

        # Rol bazlı renk ayarı
        if self.kullanici.rol == "admin":
            user_info_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
        elif self.kullanici.rol == "kullanici":
            user_info_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
        else:
            user_info_label.setStyleSheet("color: gray; font-weight: bold; font-size: 14px;")

        # Ekrana ekle


        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        right_panel.setLayout(right_layout)
        right_layout.addWidget(user_info_label)
        right_layout.addWidget(QLabel("Gider Listesi"))

        # Filtre Alanları
        filter_layout = QHBoxLayout()

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setDate(QDate.currentDate().addMonths(-1))  # Varsayılan: bir ay geriden başla
        filter_layout.addWidget(QLabel("Başlangıç Tarihi:"))
        filter_layout.addWidget(self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(QLabel("Bitiş Tarihi:"))
        filter_layout.addWidget(self.end_date)

        self.aciklama_input = QLineEdit()
        self.aciklama_input.setPlaceholderText("Açıklama içeriği")
        filter_layout.addWidget(QLabel("Açıklama:"))
        filter_layout.addWidget(self.aciklama_input)

        self.filter_button = QPushButton("🔍 Filtrele")
        self.filter_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(self.filter_button)

        self.reset_button = QPushButton("♻️ Tümünü Göster")
        self.reset_button.clicked.connect(self.load_data)
        filter_layout.addWidget(self.reset_button)

        right_layout.addLayout(filter_layout)

        right_layout.addWidget(self.table)

        # Ana Layout'a Ekle
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        # Buton Fonksiyonları
        self.create_button.clicked.connect(self.ac_yeni_yapi_ekrani)
        self.expense_button.clicked.connect(self.ac_yeni_gider_ekrani)
        self.delete_button.clicked.connect(self.delete_selected)
        self.edit_button.clicked.connect(self.ac_duzenleme_ekrani)
        self.log_button.clicked.connect(self.ac_log_ekrani)
        self.summary_button.clicked.connect(self.ac_aylik_ozet_ekrani)
        self.export_button.clicked.connect(self.export_to_excel)
        self.import_button.clicked.connect(self.excelden_aktar)
        self.calendar_button.clicked.connect(self.ac_takvim_ekrani)

        self.load_data()

    def load_data(self, filtered=False):
        self.table.setRowCount(0)
        source = self.filtered_giderler if filtered else get_all_giderler()
        self.giderler = source if not filtered else self.giderler  # Ana listeyi sadece ilk yüklemede güncelle

        for row_idx, gider in enumerate(source):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(gider.odemeTuru))
            self.table.setItem(row_idx, 1, QTableWidgetItem(gider.butceKalemi))
            self.table.setItem(row_idx, 2, QTableWidgetItem(gider.hesapAdi))
            self.table.setItem(row_idx, 3, QTableWidgetItem(gider.aciklama))
            self.table.setItem(row_idx, 4, QTableWidgetItem(gider.tarih.strftime("%Y-%m-%d")))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"{gider.tutar:.2f}"))

    def apply_filters(self):
        start_date = self.start_date.date().toPython()
        end_date = self.end_date.date().toPython()
        search_text = self.aciklama_input.text().lower()

        self.filtered_giderler = [
            gider for gider in self.giderler
            if start_date <= gider.tarih <= end_date and search_text in gider.aciklama.lower()
        ]
        self.load_data(filtered=True)

    def on_row_selected(self, row, _column):
        self.selected_gider_id = self.giderler[row].giderId
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def delete_selected(self):
        if self.selected_gider_id is None:
            return
        confirm = QMessageBox.question(self, "Silme Onayı", "Bu işlemi silmek istediğinize emin misiniz?")
        if confirm == QMessageBox.Yes:
            success = delete_gider(self.selected_gider_id)
            if success:
                log_info(f"Gider silindi - ID: {self.selected_gider_id}")
                QMessageBox.information(self, "Başarılı", "Kayıt silindi.")
                self.load_data()
                self.selected_gider_id = None
                self.edit_button.setEnabled(False)
                self.delete_button.setEnabled(False)
            else:
                log_error("Gider silinemedi", f"ID: {self.selected_gider_id}")
                QMessageBox.critical(self, "Hata", "Kayıt silinemedi.")

    def ac_yeni_yapi_ekrani(self):
        self.structure_screen = AddStructureScreen()
        self.structure_screen.show()

    def ac_yeni_gider_ekrani(self):
        self.expense_screen = AddExpenseScreen()
        self.expense_screen.gider_eklendi_callback = self.load_data
        self.expense_screen.show()

    def ac_log_ekrani(self):
        self.log_viewer = LogViewerScreen()
        self.log_viewer.show()

    def ac_aylik_ozet_ekrani(self):
        self.ozet_ekrani = MonthlySummaryScreen()
        self.ozet_ekrani.show()

    def ac_takvim_ekrani(self):
        self.calendar_screen = CalendarViewScreen(
            self.giderler,
            on_gider_eklendi_callback=self.load_data
        )
        self.calendar_screen.show()

    def export_to_excel(self):
        export_list = self.filtered_giderler if self.filtered_giderler else self.giderler

        if not export_list:
            QMessageBox.warning(self, "Uyarı", "Aktarılacak gider verisi bulunamadı.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Excel Dosyası Kaydet", "giderler.xlsx", "Excel Dosyası (*.xlsx)")
        if not path:
            return

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Giderler"

            # Başlıklar
            ws.append(["Ödeme Türü", "Bütçe Kalemi", "Hesap Adı", "Açıklama", "Tarih", "Tutar"])

            # Gider verileri
            for gider in export_list:
                ws.append([
                    gider.odemeTuru,
                    gider.butceKalemi,
                    gider.hesapAdi,
                    gider.aciklama,
                    gider.tarih.strftime("%Y-%m-%d"),
                    float(gider.tutar)
                ])

            wb.save(path)
            QMessageBox.information(self, "Başarılı", f"Giderler başarıyla kaydedildi:\n{path}")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Excel aktarımı sırasında bir hata oluştu:\n{str(e)}")

    def excelden_aktar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Excel Dosyası Seç", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)

            # Gerekli lookup tablolarını al
            odeme_lookup = {x.ad: x.odemeTuruId for x in get_odeme_turleri()}
            kalem_lookup = {x.ad: x.butceKalemiId for x in get_butce_kalemleri()}
            hesap_lookup = {x.ad: x.hesapAdiId for x in get_hesap_adlari()}

            eklenen = 0
            for _, row in df.iterrows():
                odeme_id = odeme_lookup.get(str(row["ödeme türü"]).strip())
                kalem_id = kalem_lookup.get(str(row["bütçe kalemi"]).strip())
                hesap_id = hesap_lookup.get(str(row["hesap adı"]).strip())
                aciklama = str(row["açıklama"])
                tarih = str(pd.to_datetime(row["tarih"]).date())
                tutar = float(row["tutar"])

                if None in (odeme_id, kalem_id, hesap_id):
                    continue  # geçersiz eşleşme

                if add_gider(odeme_id, kalem_id, hesap_id, aciklama, tarih, tutar):
                    eklenen += 1

            QMessageBox.information(self, "Başarılı", f"{eklenen} gider başarıyla eklendi.")
            self.load_data()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya okunamadı veya işlem yapılamadı.\n\n{str(e)}")

    def ac_duzenleme_ekrani(self):
        if self.selected_gider_id is None:
            return
        selected_gider = next((g for g in self.giderler if g.giderId == self.selected_gider_id), None)
        if selected_gider:
            self.edit_screen = EditExpenseScreen(selected_gider, self.load_data)
            self.edit_screen.show()
