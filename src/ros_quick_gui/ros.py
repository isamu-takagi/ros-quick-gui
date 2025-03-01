import rclpy
import rclpy.executors
from PyQt5.QtCore import QObject, QThread, qDebug


class RclpyWorker(QObject):

    def __init__(self):
        super().__init__()
        self.executor = None

    def spin(self):
        qDebug("spin start")
        rclpy.init()
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(rclpy.create_node("ros_quick_gui"))
        self.executor.spin()
        rclpy.shutdown()
        qDebug("spin end")


class RclpyThread:
    def __init__(self):
        self.worker = RclpyWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.spin)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def quit(self):
        self.worker.executor.shutdown()
        self.worker.deleteLater()
        self.thread.quit()
        self.thread.wait()
