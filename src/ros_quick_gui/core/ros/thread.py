from PyQt5.QtCore import QObject, QThread, qDebug
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node


class RclpyWorker(QObject):

    def __init__(self, node: Node):
        super().__init__()
        self.exec = SingleThreadedExecutor()
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
