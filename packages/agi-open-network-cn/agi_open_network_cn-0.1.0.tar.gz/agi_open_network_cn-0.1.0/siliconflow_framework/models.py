from typing import List, Dict, Any, Optional

class BaseModel:
    """基础模型类"""
    def __init__(self, client):
        self.client = client

class ChatModel(BaseModel):
    """聊天模型"""
    AVAILABLE_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "chatglm-turbo",
        "chatglm-pro",
        "chatglm-std",
        "chatglm-lite",
        "qwen-turbo",
        "qwen-plus",
    ]
    
    def __init__(self, client, model_name: str = "gpt-3.5-turbo"):
        super().__init__(client)
        self.model_name = model_name
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """发送聊天请求"""
        return self.client.chat_completion(
            messages=messages,
            model=self.model_name,
            **kwargs
        )
    
    def simple_chat(self, message: str, **kwargs) -> str:
        """简单的聊天接口"""
        response = self.chat([{"role": "user", "content": message}], **kwargs)
        return response["choices"][0]["message"]["content"]

class TextModel(BaseModel):
    """文本模型"""
    AVAILABLE_MODELS = [
        "text-davinci-003",
        "text-embedding-ada-002",
    ]
    
    def __init__(self, client, model_name: str = "text-davinci-003"):
        super().__init__(client)
        self.model_name = model_name
    
    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """文本补全"""
        return self.client.text_completion(
            prompt=prompt,
            model=self.model_name,
            **kwargs
        )
    
    def simple_complete(self, prompt: str, **kwargs) -> str:
        """简单的文本补全接口"""
        response = self.complete(prompt, **kwargs)
        return response["choices"][0]["text"]

class ImageModel(BaseModel):
    """图像模型"""
    AVAILABLE_MODELS = [
        "stable-diffusion-3-5-large-turbo",
        "stable-diffusion-xl",
        "FLUX.1-schnell",
        "Pro/black-forest-labs/FLUX.1-schnell",
    ]
    
    def __init__(self, client, model_name: str = "stable-diffusion-3-5-large-turbo"):
        super().__init__(client)
        self.model_name = model_name
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成图像"""
        return self.client.image_generation(
            prompt=prompt,
            model=self.model_name,
            **kwargs
        )
    
    def simple_generate(self, prompt: str, **kwargs) -> str:
        """简单的图像生成接口"""
        response = self.generate(prompt, **kwargs)
        return response["data"][0]["url"]

class AudioModel(BaseModel):
    """音频模型"""
    def __init__(self, client):
        super().__init__(client)
    
    def transcribe(self, audio_file: str, **kwargs) -> Dict[str, Any]:
        """语音转文本"""
        return self.client.audio_transcription(audio_file, **kwargs)
    
    def synthesize(self, text: str, **kwargs) -> Dict[str, Any]:
        """文本转语音"""
        return self.client.text_to_speech(text, **kwargs)
    
    def simple_transcribe(self, audio_file: str, **kwargs) -> str:
        """简单的语音转文本接口"""
        response = self.transcribe(audio_file, **kwargs)
        return response["text"]
    
    def simple_synthesize(self, text: str, **kwargs) -> bytes:
        """简单的文本转语音接口"""
        response = self.synthesize(text, **kwargs)
        return response["audio"]

class VideoModel(BaseModel):
    """视频模型"""
    def __init__(self, client):
        super().__init__(client)
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成视频"""
        return self.client.video_generation(prompt, **kwargs)
    
    def get_status(self, request_id: str) -> Dict[str, Any]:
        """获取视频生成状态"""
        return self.client.get_video_status(request_id)
    
    def simple_generate(self, prompt: str, **kwargs) -> str:
        """简单的视频生成接口"""
        response = self.generate(prompt, **kwargs)
        request_id = response["request_id"]
        # 注意：这里需要轮询获取结果，实际使用时建议使用异步方式
        status_response = self.get_status(request_id)
        return status_response["url"] 