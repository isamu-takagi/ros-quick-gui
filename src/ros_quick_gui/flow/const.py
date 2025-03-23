from ros_quick_gui.core.graph.data import DataContext
from ros_quick_gui.core.graph.flow import FilterNode, Signal, Socket


class Const(FilterNode):
    def __init__(self, value):
        super().__init__()
        self._value = value
        self._ignite = Socket(self._receive)
        self._output = Signal()

    def _process(self, context: DataContext):
        context.value = self._value

    def _receive(self, context: DataContext):
        self._process(context)
        self._output._invoke(context)

    def _default_socket(self):
        return self.ignite

    def _default_signal(self):
        return self.output

    @property
    def ignite(self):
        return self._ignite

    @property
    def output(self):
        return self._output
