import functools
from abc import ABC, abstractmethod
from rclpy.node import Node
from rosidl_runtime_py.utilities import get_message


class RclpyNodeFacade:
    def __init__(self, node: Node):
        self.__node = node
        self.__timer = RclpyTimerFacade(node)
        self.__msg = RclpyTopicTypeFinder(node)
        self.__pubs = {}
        self.__subs = {}

    @property
    def timer(self):
        return self.__timer

    @property
    def msg(self):
        return self.__msg

    def clock(self):
        return self.__node.get_clock()

    def register_publisher(self, topic_type, topic_name):
        # TODO: Check topic type conflict.
        topic_type = self.find_topic_type(topic_type, topic_name)
        if topic_name not in self.__pubs:
            self.__pubs[topic_name] = self.__node.create_publisher(topic_type, topic_name, 1)
        return self.__pubs[topic_name]

    def register_subscription(self, topic_type, topic_name, topic_callback):
        def on_topic(msg):
            for callback in self.__subs[topic][1]:
                callback(msg)

        topic = (topic_name, topic_type)
        if topic not in self.__subs:
            sub = self.__node.create_subscription(topic_type, topic_name, on_topic, 1)
            self.__subs[topic] = (sub, [])
        self.__subs[topic][1].append(topic_callback)


class RclpySetup(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _ros_setup(self, ros: RclpyNodeFacade):
        raise NotImplementedError("RclpySetup._ros_setup")


class RclpyTimerFacade:
    def __init__(self, node: Node):
        self.__node = node
        self.__timers = {}

    def create(self, sec: float, callback: callable):
        timer = self.__timers.get(callback)
        if timer:
            raise Exception("This timer is already created.")
        timer = self.__node.create_timer(sec, callback)
        self.__timers[callback] = timer


class RclpyTopicTypeFinder:
    def __init__(self, node: Node):
        self.__node = node
        self.__cache = dict(self.__node.get_topic_names_and_types())
        self.__tasks = {}
        self.__timer = node.create_timer(1.0, self.__on_timer)

    def find_topic_type(self, topic_name, topic_type, callback):
        if topic_type is None:
            self.__tasks[callback] = topic_name
            return
        if type(topic_type) is str:
            topic_type = get_message(topic_type)
        callback(topic_type)

    def __on_timer(self):
        if self.__tasks:
            self.__cache = dict(self.__node.get_topic_names_and_types())
            for callback, topic_name in list(self.__tasks.items()):
                topic_types = self.__cache.get(topic_name)
                if topic_types:
                    callback(get_message(topic_types[0]))
                    self.__tasks.pop(callback)
