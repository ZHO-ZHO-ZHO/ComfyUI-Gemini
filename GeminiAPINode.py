import os
import io
import json
import requests
import torch
import google.generativeai as genai
from io import BytesIO
from PIL import Image

p = os.path.dirname(os.path.realpath(__file__))

def get_gemini_api_key():
    try:
        config_path = os.path.join(p, 'config.json')
        with open(config_path, 'r') as f:  
            config = json.load(f)
        api_key = config["GEMINI_API_KEY"]
    except:
        print("出错啦 Error: API key is required")
        return ""
    return api_key

class Gemini_API_Zho:

    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "model_name": (["gemini-pro", "gemini-pro-vision", "gemini-1.5-pro-latest"],),
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
            genai.configure(api_key=self.api_key,transport='rest')
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

        if model_name == 'gemini-1.5-pro-latest':
            if image == None:
                if stream:
                    response = model.generate_content(prompt, stream=True)
                    textoutput = "\n".join([chunk.text for chunk in response])
                else:
                    response = model.generate_content(prompt)
                    textoutput = response.text
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
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Describe this image", "multiline": True}),
                "image_url": ("STRING", {"default": ""}),
                "model_name": (["gemini-pro-vision", "gemini-1.5-pro-latest"],),
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
            genai.configure(api_key=self.api_key,transport='rest')
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

#chat
class Gemini_API_Chat_Zho:

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.chat = None  # 初始化时，聊天实例为空
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "model_name": (["gemini-pro", "gemini-1.5-pro-latest"],),
                "api_key": ("STRING", {"default": ""})  # Add api_key as an input
            },
            "optional": {
                "image": ("IMAGE",),  
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "generate_chat"

    CATEGORY = "Zho模块组/✨Gemini"
    
    def generate_chat(self, prompt, model_name, api_key):
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=self.api_key,transport='rest')
        if not self.api_key:
            raise ValueError("API key is required")

        if not self.chat:
            model = genai.GenerativeModel(model_name)
            self.chat = model.start_chat(history=[])

        if model_name == 'gemini-pro':
            response = self.chat.send_message(prompt)
            textoutput = response.text
            chat_history = self.format_chat_history(self.chat)

        if model_name == 'gemini-1.5-pro-latest':
            if image == None:
                response = self.chat.send_message(prompt)
                textoutput = response.text
                chat_history = self.format_chat_history(self.chat)
            else:
                # 转换图像
                pil_image = self.tensor_to_image(image)

                response = self.chat.send_message([prompt, pil_image])
                textoutput = response.text
                chat_history = self.format_chat_history(self.chat)
        
        return (chat_history,)

    def format_chat_history(self, chat):
        formatted_history = []
        for message in chat.history:
            formatted_message = f"{message.role}: {message.parts[0].text}"
            formatted_history.append(formatted_message)
            formatted_history.append("-" * 40)  # 添加分隔线
        return "\n".join(formatted_history)


class Gemini_API_S_Zho:

    def __init__(self):
        self.api_key = get_gemini_api_key()
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "model_name": (["gemini-pro", "gemini-pro-vision", "gemini-1.5-pro-latest"],),
                "stream": ("BOOLEAN", {"default": False}),
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

    def generate_content(self, prompt, model_name, stream, image=None):
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

        if model_name == 'gemini-1.5-pro-latest':
            if image == None:
                if stream:
                    response = model.generate_content(prompt, stream=True)
                    textoutput = "\n".join([chunk.text for chunk in response])
                else:
                    response = model.generate_content(prompt)
                    textoutput = response.text
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


class Gemini_API_S_Vsion_ImgURL_Zho:

    def __init__(self):
        self.api_key = get_gemini_api_key()
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Describe this image", "multiline": True}),
                "image_url": ("STRING", {"default": ""}),
                "model_name": (["gemini-pro-vision", "gemini-1.5-pro-latest"],),
                "stream": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "Zho模块组/✨Gemini"

    def generate_content(self, prompt, model_name, stream, image_url):
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


