from PyQt5.QtWidgets import QGridLayout, QWidget

from ros_quick_gui.core.graph import NodeScreen


class MatrixLayout(NodeScreen):
    def __init__(self, *, rows: int = None, cols: int = None):
        super().__init__()

    def _qt_setup(self):
        layout = QGridLayout()
        for i in range(len(self._children)):
            screen = self._children[i]._qt()
            layout.addWidget(screen, 0, i)
        return layout
