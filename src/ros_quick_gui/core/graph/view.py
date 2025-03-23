from abc import abstractmethod
from ros_quick_gui.core.graph.node import GraphNode


class View(GraphNode):
    def __init__(self):
        super().__init__()
        self.__qt = None

    def _qt(self):
        self.__qt = self.__qt or self._qt_setup()
        return self.__qt

    def _qt_widget(self):
        from PyQt5.QtWidgets import QLayout, QWidget

        qt = self._qt()
        if isinstance(qt, QWidget):
            return qt
        if isinstance(qt, QLayout):
            widget = QWidget()
            widget.setLayout(qt)
            return widget
        raise TypeError("View._qt_widget")

    @abstractmethod
    def _qt_setup(self):
        raise NotImplementedError("View._qt_setup")

    @abstractmethod
    def add(self, view):
        raise NotImplementedError("View.add")

    @classmethod
    def _shift_connect(cls, importer: "View", exporter: "View"):
        importer.add(exporter)


class LeafView(View):
    def __init__(self):
        super().__init__()

    def add(self, view):
        raise TypeError(f"Cannot add '{view}' to LeafView")