#chat
class Gemini_API_S_Chat_Zho:

    def __init__(self):
        self.api_key = get_gemini_api_key()
        self.chat = None  # 初始化时，聊天实例为空
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "model_name": (["gemini-pro", "gemini-1.5-pro-latest"],),
            },
            "optional": {
                "image": ("IMAGE",),  
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "generate_chat"

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
    
    def generate_chat(self, prompt, model_name):
        if not self.api_key:
            raise ValueError("API key is required")

        if not self.chat:
            model = genai.GenerativeModel(model_name)
            self.chat = model.start_chat(history=[])

        if model_name == 'gemini-pro':
            response = self.chat.send_message(prompt)
            textoutput = response.text
            chat_history = self.format_chat_history(self.chat)

        if model_name == 'gemini-1.5-pro-latest':
            if image == None:
                response = self.chat.send_message(prompt)
                textoutput = response.text
                chat_history = self.format_chat_history(self.chat)
            else:
                # 转换图像
                pil_image = self.tensor_to_image(image)

                response = self.chat.send_message([prompt, pil_image])
                textoutput = response.text
                chat_history = self.format_chat_history(self.chat)
        
        return (chat_history,)

    def format_chat_history(self, chat):
        formatted_history = []
        for message in chat.history:
            formatted_message = f"{message.role}: {message.parts[0].text}"
            formatted_history.append(formatted_message)
            formatted_history.append("-" * 40)  # 添加分隔线
        return "\n".join(formatted_history)


# System instructions
class Gemini_15P_API_S_Advance_Zho:

    def __init__(self):
        self.api_key = get_gemini_api_key()
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "system_instruction": ("STRING", {"default": "You are creating a prompt for Stable Diffusion to generate an image. First step: describe this image, then put description into text. Second step: generate a text prompt for %s based on first step.  Only respond with the prompt itself, but embellish it as needed but keep it under 80 tokens.", "multiline": True}),
                "model_name": (["gemini-1.5-pro-latest"],),
                "stream": ("BOOLEAN", {"default": False}),
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

    def generate_content(self, prompt, system_instruction, model_name, stream, image=None):
        if not self.api_key:
            raise ValueError("API key is required")

        model = genai.GenerativeModel(model_name, system_instruction=system_instruction)

        if image == None:
            if stream:
                response = model.generate_content(prompt, stream=True)
                textoutput = "\n".join([chunk.text for chunk in response])
            else:
                response = model.generate_content(prompt)
                textoutput = response.text
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


class Gemini_15P_API_S_Chat_Advance_Zho:

    def __init__(self):
        self.api_key = get_gemini_api_key()
        self.chat = None  # 初始化时，聊天实例为空
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "system_instruction": ("STRING", {"default": "You are creating a prompt for Stable Diffusion to generate an image. First step: describe this image, then put description into text. Second step: generate a text prompt for %s based on first step.  Only respond with the prompt itself, but embellish it as needed but keep it under 80 tokens.", "multiline": True}),
                "model_name": (["gemini-1.5-pro-latest"],),
            },
            "optional": {
                "image": ("IMAGE",),  
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "generate_chat"

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

    def generate_chat(self, prompt, system_instruction, model_name, image=None):
        if not self.api_key:
            raise ValueError("API key is required")

        if not self.chat:
            model = genai.GenerativeModel(model_name, system_instruction=system_instruction)
            self.chat = model.start_chat(history=[])

        if model_name == 'gemini-1.5-pro-latest':
            if image == None:
                response = self.chat.send_message(prompt)
                textoutput = response.text
                chat_history = self.format_chat_history(self.chat)
            else:
                # 转换图像
                pil_image = self.tensor_to_image(image)

                response = self.chat.send_message([prompt, pil_image])
                textoutput = response.text
                chat_history = self.format_chat_history(self.chat)
        
        return (chat_history,)

    def format_chat_history(self, chat):
        formatted_history = []
        for message in chat.history:
            formatted_message = f"{message.role}: {message.parts[0].text}"
            formatted_history.append(formatted_message)
            formatted_history.append("-" * 40)  # 添加分隔线
        return "\n".join(formatted_history)


# File API
class Gemini_FileUpload_API_S_Zho:

    def __init__(self):
        self.api_key = get_gemini_api_key()
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file": ("STRING", {"default": "./sample.mp3", "multiline": False}),
            }
        }

    RETURN_TYPES = ("FILE",)
    RETURN_NAMES = ("file",)
    FUNCTION = "file_upload"

    CATEGORY = "Zho模块组/✨Gemini"

    def file_upload(self, file):
        if not self.api_key:
            raise ValueError("API key is required")

        your_file = genai.upload_file(file)

        return [your_file]


