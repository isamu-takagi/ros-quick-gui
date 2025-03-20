from PyQt5.QtWidgets import QGridLayout

from ros_quick_gui.core.graph import View


class MatrixLayout(View):

    def __init__(self, *, cols: int = 0, rows: int = 0, dir: str = "RB"):
        super().__init__()
        self._index = _MatrixIndex(cols, rows)
        self._children = []

    def _qt_setup(self):
        layout = QGridLayout()
        for child in self._children:
            screen = child._qt()
            ix, iy = self._index.next()
            layout.addWidget(screen, iy, ix)
        layout.setRowStretch(2, 1)
        return layout

    def add(self, node):
        self._children.append(node)


# TODO: support direction
class _MatrixIndex:
    def __init__(self, cols, rows):
        self.mx = cols or 2**31
        self.my = rows or 2**31
        self.ix = 0
        self.iy = 0
        self.dx = 1
        self.dy = 0

    def next(self):
        result = (self.ix, self.iy)
        self.__next_cell()
        self.__next_line()
        return result

    def __next_cell(self):
        self.ix += self.dx
        self.iy += self.dy

    def __next_line(self):
        if (0 <= self.ix < self.mx) and (0 <= self.iy < self.my):
            return
        self.ix = 0
        self.iy = self.iy + 1
