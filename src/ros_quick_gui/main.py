import sys

from PyQt5.QtWidgets import QApplication, QPushButton

from .ros import RclpyThread
from .window import MainWindow


def main():
    app = QApplication(sys.argv)
    ros = RclpyThread()
    win = MainWindow()
    win.setCentralWidget(QPushButton("Hello"))
    win.show()
    ret = app.exec_()
    ros.quit()
    sys.exit(ret)
