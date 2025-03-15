import rclpy
import rclpy.executors
from PyQt5.QtCore import QObject, QThread, qDebug

from .context import RclpyContext


class RclpyManager:
    def __init__(self, argv):
        self.argv = argv

    def init(self):
        rclpy.init()
        node = rclpy.create_node("ros_quick_gui")
        self.context = RclpyContext(node)
        self.thread = RclpyThread(node)

    def exec(self):
        self.thread.exec()

    def quit(self):
        self.thread.quit()
        rclpy.shutdown()


class RclpyWorker(QObject):

    def __init__(self, node):
        super().__init__()
        self.exec = rclpy.executors.SingleThreadedExecutor()
        self.node = node

    def spin(self):
        qDebug("spin start")
        self.exec.add_node(self.node)
        self.exec.spin()
        qDebug("spin end")

    def quit(self):
        self.exec.shutdown()


class RclpyThread:
    def __init__(self, node):
        self.worker = RclpyWorker(node)
        self.thread = QThread()

    def exec(self):
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.spin)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def quit(self):
        self.worker.quit()
        self.thread.quit()
        self.thread.wait()
