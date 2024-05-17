from abc import ABC
from queues.consuemrs_base import ConsumersBase
from google.cloud import pubsub_v1
from typing import Callable
from queues.gcp_pub_sub.gcp_pub_sub_base import GcpPubSubBase


class GcpPubSubConsumer(ConsumersBase, GcpPubSubBase, ABC):
    """ Producer for GCP pubsub """

    def __init__(self, project: str, subscription: str):
        super().__init__()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project, subscription)

    def consume_messages(self, call_back_method: Callable):
        """ Subscribe to the subscription and listen for messages indefinitely """
        streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path,
            callback=call_back_method
        )
        print(f"Listening for messages on {self.subscription_path}\n")

        # Keep the main thread running, use exception handling for graceful shutdown.
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()  # Cancel the subscription stream on interruption
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            streaming_pull_future.cancel()  # Ensure the stream is canceled on error

    def callback(self, message):
        """ Callback function to handle incoming messages - this is a SAMPLE """
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()

    def is_empty(self) -> bool:
        """ Check if the queue is empty """
        raise NotImplementedError("Method is_empty is not supported in GCP pub/sub ")

# if __name__ == "__main__":
#     handler = GcpPubSubConsumer(
#         project='',
#         subscription=''
#     )
#
#     def callback_print(message):
#         """ Callback function to handle incoming messages """
#         print(message.data.decode('utf-8'), end='')
#         message.ack()
#
#     handler.consume_messages(callback_print)