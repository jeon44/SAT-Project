import sys
import os
from PyQt5 import QtWidgets, uic

# test1.py

UI_FILENAME = "untitled.ui"

class MainWindow(QtWidgets.QDialog):
    def __init__(self, ui_path):
        super().__init__()
        uic.loadUi(ui_path, self)

        self.mybutton1.clicked.connect(self.on_mybutton1_clicked)

    def on_mybutton1_clicked(self):
        print("Button clicked!")

def main():
    ui_path = os.path.join(os.path.dirname(__file__), UI_FILENAME)
    if not os.path.exists(ui_path):
        print(f"UI file not found: {ui_path}")
        sys.exit(1)
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(ui_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()