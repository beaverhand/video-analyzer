from transformers import Qwen3VLForConditionalGeneration, AutoProcessor

class LocalClient(LLMClientABC):
  def __init__ (self, model="Qwen/Qwen3-VL-4B-Thinking"):
    self.model = Qwen3VLForConditionalGeneration.from_pretrained(model, dtype="auto", device_map="auto")
    self.processor = AutoProcessor.from_pretrained(model)

  def invoke(self, input, prompt=""):
    # formatted the message
    messages = self.message_synthesis(input, prompt)
    inputs = self.generate_input(messages)

    # Inference: Generation of the output
    output_text = self.generate(inputs)
    return output_text
  
  def message_synthesis(self, input, prompt=""):
    messages = [
                  {
                      "role": "user",
                      "content": [
                          {
                              "type": "image",
                              "image": input,
                          },
                          {"type": "text", "text": prompt if prompt else self.prompt},
                      ],
                  }
              ]

    return messages

  def generate_input(self, messages):
    inputs = self.processor.apply_chat_template(
      messages,
      tokenize=True,
      add_generation_prompt=True,
      return_dict=True,
      return_tensors="pt"
      )

    inputs = inputs.to(self.model.device)
    return inputs

  def generate(self, inputs):
    generated_ids = self.model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = self.processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    return output_text