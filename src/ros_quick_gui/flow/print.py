from ros_quick_gui.core.graph.data import DataContext
from ros_quick_gui.core.graph.flow import Socket, SocketNode


class Print(SocketNode):
    def __init__(self):
        super().__init__()
        self._input = Socket(self._receive)

    def _receive(self, context: DataContext):
        print(context.value)

    def _default_socket(self):
        return self.input

    @property
    def input(self):
        return self._input
