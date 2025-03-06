import collections
import functools

import rclpy
import rclpy.executors
from PyQt5.QtCore import QObject, QThread, qDebug


class RclpyWorker(QObject):

    def __init__(self):
        super().__init__()
        self.exec = rclpy.executors.SingleThreadedExecutor()
        self.node = rclpy.create_node("ros_quick_gui")

    def spin(self):
        qDebug("spin start")
        self.exec.add_node(self.node)
        self.exec.spin()
        qDebug("spin end")

    def quit(self):
        self.exec.shutdown()


class RclpyThread:
    def __init__(self):
        rclpy.init()
        self.worker = RclpyWorker()
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
        rclpy.shutdown()

    def node(self):
        return RclpyNodeInterface(self.worker.node)


class RclpyNodeInterface:
    def __init__(self, node):
        self.__node = node
        self.__subs = {}
        self.__sub_units = collections.defaultdict(list)

    def register_subscription(self, topic_type, topic_name, unit):
        if topic_name not in self.__subs:
            callback = functools.partial(self.callback, topic_name=topic_name)
            self.__subs[topic_name] = self.__node.create_subscription(
                topic_type, topic_name, callback, 1
            )
        self.__sub_units[topic_name].append(unit)

    def callback(self, msg, topic_name):
        qDebug(f"{msg} {topic_name}")
        for unit in self.__sub_units[topic_name]:
            unit.callback(msg)
