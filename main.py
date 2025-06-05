import sys
from PySide6.QtWidgets import QApplication, QWidget
from gui.login_screen import LoginScreen
from db.connection import get_connection

def test_db_connection():
    conn = get_connection()
    if conn:
        print("✅ Veritabanı bağlantısı başarılı!")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Kullanici")
        result = cursor.fetchone()
        print(f"🔍 Kullanici tablosunda {result[0]} kayıt var.")
        conn.close()
    else:
        print("❌ Bağlantı kurulamadı.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_db_connection()
    # Basit bir pencere oluştur
    window = LoginScreen()
    window.setWindowTitle("Data Platform - Muhasebe Programı")
    window.show()

    sys.exit(app.exec())