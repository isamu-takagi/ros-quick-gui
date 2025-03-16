from ros_quick_gui.core import utils
from ros_quick_gui.core.graph import BridgeStream


class Get(BridgeStream):
    def __init__(self, field):
        super().__init__()
        self._field = field.split(".")

    def _process(self, context):
        context.value = utils.get_field(context.value, self._field)
