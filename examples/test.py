#! /usr/bin/env python3
from ros_quick_gui.flow import Data
from ros_quick_gui.view import Label, MatrixLayout


def generate_gui_settings():
    layout = MatrixLayout(cols=3)
    layout << Label("text1")
    layout.add(Label("text2"))

    Data(123) << Data(456)
    Data(123) << Data(456)

    # layout = MatrixLayout(cols=3)
    # layout << Label("text") << Get("data") << Sub("/test/text")
    # return layout
    return layout


generate_gui_settings()
