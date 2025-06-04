import sys
from PySide6.QtWidgets import QApplication, QWidget
from gui.login import LoginScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Basit bir pencere oluştur
    window = LoginScreen()
    window.setWindowTitle("Data Platform - Muhasebe Programı")
    window.show()

    sys.exit(app.exec())
