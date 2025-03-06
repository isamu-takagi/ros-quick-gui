from PyQt5.QtWidgets import QLabel, QPushButton


class StringFilter:
    def __call__(self, input):
        return str(input)


class AccessDataFilter:
    def __call__(self, input):
        return input.data


class TopicLabel:
    def __init__(self, topic_type, topic_name, filter=None):
        self.topic_type = topic_type
        self.topic_name = topic_name
        self.widget = None
        self.filter = filter or StringFilter()

    def init(self, node):
        self.widget = QLabel("Topic Label")
        node.register_subscription(self.topic_type, self.topic_name, self)

    def callback(self, msg):
        self.widget.setText(self.filter(msg))


class PublishButton:
    def __init__(self):
        self.button = QPushButton("Publish")
        self.button.clicked.connect(self.publish)
