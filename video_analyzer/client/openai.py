import os
from openai import OpenAI
from core.config import settings
from client.llm_client import LLMClient
from logger import GLOBAL_LOGGER as log
from prompts.custom_prompt import SYSTEM_PROMPT
class OpenAIClient(LLMClient):
  def __init__(self, model="Qwen/Qwen3-VL-4B-Instruct"):
    self.client = OpenAI(
        api_key = settings.OPENROUTER_API_KEY,
        base_url = settings.OPENROUTER_BASE_URL,
    )
    self.model = model

  def invoke(
      self,
      video,
      prompt,
      video_type='url'
  ):
      messages = self.message_synthesis(video, video_type, prompt)
      log.debug("Message Syntesis is done")
      completion = self.client.chat.completions.create(
          model = self.model,
          messages = messages,
      )
      log.debug("Completion is done")
      return completion.choices[0].message.content

  def message_synthesis(
    self,
    video,
    video_type='url',
    prompt=""
  ):
    if video_type=='url':
        video_msg = {"type": "video_url", "video_url": {"url": video}}
    elif video_type=='frame_list':
        video_msg = {"type": "video", "video": video['frame_list']}
    
    messages = [
        # {
        #     "role": "system",
        #     "content": SYSTEM_PROMPT,
        # },
        {
            "role": "user",
            "content": [
                video_msg,
                {"type": "text", "text": prompt},
            ]
        } 
    ]
    return messages