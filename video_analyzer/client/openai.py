import os
from openai import OpenAI

class OpenAIClient:
  def __init__(self, model="qwen/qwen3-vl-8b-thinking"):
    self.client = OpenAI(
        api_key = "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",
        base_url = "https://openrouter.ai/api/v1",
    )
    self.model = model

  def invoke(
      self,
      video,
      prompt,
      video_type='url'
  ):
      messages = self.message_synthesis(video, video_type, prompt)
      completion = self.client.chat.completions.create(
          model = self.model,
          messages = messages,
      )
      return completion.choices[0].message.content

  def message_synthesis(
    self,
    video,
    video_type='url',
    prompt=""
  ):
    if video_type=='url':
        video_msg = {"type": "image_url", "image_url": {"url": video}}
    elif video_type=='frame_list':
        video_msg = {"type": "video", "video": video['frame_list']}
    
    messages = [
        {
            "role": "user",
            "content": [
                video_msg,
                {"type": "text", "text": prompt},
            ]
        } 
    ]
    return messages