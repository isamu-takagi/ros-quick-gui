from ros_quick_gui.core.graph.data import DataContext
from ros_quick_gui.core.graph.flow import Signal, SignalNode
from ros_quick_gui.core.ros.facade import RclpyNodeFacade, RclpySetup


class Timer(SignalNode, RclpySetup):
    def __init__(self, rate):
        super().__init__()
        self._rate = rate
        self._elapsed = Signal()

    def _ros_setup(self, ros: RclpyNodeFacade):
        self._ros = ros
        ros.timer.create(1.0 / self._rate, self._on_timer)

    def _on_timer(self):
        self._elapsed._invoke(DataContext(None))

    def _default_signal(self):
        return self.elapsed

    @property
    def elapsed(self):
        return self._elapsed
