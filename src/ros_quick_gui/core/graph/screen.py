from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QLayout, QWidget

from ros_quick_gui.core.graph.stream import RecvStream


class Screen(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _qt_setup(self):
        raise NotImplementedError("Screen._qt_setup")

    def _qt(self, convert_widget=False):
        screen = self._qt_setup()
        if isinstance(screen, QWidget):
            return screen
        if isinstance(screen, QLayout):
            if not convert_widget:
                return screen
            widget = QWidget()
            widget.setLayout(screen)
            return widget
        raise TypeError("Screen._qt")


class NodeScreen(Screen):
    def __init__(self):
        super().__init__()
        self._children = []

    def add_child(self, screen: Screen):
        self._children.append(screen)

    def __lshift__(self, screen: Screen):
        self.add_child(screen)
        return screen


class LeafScreen(Screen, RecvStream):
    def __init__(self):
        super().__init__()
