import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from db.queries.gider_queries import get_all_giderler
from collections import defaultdict
import datetime

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

        self.setLayout(layout)

        self.plot_and_list_data()

    def plot_and_list_data(self):
        giderler = get_all_giderler()

        # Ay bazlı toplama
        aylik_toplamlar = defaultdict(float)
        for gider in giderler:
            ay = gider.tarih.strftime("%Y-%m")
            aylik_toplamlar[ay] += float(gider.tutar)

        # Grafiği çiz
        ax = self.canvas.figure.subplots()
        ax.clear()
        aylar = sorted(aylik_toplamlar.keys())
        tutarlar = [aylik_toplamlar[ay] for ay in aylar]

        ax.bar(aylar, tutarlar)
        ax.set_title("Aylık Giderler")
        ax.set_xlabel("Ay")
        ax.set_ylabel("Tutar (₺)")
        ax.tick_params(axis='x', rotation=45)
        self.canvas.draw()

        # Tabloyu doldur
        self.table.setRowCount(len(aylik_toplamlar))
        for row, ay in enumerate(aylar):
            self.table.setItem(row, 0, QTableWidgetItem(ay))
            self.table.setItem(row, 1, QTableWidgetItem(f"{aylik_toplamlar[ay]:.2f}"))
