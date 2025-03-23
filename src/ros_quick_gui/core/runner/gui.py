import sys
from python_qt_binding.QtWidgets import QApplication
from ros_quick_gui.core.graph.node import Graph
from ros_quick_gui.core.ros import RclpyManager
from ros_quick_gui.core.ros.facade import RclpySetup
from ros_quick_gui.core.window import MainWindow


def ros_setup(ros):
    for node in Graph.nodes(RclpySetup):
        node._ros_setup(ros)


def run_gui(widget):
    app = QApplication(sys.argv)
    ros = RclpyManager(sys.argv)

    window = MainWindow()
    window.setCentralWidget(widget._qt_widget())
    window.show()

    ros.init()
    ros_setup(ros.facade)
    ros.exec()
    ret = app.exec_()
    ros.quit()
    sys.exit(ret)
