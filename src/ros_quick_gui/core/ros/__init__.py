import rclpy

from .facade import RclpyNodeFacade
from .thread import RclpyThread


class RclpyManager:
    def __init__(self, argv):
        self.argv = argv

    def init(self):
        rclpy.init()
        node = rclpy.create_node("ros_quick_gui")
        self.thread = RclpyThread(node)
        self.facade = RclpyNodeFacade(node)

    def exec(self):
        self.thread.exec()

    def quit(self):
        self.thread.quit()
        rclpy.shutdown()
