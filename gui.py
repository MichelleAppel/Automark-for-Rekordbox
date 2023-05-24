import sys
from PyQt5.QtWidgets import QApplication
from gui.app_window import AppWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    # window.load_defaults()
    window.run()
    sys.exit(app.exec_())
