from abc import ABC
from ast import Bytes
from typing import List
import json  # if you need to serialize non-string data
from google.cloud import pubsub_v1
from queues.gcp_pub_sub.gcp_pub_sub_base import GcpPubSubBase
from queues.producers_base import ProducersBase

class GcpPubSubProducer(ProducersBase, GcpPubSubBase, ABC):
    """ Producer for GCP pubsub """

    def __init__(self, project: str, topic: str):
        super().__init__()
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project, topic)

    def publish_messages(self, items: List[bytes]):
        try:
            for message in items:
                if len(message) > 0:
                    future = self.publisher.publish(self.topic_path, message)
                    result = future.result()  # Ensure the message was published
        except Exception as e:
            print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     handler = GcpPubSubProducer(
#         project='',
#         topic=''
#     )
#     handler.publish_messages(['new_testing11'.encode('utf-8'), 'new_testing22'.encode('utf-8')])
