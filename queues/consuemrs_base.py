from abc import ABC, abstractmethod
from typing import List, Callable

from queues.queues_base import QueuesBase


class ConsumersBase(QueuesBase, ABC):
    """ Base for all consumers """

    @abstractmethod
    def consume_messages(self, call_back_method: Callable):
        """Remove and return the front item from the queue."""
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        pass