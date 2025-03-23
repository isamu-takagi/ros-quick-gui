from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from ros_quick_gui.core.graph.data import DataContext
from ros_quick_gui.core.graph.flow import Socket, SocketNode
from ros_quick_gui.core.graph.view import LeafView


class Label(LeafView, SocketNode):
    def __init__(self, text: str = ""):
        super().__init__()
        self._text = text
        self._input = Socket(self._receive)

    def _qt_setup(self):
        self._label = QLabel(self._text)
        self._label.setAlignment(Qt.AlignCenter)
        return self._label

    def _receive(self, context: DataContext):
        return self._label.setText(str(context.value))

    def _default_socket(self):
        return self.input

    @property
    def input(self):
        return self._input
