from UI.UI_Design import Window
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QToolTip, \
    QPushButton, QMessageBox, QDesktopWidget, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, Qt
from Others.logging_file import init_logger
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_logger("logging.txt")
    window = Window()

    sys.exit(app.exec_())



