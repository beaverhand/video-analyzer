from abc import ABC, abstractmethod

class LLMClient(ABC):
  @abstractmethod
  def invoke(self, input, prompt="", video_type='url'):
    pass

  @abstractmethod
  def message_synthesis(self, input, video_type='url', prompt=""):
    pass