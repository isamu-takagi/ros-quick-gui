from abc import abstractmethod
from copy import deepcopy
from ros_quick_gui.core.graph.node import GraphNode


class Flow(GraphNode):
    def __init__(self):
        super().__init__()

    @classmethod
    def _shift_connect(cls, importer, exporter):
        signal = cls.__as_signal(exporter)
        socket = cls.__as_socket(importer)
        signal.connect(socket)

    @classmethod
    def __as_socket(cls, target):
        if isinstance(target, SocketNode):
            return target._default_socket()
        if isinstance(target, Socket):
            return target
        raise TypeError(f"The '{type(target).__name__}' type '{target}' is not a socket")

    @classmethod
    def __as_signal(cls, target):
        if isinstance(target, SignalNode):
            return target._default_signal()
        if isinstance(target, Signal):
            return target
        raise TypeError(f"The '{type(target).__name__}' type '{target}' is not a signal")


class Socket(Flow):
    def __init__(self, func: callable):
        super().__init__()
        self.__func = func

    def __call__(self, *args, **kwargs):
        self.__func(*args, **kwargs)


class Signal(Flow):
    def __init__(self):
        super().__init__()
        self.__sockets = []

    def connect(self, socket: Socket):
        self.__sockets.append(socket)

    def _invoke(self, *args, **kwargs):
        for socket in self.__sockets:
            socket(*args, **kwargs)


class SocketNode(Flow):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _default_socket(self):
        raise NotImplementedError("SocketNode._default_socket")


class SignalNode(Flow):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _default_signal(self):
        raise NotImplementedError("SignalNode._default_signal")


class FilterNode(SocketNode, SignalNode):
    def __init__(self):
        super().__init__()
