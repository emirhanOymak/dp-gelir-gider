from PySide6.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QListWidget, QLabel, QPushButton
from PySide6.QtCore import QDate
from PySide6.QtGui import QTextCharFormat, QBrush, QColor
from gui.add_expense_screen import AddExpenseScreen
from utils.logger import log_info

class CalendarViewScreen(QWidget):
    def __init__(self, giderler, on_gider_eklendi_callback=None):
        super().__init__()
        self.setWindowTitle("Takvim Görünümü")
        self.setGeometry(500, 200, 500, 500)

        self.giderler = giderler
        self.on_gider_eklendi_callback = on_gider_eklendi_callback
        self.gunluk_veriler = self.gruplandir_giderler()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.gunu_sec)
        layout.addWidget(self.calendar)

        self.renkli_gunleri_isaretle()

        self.label = QLabel("Günlük Giderler")
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.add_expense_btn = QPushButton("➕ Bu Güne Gider Ekle")
        self.add_expense_btn.clicked.connect(self.ac_gider_ekle_ekrani)
        layout.addWidget(self.add_expense_btn)

        self.setLayout(layout)
        self.gunu_sec()

    def gruplandir_giderler(self):
        grouped = {}
        for gider in self.giderler:
            gun = gider.tarih.date() if hasattr(gider.tarih, 'date') else gider.tarih
            if gun not in grouped:
                grouped[gun] = []
            grouped[gun].append(gider)
        return grouped

    def gunu_sec(self):
        secilen_tarih = self.calendar.selectedDate().toPython()
        self.list_widget.clear()

        giderler = self.gunluk_veriler.get(secilen_tarih, [])
        total = sum(g.tutar for g in giderler)
        self.label.setText(f"Günlük Giderler – Toplam: {total:.2f}₺")

        for gider in giderler:
            self.list_widget.addItem(f"{gider.aciklama} - {gider.tutar:.2f}₺")

    def renkli_gunleri_isaretle(self):
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(QColor("#b3d9ff")))  # Açık mavi arka plan

        for gun in self.gunluk_veriler.keys():
            qt_date = QDate(gun.year, gun.month, gun.day)
            self.calendar.setDateTextFormat(qt_date, fmt)

    def ac_gider_ekle_ekrani(self):
        secilen_tarih = self.calendar.selectedDate().toPython()

        self.expense_screen = AddExpenseScreen()
        self.expense_screen.date_input.setDate(QDate(secilen_tarih.year, secilen_tarih.month, secilen_tarih.day))
        self.expense_screen.gider_eklendi_callback = self.gider_eklendikten_sonra_yenile
        self.expense_screen.show()

    def gider_eklendikten_sonra_yenile(self):
        from db.queries.gider_queries import get_all_giderler
        self.giderler = get_all_giderler()
        self.gunluk_veriler = self.gruplandir_giderler()
        self.renkli_gunleri_isaretle()
        self.gunu_sec()
        if self.on_gider_eklendi_callback:
            self.on_gider_eklendi_callback()
            log_info(f"Takvimden gider eklendi")
