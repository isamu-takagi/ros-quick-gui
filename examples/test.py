#! /usr/bin/env python3
from std_msgs.msg import String
from ros_quick_gui.core.main import main
from ros_quick_gui.flow import Const, Sub, Timer
from ros_quick_gui.view import Label, MatrixLayout


def generate_gui_settings():
    layout = MatrixLayout(cols=3)

    timer = Timer(rate=1.0)
    layout << Label("text1") << Sub("/test/text", String)
    layout << Label("text2") << Sub("/test/text", "std_msgs/msg/String")
    layout << Label("text3") << Sub("/test/text")
    return layout


if __name__ == "__main__":
    main(generate_gui_settings())
