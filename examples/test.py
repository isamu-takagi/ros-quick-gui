#! /usr/bin/env python3
from ros_quick_gui.stream import Data, Get, Pub, Sub
from ros_quick_gui.widget import Label, MatrixLayout, PushButton


def generate_gui_settings():
    layout = MatrixLayout(cols=3)
    layout << Label("text") << Get("data") << Sub("/test/text")
    layout << Label("int") << Get("data") << Sub("/test/num")
    layout << PushButton("button") >> Data({"stamp": "now", "frame_id": "map"}) >> Pub("/test/header", "std_msgs/msg/Header")

    header = Sub("/test/header")
    layout << Label("sec") << Get("stamp.sec") << header
    layout << Label("nanosec") << Get("stamp.nanosec") << header
    layout << Label("frame") << Get("frame_id") << header
    return layout
