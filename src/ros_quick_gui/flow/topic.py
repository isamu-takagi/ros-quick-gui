from rosidl_runtime_py import set_message_fields

from ros_quick_gui.core.graph import RecvStream, RosStream, SendStream, StreamContext
from ros_quick_gui.core.ros import RclpyNodeFacade


class Pub(RosStream, RecvStream):
    def __init__(self, topic_name: str, topic_type: str):
        super().__init__()
        self._topic_type = topic_type
        self._topic_name = topic_name
        self._ros = None
        self._pub = None

    def _ros_setup(self, ros: RclpyNodeFacade):
        self._ros = ros
        self._topic_type = ros.find_topic_type(self._topic_type, self._topic_name)
        self._pub = ros.register_publisher(self._topic_type, self._topic_name)

    def _receive(self, context: StreamContext):
        now = self._ros.clock().now().to_msg()
        msg = self._topic_type()
        setters = set_message_fields(msg, context.value, expand_time_now=True)
        for setter in setters:
            setter(now)
        self._pub.publish(msg)


class Sub(RosStream, SendStream):
    def __init__(self, topic_name: str, topic_type: str | None = None):
        super().__init__()
        self._topic_type = topic_type
        self._topic_name = topic_name

    def _ros_setup(self, ros: RclpyNodeFacade):
        ros.register_subscription(self._topic_type, self._topic_name, self)

    def _ros_callback(self, msg):
        self._send(StreamContext(msg))

    # TODO: move auto connect process and update topic_type
    def _ros_timer(self):
        pass
