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

import os

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DP Muhasebe Paneli")
        self.setGeometry(400, 150, 1000, 600)
        self.setFixedSize(self.width(), self.height())
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.selected_gider_id = None
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

        for btn in [self.create_button, self.expense_button, self.edit_button, self.delete_button]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(35)

        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        self.menu_layout.addWidget(self.create_button)
        self.menu_layout.addWidget(self.expense_button)
        self.menu_layout.addWidget(self.edit_button)
        self.menu_layout.addWidget(self.delete_button)
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

        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        right_panel.setLayout(right_layout)

        right_layout.addWidget(QLabel("Gider Listesi"))
        right_layout.addWidget(self.table)

        # Ana Layout'a Ekle
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        # Buton Fonksiyonları
        self.create_button.clicked.connect(self.ac_yeni_yapi_ekrani)
        self.expense_button.clicked.connect(self.ac_yeni_gider_ekrani)
        self.delete_button.clicked.connect(self.delete_selected)
        self.edit_button.clicked.connect(self.ac_duzenleme_ekrani)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        self.giderler = get_all_giderler()
        for row_idx, gider in enumerate(self.giderler):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(gider.odemeTuru))
            self.table.setItem(row_idx, 1, QTableWidgetItem(gider.butceKalemi))
            self.table.setItem(row_idx, 2, QTableWidgetItem(gider.hesapAdi))
            self.table.setItem(row_idx, 3, QTableWidgetItem(gider.aciklama))
            self.table.setItem(row_idx, 4, QTableWidgetItem(gider.tarih.strftime("%Y-%m-%d")))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"{gider.tutar:.2f}"))

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
                QMessageBox.information(self, "Başarılı", "Kayıt silindi.")
                self.load_data()
                self.selected_gider_id = None
                self.edit_button.setEnabled(False)
                self.delete_button.setEnabled(False)
            else:
                QMessageBox.critical(self, "Hata", "Kayıt silinemedi.")

    def ac_yeni_yapi_ekrani(self):
        self.structure_screen = AddStructureScreen()
        self.structure_screen.show()

    def ac_yeni_gider_ekrani(self):
        self.expense_screen = AddExpenseScreen()
        self.expense_screen.gider_eklendi_callback = self.load_data
        self.expense_screen.show()

    def ac_duzenleme_ekrani(self):
        if self.selected_gider_id is None:
            return
        selected_gider = next((g for g in self.giderler if g.giderId == self.selected_gider_id), None)
        if selected_gider:
            self.edit_screen = EditExpenseScreen(selected_gider, self.load_data)
            self.edit_screen.show()
