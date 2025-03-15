from ros_quick_gui.core.graph import SourceStream


class Topic(SourceStream):
    def __init__(self, topic_name: str, topic_type: str | None = None):
        super().__init__()
        self.topic_type = topic_type
        self.topic_name = topic_name

    def _ros_setup(self, ros):
        ros.register_subscription(self.topic_type, self.topic_name, self)

    def _ros_callback(self, msg):
        self._send(msg)
