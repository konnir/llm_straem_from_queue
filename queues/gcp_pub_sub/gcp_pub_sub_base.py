from abc import ABC
from google.cloud import pubsub_v1
from queues.queues_base import QueuesBase

class GcpPubSubBase(QueuesBase, ABC):

    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    handler = GcpPubSubBase()
    items = ['testing 123']
    handler.publish_messages(items)
    consumer = handler.consume_messages()

