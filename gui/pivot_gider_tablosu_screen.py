from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QApplication, QComboBox, QLabel, QHBoxLayout

from PySide6.QtGui import QFont, QColor, QBrush
from PySide6.QtCore import Qt
from db.queries.gider_queries import get_all_giderler
import pandas as pd
import datetime


import pandas as pd

def create_pivot_gider_tablosu(giderler, yil=2025, ay=1):
    # Giderleri DataFrame'e aktar
    rows = []
    for gider in giderler:
        try:
            tarih = pd.to_datetime(gider.tarih).strftime("%Y-%m-%d")
        except Exception:
            tarih = str(gider.tarih)
        rows.append({
            'Gider': gider.odemeTuru,
            'Bütçe Kalemi': gider.butceKalemi,
            'Hesap Adı': gider.hesapAdi,
            'Açıklama': gider.aciklama,
            'Tarih': tarih,
            'Tutar': gider.tutar
        })
    df = pd.DataFrame(rows)


    if df.empty:
        columns = ["Gider", "Bütçe Kalemi", "Hesap Adı", "Açıklama"] + [f"2025-01-{str(day).zfill(2)}" for day in range(1, 32)]
        return pd.DataFrame(columns=columns)

    df["Tarih"] = pd.to_datetime(df["Tarih"])
    df = df[(df["Tarih"].dt.year == yil) & (df["Tarih"].dt.month == ay)]

    days = pd.date_range(f"{yil}-{ay:02d}-01", f"{yil}-{ay:02d}-{31 if ay in [1,3,5,7,8,10,12] else 30 if ay != 2 else 28}")
    day_sutunlari = [d.strftime("%Y-%m-%d") for d in days]



    # Pivot tablo oluştur


    pivot = pd.pivot_table(
        df,
        index=["Gider", "Bütçe Kalemi", "Hesap Adı", "Açıklama"],
        columns=df["Tarih"].dt.strftime("%Y-%m-%d"),
        values="Tutar",
        aggfunc="sum",
        fill_value=0
    ).reset_index()


    for day in day_sutunlari:
        if day not in pivot.columns:
            pivot[day] = 0
    columns = ["Gider", "Bütçe Kalemi", "Hesap Adı", "Açıklama"] + day_sutunlari
    pivot = pivot[columns]

    # Nihai tablo: Satırları gruplara böl, toplamları ekle
    final_rows = []
    for gider, group_gider in pivot.groupby("Gider", sort=False):
        first_gider = True
        for butce_kalemi, group_butce in group_gider.groupby("Bütçe Kalemi", sort=False):
            # Her bütçe kalemi öncesinde boş satır ekle
            if not first_gider or final_rows:
                final_rows.append(["", "", "", ""] + [""]*len(day_sutunlari))
            # İlk Gider satırı (sadece Gider adı, diğerleri boş)
            if first_gider:
                final_rows.append([gider, "", "", ""] + [""]*len(day_sutunlari))
                first_gider = False
            # Bütçe kalemi satırları
            first_butce = True
            for _, row in group_butce.iterrows():
                row_gider = ""
                row_butce = butce_kalemi if first_butce else ""
                final_rows.append([row_gider, row_butce, row["Hesap Adı"], row["Açıklama"]] + [row[day] for day in day_sutunlari])
                first_butce = False
            # TOPLAM satırı
            toplam = ["", butce_kalemi, "", "TOPLAM"] + [group_butce[day].sum() for day in day_sutunlari]
            final_rows.append(toplam)
    df_final = pd.DataFrame(final_rows, columns=columns)
    return df_final



