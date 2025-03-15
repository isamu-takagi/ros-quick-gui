from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROS Quick GUI")
        self.resize(250, 150)
        self.move(300, 300)
        status = self.statusBar()
        status.showMessage("status message")
