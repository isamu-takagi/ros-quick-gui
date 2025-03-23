import collections
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from rclpy.node import Node
from rclpy.timer import Timer
from rosidl_runtime_py.utilities import get_message


class RclpyNodeFacade:
    def __init__(self, node: Node):
        self.__node = node
        self.__timer = RclpyTimerFacade(node)
        self.__pubs = {}
        self.__subs = {}
        self.__sub_waiting = {}
        self.__sub_streams = collections.defaultdict(list)
        self.__topic_find_timer = node.create_timer(1.0, self.__on_topic_find_timer)
        self.__topic_find_cache = dict(node.get_topic_names_and_types())

    @property
    def timer(self):
        return self.__timer

    def clock(self):
        return self.__node.get_clock()

    def register_publisher(self, topic_type, topic_name):
        # TODO: Check topic type conflict.
        topic_type = self.find_topic_type(topic_type, topic_name)
        if topic_name not in self.__pubs:
            self.__pubs[topic_name] = self.__node.create_publisher(topic_type, topic_name, 1)
        return self.__pubs[topic_name]

    def register_subscription(self, topic_type, topic_name, stream):
        # TODO: Check topic type conflict.
        topic_type = self.find_topic_type(topic_type, topic_name)
        if topic_type:
            self.__start_subscription(topic_type, topic_name, stream)
        else:
            self.__sub_waiting[stream] = topic_name

    def __start_subscription(self, topic_type, topic_name, stream):
        if topic_name not in self.__subs:
            callback = functools.partial(self.__on_topic, topic_name=topic_name)
            self.__subs[topic_name] = self.__node.create_subscription(topic_type, topic_name, callback, 1)
        self.__sub_streams[topic_name].append(stream)
        self.__node.get_logger().info(f"Start subscription of '{topic_name}'")

    def find_topic_type(self, topic_type, topic_name):
        if topic_type is None:
            types = self.__topic_find_cache.get(topic_name)
            topic_type = types[0] if types else None
        if type(topic_type) is str:
            topic_type = get_message(topic_type)
        return topic_type

    def __on_topic(self, msg, topic_name):
        for stream in self.__sub_streams[topic_name]:
            stream._ros_callback(msg)

    def __on_topic_find_timer(self):
        self.__topic_find_cache = dict(self.__node.get_topic_names_and_types())
        for stream, topic_name in list(self.__sub_waiting.items()):
            topic_type = self.find_topic_type(None, topic_name)
            if topic_type:
                self.__sub_waiting.pop(stream)
                self.__start_subscription(topic_type, topic_name, stream)


class RclpySetup(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _ros_setup(self, ros: RclpyNodeFacade):
        raise NotImplementedError("RclpySetup._ros_setup")


class RclpyTimerFacade:
    def __init__(self, node: Node):
        self.node = node
        self.__timers = {}

    def create(self, sec: float, callback: callable):
        timer = self.__timers.get(callback)
        if timer:
            raise Exception("This timer is already created.")
        timer = self.node.create_timer(sec, callback)
        self.__timers[callback] = timer