class PivotGiderTablosuScreen(QWidget):
    def __init__(self, yil=2025, ay=1):
        super().__init__()
        self.setWindowTitle("Pivot Gider Tablosu - {} {}".format(self.get_month_name(ay), yil))
        self.resize(1900, 900)
        self.setMinimumWidth(1600)
        self.setMinimumHeight(800)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        ay_secici_layout = QHBoxLayout()
        self.ay_label = QLabel("Ay:")
        ay_secici_layout.addWidget(self.ay_label)
        self.ay_combo = QComboBox()
        self.aylar = [
            ("Ocak", 1), ("Şubat", 2), ("Mart", 3), ("Nisan", 4), ("Mayıs", 5), ("Haziran", 6),
            ("Temmuz", 7), ("Ağustos", 8), ("Eylül", 9), ("Ekim", 10), ("Kasım", 11), ("Aralık", 12)
        ]
        for ad, _num in self.aylar:
            self.ay_combo.addItem(ad)
        self.ay_combo.setCurrentIndex(ay - 1)
        self.ay_combo.currentIndexChanged.connect(self.ay_degisti)
        ay_secici_layout.addWidget(self.ay_combo)
        ay_secici_layout.addStretch()
        self.layout.addLayout(ay_secici_layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Export butonu
        self.export_btn = QPushButton("Excel'e Aktar")
        self.export_btn.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.export_btn, alignment=Qt.AlignRight)

        self.secili_yil = yil
        self.secili_ay = ay
        self.load_pivot_data(self.secili_yil, self.secili_ay)

    def get_month_name(self, ay):
        aylar = [
            "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
            "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
        ]
        return aylar[ay - 1]

    def ay_degisti(self):
        secili_index = self.ay_combo.currentIndex()
        self.secili_ay = self.aylar[secili_index][1]
        self.setWindowTitle(f"Pivot Gider Tablosu - {self.get_month_name(self.secili_ay)} {self.secili_yil}")
        self.load_pivot_data(self.secili_yil, self.secili_ay)

    def load_pivot_data(self, yil, ay):
        giderler = get_all_giderler()
        df_pivot = create_pivot_gider_tablosu(giderler, yil, ay)

        self.table.setColumnCount(df_pivot.shape[1])
        self.table.setRowCount(df_pivot.shape[0])
        self.table.setHorizontalHeaderLabels(df_pivot.columns)

        font_bold = QFont()
        font_bold.setBold(True)

        RENK_MAVI = QColor("#d6eaf8")
        RENK_SARI = QColor("#ffffb3")
        RENK_BEYAZ = QColor("#ffffff")
        RENK_YESIL = QColor("#b7f7b5")  # Açık yeşil

        col_names = list(df_pivot.columns)
        gun_col_start = col_names.index("Açıklama") + 1
        gun_col_indexes = range(gun_col_start, len(col_names))

        for row in range(df_pivot.shape[0]):
            satir = df_pivot.iloc[row]
            is_toplam = str(satir["Açıklama"]).upper() == "TOPLAM"
            is_bosluk = all(str(satir[col]).strip() == "" for col in ["Gider", "Bütçe Kalemi", "Hesap Adı", "Açıklama"])

            if is_bosluk:
                arka_plan = QBrush(RENK_BEYAZ)
            elif is_toplam:
                arka_plan = QBrush(RENK_SARI)
            else:
                arka_plan = QBrush(RENK_MAVI)

            for row in range(df_pivot.shape[0]):
                satir = df_pivot.iloc[row]
                is_toplam = str(satir["Açıklama"]).upper() == "TOPLAM"
                is_bosluk = all(
                    str(satir[col]).strip() == "" for col in ["Gider", "Bütçe Kalemi", "Hesap Adı", "Açıklama"])

                if is_bosluk:
                    arka_plan = QBrush(RENK_BEYAZ)
                elif is_toplam:
                    arka_plan = QBrush(RENK_SARI)
                else:
                    arka_plan = QBrush(RENK_MAVI)

                for col in range(df_pivot.shape[1]):
                    value = df_pivot.iat[row, col]
                    item = QTableWidgetItem(
                        "" if pd.isnull(value)
                        else str(int(value)) if isinstance(value, (float, int)) and value != "" else str(value)
                    )

                    # TOPLAM satırında "Bütçe Kalemi" hücresi boş olsun
                    if is_toplam and col == 1:
                        item.setText("")

                    # Gün hücresi ve değer 0 değilse: yeşil (sadece TOPLAM olmayanlarda)
                    if not is_toplam and col in gun_col_indexes:
                        try:
                            val = float(value)
                        except:
                            val = 0
                        if val != 0:
                            item.setBackground(QBrush(RENK_YESIL))
                        else:
                            item.setBackground(arka_plan)
                    else:
                        item.setBackground(arka_plan)

                    # Kalın font atamaları
                    if col == 0 and str(value).strip() != "":
                        item.setFont(font_bold)
                    elif is_toplam:
                        item.setFont(font_bold)

                    self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

    def export_to_excel(self):
        df = self.get_current_table_as_df()
        path, _ = QFileDialog.getSaveFileName(self, "Excel'e Aktar", "pivot_giderler_ocak2025.xlsx", "Excel Files (*.xlsx)")
        if path:
            try:
                df.to_excel(path, index=False)
            except Exception as e:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Hata", f"Excel aktarımı başarısız: {str(e)}")

    def get_current_table_as_df(self):
        cols = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return pd.DataFrame(data, columns=cols)

