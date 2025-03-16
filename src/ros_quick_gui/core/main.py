import sys

from PyQt5.QtWidgets import QApplication

from .ros import RclpyManager
from .window import MainWindow


def stream_setup(ros):
    from ros_quick_gui.core.graph.stream import RosStream

    for stream in RosStream._instances:
        stream._ros_setup(ros)


def main(widget):
    app = QApplication(sys.argv)
    ros = RclpyManager(sys.argv)

    window = MainWindow()
    window.setCentralWidget(widget._qt(True))
    window.show()

    ros.init()
    stream_setup(ros.facade)
    ros.exec()
    ret = app.exec_()
    ros.quit()
    sys.exit(ret)


from argparse import ArgumentParser
from importlib.util import module_from_spec, spec_from_file_location


def entry():
    parser = ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    spec = spec_from_file_location("ros_quick_gui.target", args.path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    generate_gui_settings = getattr(module, "generate_gui_settings")

    main(generate_gui_settings())
    # test(generate_gui_settings())
