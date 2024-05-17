from abc import ABC, abstractmethod

class LlmBase(ABC):
    """ Base class for all LLM related operations """

    def llm_compilation_stream(self, text: str, system_prompt: str, model: str) -> object:
        """ Method to get a response from the LLM response as stream """