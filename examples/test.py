#! /usr/bin/env python3
from ros_quick_gui.stream import Get, Topic
from ros_quick_gui.widget import Label, MatrixLayout, PushButton


def generate_gui_settings():
    layout = MatrixLayout(cols=3)
    layout << Label("text") << Get("data") << Topic("/test/text")
    layout << Label("int") << Get("data") << Topic("/test/num")
    layout << PushButton("button") >> Topic("/test/header")

    header = Topic("/test/header")
    layout << Label("sec") << Get("stamp.sec") << header
    layout << Label("nanosec") << Get("stamp.nanosec") << header
    layout << Label("frame") << Get("stamp.frame_id") << header
    return layout
