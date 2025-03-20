from abc import abstractmethod
from copy import deepcopy

from ros_quick_gui.core.graph.node import GraphNode


class Flow(GraphNode):
    def __init__(self):
        super().__init__()

    @classmethod
    def _shift_connect(cls, importer, exporter):
        print("flow connect", importer, exporter)


class PureSignal:
    pass


class PureSocket:
    pass


class FlowSignal:
    pass


class FlowSocket:
    pass


class FlowBridge:
    pass
