from abc import ABC, abstractmethod


class GraphNode(ABC):

    def __init__(self):
        Graph._nodes.append(self)

    def __lshift__(l, r):
        return GraphUtils.lshift(l, r)

    def __rshift__(l, r):
        return GraphUtils.rshift(l, r)

    def __rlshift__(r, l):
        return GraphUtils.lshift(l, r)

    def __rrshift__(r, l):
        return GraphUtils.rshift(l, r)

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

    @property
    def left(self):
        return self.nodes[0]

    @property
    def right(self):
        return self.nodes[-1]


class GraphUtils:

    @classmethod
    def lshift(cls, l, r):
        l = cls.normalize_operand(l)
        r = cls.normalize_operand(r)
        cls.connect(l.right, r.left)
        return GraphChain(l.nodes + r.nodes)

    @classmethod
    def rshift(cls, l, r):
        l = cls.normalize_operand(l)
        r = cls.normalize_operand(r)
        cls.connect(r.left, l.right)
        return GraphChain(l.nodes + r.nodes)

    @classmethod
    def normalize_operand(cls, target):
        if isinstance(target, GraphChain):
            return target
        if isinstance(target, GraphNode):
            return GraphChain([target])
        raise TypeError(f"The '{type(target).__name__}' type '{target}' is not a graph element")

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


class Graph:

    _nodes = []
    _links = []

    @classmethod
    def nodes(cls, base=GraphNode):
        for node in cls._nodes:
            if isinstance(node, base):
                yield node
