from abc import ABC, abstractmethod
from typing import List
from queues.queues_base import QueuesBase


class ProducersBase(QueuesBase, ABC):
    """ Base for all producers """

    @abstractmethod
    def publish_messages(self, messages: List[object]):
        """Remove and return the front item from the queue."""
        pass
