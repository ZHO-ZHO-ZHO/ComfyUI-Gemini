<p align="center"><img  src="https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/ec15bc39-8111-417b-afc5-67cdfb3a9df5" alt="Gemini项目图" /></p>

<!---
![Gemini项目图](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/ec15bc39-8111-417b-afc5-67cdfb3a9df5)
--->

<h1 align="center">Gemini in ComfyUI</h1>
<!---
# Gemini in ComfyUI
--->


![Dingtalk_20231220204257](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/07c68b08-858b-4233-a48b-1069552fc8d8)



V2.0 聊天机器人节点

https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/cb64ee29-a983-47fd-b26b-55386314afdd



## 项目介绍 | Info

- 将 Google Gemini 引入到 ComfyUI 中，现在你可以用它为你生成提示词、描述图像，也可与它畅聊人生

- 目前 Gemini API 免费开放，你可以在这里申请一个自己的 API Key：[Gemini API 申请](https://makersuite.google.com/app/apikey)

- 版本：V2.1 新增上下文聊天节点（相当于聊天机器人）💬 ，修复 Deadline of 60.0s bug

## 详细说明 | Features

- Gemini 目前提供 2 种模型：

   - Gemini-pro: 文本模型

   - Genimi-pro-vision: 文本 + 图像模型

- 2 类节点:

   - 隐式 API KEY：将 Gemini_API_Key 设置为了环境变量，更安全，方便分享工作流（不会外泄 API KEY）
     
       ㊙️Gemini_Zho：同时支持两种模型，其中 Genimi-pro-vision 可接受图像作为输入
     
       ㊙️Gemini_Vsion_ImgURL_Zho：Genimi-pro-vision 模型，接受图像链接作为输入
     
       💬Gemini_Chat_Zho：Genimi-pro 模型，支持上下文窗口，聊天机器人（Genimi-pro-vision 本身还未支持上下文功能）

   - 显式API KEY：直接在节点中输入 Gemini_API_Key，仅供个人私密使用，请勿将包含 API KEY 的工作流分享出去
     
       ✨Gemini_API_Zho：同时支持两种模型，其中 Genimi-pro-vision 可接受图像作为输入
  
       ✨Gemini_API_Vsion_ImgURL_Zho：Genimi-pro-vision 模型，接受图像链接作为输入
     
       💬Gemini_API_Chat_Zho：：Genimi-pro 模型，支持上下文窗口，聊天机器人（Genimi-pro-vision 本身还未支持上下文功能）

- 辅助节点:

   - ✨DisplayText_Zho：显示文本
     
   - ✨ConcatText_Zho：使用 “，” 连接文本

- 节点示例：

![Dingtalk_20231220180446](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/3cba8d69-09bb-470c-940c-7f796c869d63)

聊天机器人

![image](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/8a38f437-0148-4777-b872-e88995dd53d2)


## 参数说明 | Parameters

- image（非必要）：选择 Gemini-pro 时无需接入图像，选择 Genimi-pro-vision 时需要接入图像
- prompt：提示词
- model_name：模型选择，Gemini-pro 或 Genimi-pro-vision
- stream：流式传输响应
- api_key：输入 Gemini_API_Key （仅在显式节点上有）

## 使用方法 | How to use

- 首先需要申请一个自己的 Gemini_API_Key：[Gemini API 申请](https://makersuite.google.com/app/apikey) 

- 选择隐式节点㊙️（推荐）：将你的 Gemini_API_Key 添加到 `config.json` 文件中，运行时会自动加载

- 选择显示节点✨：直接将 Gemini_API_Key 输入到节点的 api_key 中（注意：请勿将包含此节点的工作流分享出去，以免泄露你的 API Key）

- 使用注意：本地使用请确保你可以有效连接到 Google Gemini 的服务，推荐使用 Colab 或 Kaggle（无连接问题）

## 安装 | Install

- 推荐使用管理器 ComfyUI Manager 安装

- 手动安装：
    1. `cd custom_nodes`
    2. `git clone https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini.git`
    3. `cd custom_nodes/ComfyUI-Gemini`
    4. `pip install -r requirements.txt`
    5. 重启 ComfyUI

## 工作流 | Workflow

### V2.0 工作流（隐式）（V1.1工作流依旧可用）

[Gemini-pro Chatbot【Zho】](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/blob/main/Gemini_workflows/Gemini-pro%20Chatbot%E3%80%90Zho%E3%80%91.json)

![image](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/8a38f437-0148-4777-b872-e88995dd53d2)

### V1.1 工作流（隐式）

[Gemini-pro【Zho】](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/blob/main/Gemini_workflows/Gemini-pro%E3%80%90Zho%E3%80%91.json) 

![Dingtalk_20231220183708](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/7f0e222a-2de4-4c5b-883a-2172667d1d5b)

[Genimi-pro-vision【Zho】](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/blob/main/Gemini_workflows/Gemini-pro-vision%E3%80%90Zho%E3%80%91.json)

![Dingtalk_20231220192932](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/db4f4bf6-a0cf-42af-ac5a-7e2afd1bda93)

![Dingtalk_20231220190218](https://github.com/ZHO-ZHO-ZHO/ComfyUI-Gemini/assets/140084057/5bb57f7b-f00f-454a-9435-c1b8a02ae71a)


## 更新日志 | Changelog

20231229

- V2.1版：修复 Deadline of 60.0s bug，方法来自官方：https://github.com/google/generative-ai-python/issues/117

20231222

- V2.0版：新增上下文聊天节点，相当于聊天机器人
    - 💬Gemini_Chat_Zho（隐式）
    - 💬Gemini_API_Chat_Zho（显示）

20231221

- V1.1版：修改 API KEY 的加载方式为自动添加 config.json ，将 API KEY 写入即可
  
- 已登陆 manager 不用手动安装了

20231220

- 实现 Genimi-pro-vision 模型调用，支持图像或图像链接输入
- 增加隐式节点，更加安全
- 增加辅助节点

20231219

- 创建 ComfyUI Gemini 项目，实现 Gemini-pro 模型调用


## Stars 

[![Star History Chart](https://api.star-history.com/svg?repos=ZHO-ZHO-ZHO/ComfyUI-Gemini&type=Timeline)](https://star-history.com/#ZHO-ZHO-ZHO/ComfyUI-Gemini&Timeline)


## Credits

- DisplayText节点参考了：[ComfyUI_Custom_Nodes_AlekPet](https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet)，感谢 AlekPet ！
