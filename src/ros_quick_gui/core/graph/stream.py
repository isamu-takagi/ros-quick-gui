from abc import ABC, abstractmethod


class Stream(ABC):
    def __init__(self):
        super().__init__()


class SendStream(Stream):
    def __init__(self):
        super().__init__()
        self._outputs: list[RecvStream] = []

    def add_dst(self, recv: "RecvStream"):
        self._outputs.append(recv)

    def _send(self, context):
        # TODO(Takagi, Isamu): Clone context if destination is not unique
        for output in self._outputs:
            output._receive(context)


class RecvStream(Stream):
    def __init__(self):
        super().__init__()

    def __lshift__(self, send: "SendStream"):
        send.add_dst(self)
        return send

    @abstractmethod
    def _receive(self, context):
        pass


class BridgeStream(SendStream, RecvStream):
    def __init__(self):
        super().__init__()


class SourceStream(SendStream):
    _instances = []

    def __init__(self):
        super().__init__()
        self.__class__._instances.append(self)
