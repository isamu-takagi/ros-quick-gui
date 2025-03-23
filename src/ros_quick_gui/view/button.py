from PyQt5.QtWidgets import QPushButton
from ros_quick_gui.core.graph import Screen, SendStream, StreamContext


class PushButton(Screen, SendStream):
    def __init__(self, text: str = ""):
        super().__init__()
        self._text = text

    def _qt_setup(self):
        self._label = QPushButton(self._text)
        self._label.clicked.connect(self._on_click)
        return self._label

    def _on_click(self):
        self._send(StreamContext(None))
