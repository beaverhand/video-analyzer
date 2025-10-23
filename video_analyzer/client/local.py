from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from logger import GLOBAL_LOGGER as log
from client.llm_client import LLMClient
import os

class LocalClient(LLMClient):
  def __init__ (self, model="Qwen/Qwen3-VL-4B-Thinking"):
    self.model = Qwen3VLForConditionalGeneration.from_pretrained(model, dtype="auto", device_map="auto")
    self.processor = AutoProcessor.from_pretrained(model)

  # def invoke(self, input, prompt=""):
  #   # formatted the message
  #   messages = self.message_synthesis(input, prompt)
  #   inputs = self.generate_input(messages)

  #   # Inference: Generation of the output
  #   output_text = self.generate(inputs)
  #   return output_text
  
  def message_synthesis(self, video, total_pixels, min_pixels, max_frames, sample_fps, prompt):
    messages = [
        {"role": "user", "content": [
                {"video": video,
                "total_pixels": total_pixels, 
                "min_pixels": min_pixels, 
                "max_frames": max_frames,
                'sample_fps':sample_fps},
                {"type": "text", "text": prompt},
            ]
        },
    ]

    return messages

  def generate_input(self, messages):
    text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs, video_kwargs = process_vision_info([messages], return_video_kwargs=True, 
                                                                   image_patch_size= 16,
                                                                   return_video_metadata=True)
    if video_inputs is not None:
        video_inputs, video_metadatas = zip(*video_inputs)
        video_inputs, video_metadatas = list(video_inputs), list(video_metadatas)
    else:
        video_metadatas = None
    inputs = self.processor(text=[text], images=image_inputs, videos=video_inputs, video_metadata=video_metadatas, **video_kwargs, do_resize=False, return_tensors="pt")
    inputs = inputs.to('cuda')
    return inputs

  def generate(self, inputs, max_new_tokens):
    output_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
    output_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return output_text

  def clean_up(self, video_path):
    if os.path.exists(video_path):
      os.remove(video_path)

  def invoke(self, video, prompt, max_new_tokens=2048, total_pixels=20480 * 32 * 32, min_pixels=64 * 32 * 32, max_frames= 2048, sample_fps = 2):
    """
    Perform multimodal inference on input video and text prompt to generate model response.

    Args:
        video (str or list/tuple): Video input, supports two formats:
            - str: Path or URL to a video file. The function will automatically read and sample frames.
            - list/tuple: Pre-sampled list of video frames (PIL.Image or url). 
              In this case, `sample_fps` indicates the frame rate at which these frames were sampled from the original video.
        prompt (str): User text prompt to guide the model's generation.
        max_new_tokens (int, optional): Maximum number of tokens to generate. Default is 2048.
        total_pixels (int, optional): Maximum total pixels for video frame resizing (upper bound). Default is 20480*32*32.
        min_pixels (int, optional): Minimum total pixels for video frame resizing (lower bound). Default is 16*32*32.
        sample_fps (int, optional): ONLY effective when `video` is a list/tuple of frames!
            Specifies the original sampling frame rate (FPS) from which the frame list was extracted.
            Used for temporal alignment or normalization in the model. Default is 2.

    Returns:
        str: Generated text response from the model.

    Notes:
        - When `video` is a string (path/URL), `sample_fps` is ignored and will be overridden by the video reader backend.
        - When `video` is a frame list, `sample_fps` informs the model of the original sampling rate to help understand temporal density.
    """
    try:
      messages = self.message_synthesis(video, total_pixels, min_pixels, max_frames, sample_fps, prompt)
      inputs = self.generate_input(messages)
      output_text = self.generate(inputs, max_new_tokens)
      return output_text[0]
    except Exception as e:
      log.exception("Error processing analysis request", str(e))
      raise HTTPException(status_code=500, detail=str(e))
    finally:
      # clean up the video file after processing
      self.clean_up(video)
