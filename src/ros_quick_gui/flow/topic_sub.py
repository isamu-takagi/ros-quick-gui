from typing import Any
from rosidl_runtime_py import set_message_fields
from ros_quick_gui.core.graph.data import DataContext
from ros_quick_gui.core.graph.flow import Signal, SignalNode
from ros_quick_gui.core.ros.facade import RclpyNodeFacade, RclpySetup


class Sub(SignalNode, RclpySetup):
    def __init__(self, topic_name: str, topic_type: Any = None):
        super().__init__()
        self._topic_name = topic_name
        self._topic_type = topic_type
        self._output = Signal()

    def _ros_setup(self, ros: RclpyNodeFacade):
        self._ros = ros
        ros.msg.find_topic_type(self._topic_name, self._topic_type, self._ros_create_sub)

    def _ros_create_sub(self, topic_type):
        self._topic_type = topic_type
        self._ros.register_subscription(self._topic_type, self._topic_name, self._ros_msg_callback)

    def _ros_msg_callback(self, msg):
        self._output._invoke(DataContext(msg))

    def _default_signal(self):
        return self.output

    @property
    def output(self):
        return self._output
