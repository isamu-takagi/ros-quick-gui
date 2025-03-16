from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from ros_quick_gui.core.graph import RecvStream, Screen, StreamContext


class Label(Screen, RecvStream):
    def __init__(self, text: str = ""):
        super().__init__()
        self._text = text

    def _qt_setup(self):
        self._label = QLabel(self._text)
        self._label.setAlignment(Qt.AlignCenter)
        return self._label

    def _receive(self, context: StreamContext):
        return self._label.setText(str(context.value))