class Gemini_File_API_S_Zho:

    def __init__(self):
        self.api_key = get_gemini_api_key()
        if self.api_key is not None:
            genai.configure(api_key=self.api_key,transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file": ("FILE",),
                "prompt": ("STRING", {"default": "Listen carefully to the following audio file. Provide a brief summary.", "multiline": True}),
                "model_name": (["gemini-1.5-pro-latest"],),
                "stream": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "Zho模块组/✨Gemini"

    def generate_content(self, prompt, model_name, stream, file):
        if not self.api_key:
            raise ValueError("API key is required")

        model = genai.GenerativeModel(model_name)

        if stream:
            response = model.generate_content([prompt, file], stream=True)
            textoutput = "\n".join([chunk.text for chunk in response])
        else:
            response = model.generate_content([prompt, file])
            textoutput = response.text

        return (textoutput,)


class ConcatText_Zho:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True}),
                "text_2": ("STRING", {"multiline": True}),
                # 可以根据需要添加更多的文本输入
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "concat_texts"

    CATEGORY = "Zho模块组/✨Gemini"

    def concat_texts(self, **kwargs):
        # 将所有输入的文本合并为一个以逗号分隔的字符串
        texts = [kwargs[key] for key in kwargs if key.startswith('text')]
        combined_text = ', '.join(texts)
        return (combined_text,)


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
    "Gemini_API_Chat_Zho": Gemini_API_Chat_Zho,
    "Gemini_API_S_Zho": Gemini_API_S_Zho,
    "Gemini_API_S_Vsion_ImgURL_Zho": Gemini_API_S_Vsion_ImgURL_Zho,
    "Gemini_API_S_Chat_Zho": Gemini_API_S_Chat_Zho,
    "Gemini_15P_API_S_Advance_Zho": Gemini_15P_API_S_Advance_Zho,
    "Gemini_15P_API_S_Chat_Advance_Zho": Gemini_15P_API_S_Chat_Advance_Zho,
    "Gemini_FileUpload_API_S_Zho": Gemini_FileUpload_API_S_Zho,
    "Gemini_File_API_S_Zho": Gemini_File_API_S_Zho,
    "ConcatText_Zho": ConcatText_Zho,
    "DisplayText_Zho": DisplayText_Zho
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_API_Zho": "✨Gemini_API_Zho",
    "Gemini_API_Vsion_ImgURL_Zho": "✨Gemini_API_Vsion_ImgURL_Zho",
    "Gemini_API_Chat_Zho": "✨Gemini_API_Chat_Zho",
    "Gemini_API_S_Zho": "㊙️Gemini_Zho",
    "Gemini_API_S_Vsion_ImgURL_Zho": "㊙️Gemini_ImgURL_Zho",
    "Gemini_API_S_Chat_Zho": "㊙️Gemini_Chat_Zho",
    "Gemini_15P_API_S_Advance_Zho": "🆕Gemini_15P_Advance_Zho",
    "Gemini_15P_API_S_Chat_Advance_Zho": "🆕Gemini_15P_Chat_Advance_Zho",
    "Gemini_FileUpload_API_S_Zho": "📄Gemini_FileUpload_Zho",
    "Gemini_File_API_S_Zho": "📄Gemini_File_Zho",
    "ConcatText_Zho": "✨ConcatText_Zho",
    "DisplayText_Zho": "✨DisplayText_Zho"
}
