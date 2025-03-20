from ros_quick_gui.core.graph.flow import Flow


class Data(Flow):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def _process(self, context):
        context.value = self._value
