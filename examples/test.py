#! /usr/bin/env python3
from std_msgs.msg import String

import ros_quick_gui.main
from ros_quick_gui.widgets import TopicLabel

label = TopicLabel(String, "/test/text")

ros_quick_gui.main.main(label)
