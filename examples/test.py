#! /usr/bin/env python3
from ros_quick_gui.widgets import Label, MatrixLayout, Topic


def generate_gui_settings():
    layout = MatrixLayout()
    layout << Label("AAA") << Topic("/test/text")
    layout << Label("BBB") << Topic("/test/num")
    layout << Label("CCC") << Topic("/test/num")
    layout << Label("DDD")
    return layout
