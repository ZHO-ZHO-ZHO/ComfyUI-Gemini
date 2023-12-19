import google.generativeai as genai

class GeminiAPINode:

    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is not None:
            genai.configure(api_key=self.api_key)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Enter your prompt", "multiline": True}),
                "model_name": ("STRING", {"default": "gemini-pro"}),
                "stream": ("BOOLEAN", {"default": False}),
                "api_key": ("STRING", {"default": ""})  # Add api_key as an input
            }
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "generate_content"

    CATEGORY = "Gemini API"

    def generate_content(self, prompt, model_name, stream, api_key):
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=self.api_key)
        if not self.api_key:
            raise ValueError("API key is required")

        model = genai.GenerativeModel(model_name)
        if stream:
            response = model.generate_content(prompt, stream=True)
            return "\n".join([chunk.text for chunk in response])
        else:
            response = model.generate_content(prompt)
            return response.text


NODE_CLASS_MAPPINGS = {
    "GeminiAPINode": GeminiAPINode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiAPINode": "Gemini API Node"
}
