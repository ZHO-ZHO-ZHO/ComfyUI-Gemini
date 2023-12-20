import io
import requests
import torch
import google.generativeai as genai
from io import BytesIO
from PIL import Image


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
        # 确保张量是在CPU上
        tensor = tensor.cpu()
    
        # 将张量数据转换为0-255范围并转换为整数
        # 这里假设张量已经是H x W x C格式
        image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
    
        # 创建PIL图像
        image = Image.fromarray(image_np, mode='RGB')
        return image

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

                # 直接使用PIL图像
                if stream:
                    response = model.generate_content([prompt, pil_image], stream=True)
                    textoutput = "\n".join([chunk.text for chunk in response])
                else:
                    response = model.generate_content([prompt, pil_image])
                    textoutput = response.text
        
        return (textoutput,)


class Gemini_API_Vsion_ImgURL_Zho:

    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is not None:
            genai.configure(api_key=self.api_key)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Describe this image", "multiline": True}),
                "image_url": ("STRING", {"default": ""}),
                "model_name": (["gemini-pro-vision"],),
                "stream": ("BOOLEAN", {"default": False}),
                "api_key": ("STRING", {"default": ""})  # Add api_key as an input
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "Zho模块组/✨Gemini"

    def generate_content(self, prompt, model_name, stream, api_key, image_url):
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=self.api_key)
        if not self.api_key:
            raise ValueError("API key is required")

        # Load the image from the URL
        response = requests.get(image_url)
        if response.status_code != 200:
            raise ValueError("Failed to load image from URL")
        img = Image.open(BytesIO(response.content))

        model = genai.GenerativeModel(model_name)

        if stream:
            response = model.generate_content([prompt, img], stream=True)
            textoutput = "\n".join([chunk.text for chunk in response])
        else:
            response = model.generate_content([prompt, img])
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
    "Gemini_API_Vsion_ImgURL_Zho": Gemini_API_Vsion_ImgURL_Zho,
    "DisplayText_Zho": DisplayText_Zho
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_API_Zho": "✨Gemini_API_Zho",
    "Gemini_API_Vsion_ImgURL_Zho": "✨Gemini_API_Vsion_ImgURL_Zho",
    "DisplayText_Zho": "✨DisplayText_Zho"
}
