import sys

from PyQt5.QtWidgets import QApplication, QPushButton

from .ros import RclpyThread
from .window import MainWindow


def main(widget):
    app = QApplication(sys.argv)
    ros = RclpyThread()

    widget.init(ros.node())
    window = MainWindow()
    window.setCentralWidget(widget.widget)
    window.show()

    ros.exec()
    ret = app.exec_()
    ros.quit()
    sys.exit(ret)
