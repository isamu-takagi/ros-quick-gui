import sys

from PyQt5.QtWidgets import QApplication

from .ros import RclpyManager
from .window import MainWindow


def stream_setup(ros):
    """
    for stream in RosStream._instances:
        stream._ros_setup(ros)"
    """
    pass


def main(widget):
    app = QApplication(sys.argv)
    ros = RclpyManager(sys.argv)

    window = MainWindow()
    window.setCentralWidget(widget._qt_widget())
    window.show()

    ros.init()
    stream_setup(ros.facade)
    ros.exec()
    ret = app.exec_()
    ros.quit()
    sys.exit(ret)


from argparse import ArgumentParser
from importlib.util import module_from_spec, spec_from_file_location


def load_python_file(path: str):
    spec = spec_from_file_location("ros_quick_gui.target", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def entry():
    parser = ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--cli", action="store_true")
    args = parser.parse_args()
    func = "generate_gui_settings"

    module = load_python_file(args.path)
    if not hasattr(module, func):
        raise NameError(f"The function '{func}' not found")
    main(getattr(module, func)())
