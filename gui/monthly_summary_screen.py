from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from db.queries.gider_queries import get_all_giderler
from collections import defaultdict
import datetime
import os
import openpyxl

class MonthlySummaryScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aylık Gider Özeti")
        self.setGeometry(400, 200, 800, 600)

        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title = QLabel("\u2728 Aylık Gider Grafiği ve Özeti")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.title)

        # Grafik Alanı
        self.canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.canvas)

        # Tablo Alanı
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Ay", "Toplam Gider (₺)"])
        layout.addWidget(self.table)

        # Excel'e Aktar Butonu
        self.export_button = QPushButton("📤 Excel'e Aktar")
        self.export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

        self.plot_and_list_data()

    def plot_and_list_data(self):
        self.giderler = get_all_giderler()

        # Ay bazlı toplama
        self.aylik_toplamlar = defaultdict(float)
        for gider in self.giderler:
            ay = gider.tarih.strftime("%Y-%m")
            self.aylik_toplamlar[ay] += float(gider.tutar)

        # Grafiği çiz
        ax = self.canvas.figure.subplots()
        ax.clear()
        aylar = sorted(self.aylik_toplamlar.keys())
        tutarlar = [self.aylik_toplamlar[ay] for ay in aylar]

        ax.bar(aylar, tutarlar)
        ax.set_title("Aylık Giderler")
        ax.set_xlabel("Ay")
        ax.set_ylabel("Tutar (₺)")
        ax.tick_params(axis='x', rotation=45)
        self.canvas.draw()

        # Tabloyu doldur
        self.table.setRowCount(len(self.aylik_toplamlar))
        for row, ay in enumerate(aylar):
            self.table.setItem(row, 0, QTableWidgetItem(ay))
            self.table.setItem(row, 1, QTableWidgetItem(f"{self.aylik_toplamlar[ay]:.2f}"))

    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Excel'e Kaydet", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Aylık Gider Özeti"

            # Başlık
            ws.append(["Ay", "Toplam Gider (₺)"])
            for ay, tutar in sorted(self.aylik_toplamlar.items()):
                ws.append([ay, round(tutar, 2)])

            wb.save(file_path)
            QMessageBox.information(self, "Başarılı", "Excel dosyası oluşturuldu.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya oluşturulamadı: {str(e)}")
