from PyQt5.QtWidgets import QLabel

from ros_quick_gui.core.graph import LeafScreen


class Label(LeafScreen):
    def __init__(self, text: str = ""):
        super().__init__()
        self._text = text

    def _qt_setup(self):
        self._label = QLabel(self._text)
        return self._label

    def _receive(self, context):
        return self._label.setText(str(context))
