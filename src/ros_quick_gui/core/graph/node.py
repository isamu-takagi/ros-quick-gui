from abc import ABC, abstractmethod


class GraphNode(ABC):

    def __lshift__(l, r):
        return GraphUtils.lshift(l, r)

    def __rshift__(l, r):
        return GraphUtils.rshift(l, r)

    def __rlshift__(r, l):
        return GraphUtils.lshift(l, r)

    def __rrshift__(r, l):
        return GraphUtils.rshift(l, r)

    def __str__(self):
        trace = getattr(self, "_value") if hasattr(self, "_value") else None
        trace = f"({trace})" if trace else ""
        return f"{self.__class__.__name__}{trace}"

    @classmethod
    @abstractmethod
    def _shift_connect(cls, importer, exporter):
        raise NotImplementedError("GraphNode._shift_connect")


class GraphChain:

    def __init__(self, nodes: list[GraphNode]):
        self.nodes = nodes

    def __str__(self):
        chain = ", ".join(str(node) for node in self.nodes)
        return f"{self.__class__.__name__} [{chain}]"

    def __lshift__(self, node):
        return GraphUtils.lshift(self, node)

    def __rshift__(self, node):
        return GraphUtils.rshift(self, node)

    @classmethod
    def build(cls, node):
        return node if isinstance(node, cls) else cls([node])

    @property
    def left(self):
        return self.nodes[0]

    @property
    def right(self):
        return self.nodes[-1]


class GraphUtils:

    @classmethod
    def lshift(cls, l, r):
        l = GraphChain.build(GraphUtils.normalize(l))
        r = GraphChain.build(GraphUtils.normalize(r))
        GraphUtils.connect(l.right, r.left)
        return GraphChain(l.nodes + r.nodes)

    @classmethod
    def rshift(cls, l, r):
        l = GraphChain.build(GraphUtils.normalize(l))
        r = GraphChain.build(GraphUtils.normalize(r))
        GraphUtils.connect(r.left, l.right)
        return GraphChain(l.nodes + r.nodes)

    @classmethod
    def normalize(cls, node):
        if isinstance(node, GraphNode):
            return node
        raise TypeError(f"The '{type(node).__name__}' type value '{node}' is not a GraphNode")

    @classmethod
    def connect(cls, importer, exporter):
        base = cls.get_common_cls(importer, exporter)
        base._shift_connect(importer, exporter)

    @classmethod
    def get_common_cls(cls, a, b):
        a = a.__class__.__mro__
        b = b.__class__.__mro__
        c = set(a) & set(b)
        return next(x for x in a if x in c)
