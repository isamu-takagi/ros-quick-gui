#! /usr/bin/env python3
from ros_quick_gui.flow import Const, Print, Timer
from ros_quick_gui.view import Label, MatrixLayout


def generate_gui_settings():
    layout = MatrixLayout(cols=3)

    timer = Timer(rate=1.0)
    layout << Label("text1") << Const(123) << timer
    layout << Label("text2") << Const(456) << timer
    layout << Label("text3") << Const(789) << timer
    # layout << Label("text") << Get("Const") << Sub("/test/text")
    return layout


if __name__ == "__main__":
    generate_gui_settings()
