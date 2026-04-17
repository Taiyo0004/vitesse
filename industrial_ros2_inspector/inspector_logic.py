import rclpy
from rclpy.node import Node
from rosidl_runtime_py.utilities import get_message
from rosidl_runtime_py import message_to_ordereddict
import json
from PyQt5.QtCore import pyqtSignal, QObject

class CommSignals(QObject):
    add_topic = pyqtSignal(str, str, list, list)
    update_data = pyqtSignal(str, str)

class DetailedInspector(Node):
    def __init__(self, signals):
        super().__init__('industrial_detailed_inspector')
        self.signals = signals
        self.discovered_topics = {}
        self.subs = {}
        self.create_timer(2.0, self.discover_topics)

    def discover_topics(self):
        topic_list = self.get_topic_names_and_types()
        for name, types in topic_list:
            if any(x in name for x in ['rosout', 'parameter', 'tf', 'events']):
                continue
            if name not in self.discovered_topics:
                pubs_info = self.get_publishers_info_by_topic(name)
                subs_info = self.get_subscriptions_info_by_topic(name)
                pub_nodes = [info.node_name for info in pubs_info]
                sub_nodes = [info.node_name for info in subs_info]
                
                self.discovered_topics[name] = types[0]
                self.signals.add_topic.emit(name, types[0], pub_nodes, sub_nodes)
                
                try:
                    msg_type = get_message(types[0])
                    self.subs[name] = self.create_subscription(
                        msg_type, name, 
                        lambda msg, t=name: self.callback(msg, t), 10
                    )
                except: pass

    def callback(self, msg, topic):
        msg_dict = message_to_ordereddict(msg)
        formatted_msg = json.dumps(msg_dict, indent=4)
        self.signals.update_data.emit(topic, formatted_msg)