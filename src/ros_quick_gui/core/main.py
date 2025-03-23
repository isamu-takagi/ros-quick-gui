from argparse import ArgumentParser
from importlib.util import module_from_spec, spec_from_file_location
from ros_quick_gui.core.runner.gui import run_gui


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
    run_gui(getattr(module, func)())
