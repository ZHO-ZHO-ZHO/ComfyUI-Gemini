import io
#from io import BytesIO
#import torchvision.transforms as transforms
import google.generativeai as genai
from PIL import Image
import torch

class Gemini_API_Zho:

    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is not None:
            genai.configure(api_key=self.api_key)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "model_name": (["gemini-pro", "gemini-pro-vision"],),
                "stream": ("BOOLEAN", {"default": False}),
                "api_key": ("STRING", {"default": ""})  # Add api_key as an input
            },
            "optional": {
                "image": ("IMAGE",),  
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "Zho模块组/✨Gemini"

    def tensor_to_image(self, tensor):
        tensor = tensor.squeeze().mul(255).byte()  # 转换为0-255范围的字节数据
        tensor = tensor.permute(1, 2, 0)  # 从C x H x W转换为H x W x C
        image = Image.fromarray(tensor.cpu().numpy(), mode='RGB')
        return image

    def image_to_byte_stream(self, image):
        byte_stream = io.BytesIO()
        image.save(byte_stream, format='JPEG')  # 保存为JPEG格式
        byte_stream.seek(0)  # 重置流位置
        return byte_stream
    
    def generate_content(self, prompt, model_name, stream, api_key, image=None):
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=self.api_key)
        if not self.api_key:
            raise ValueError("API key is required")

        model = genai.GenerativeModel(model_name)

        if model_name == 'gemini-pro':
            if stream:
                response = model.generate_content(prompt, stream=True)
                textoutput = "\n".join([chunk.text for chunk in response])
            else:
                response = model.generate_content(prompt)
                textoutput = response.text
        
        if model_name == 'gemini-pro-vision':
            if image == None:
                raise ValueError("gemini-pro-vision needs image")
            else:
                # 转换图像
                pil_image = self.tensor_to_image(image)
                image_stream = self.image_to_byte_stream(pil_image)

                # 使用图像流
                if stream:
                    response = model.generate_content([prompt, image_stream], stream=True)
                    textoutput = "\n".join([chunk.text for chunk in response])
                else:
                    response = model.generate_content([prompt, image_stream])
                    textoutput = response.text
        
        return (textoutput,)


# DisplayText node is forked from AlekPet，thanks to AlekPet！
class DisplayText_Zho:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {        
                "text": ("STRING", {"forceInput": True}),     
                },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "display_text"

    CATEGORY = "Zho模块组/✨Gemini"

    def display_text(self, text, prompt=None, extra_pnginfo=None):
        return {"ui": {"string": [text,]}, "result": (text,)}


NODE_CLASS_MAPPINGS = {
    "Gemini_API_Zho": Gemini_API_Zho,
    "DisplayText_Zho": DisplayText_Zho
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_API_Zho": "✨Gemini_API_Zho",
    "DisplayText_Zho": "✨DisplayText_Zho"
}
