from ros_quick_gui.core import utils
from ros_quick_gui.core.graph import BridgeStream


class Data(BridgeStream):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def _process(self, context):
        context.value = self._value
