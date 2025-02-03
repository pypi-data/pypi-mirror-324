import requests
from typing import Optional, Dict, Any, List

class SiliconFlowClient:
    """SiliconFlow API 客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.siliconflow.cn"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送 API 请求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_models(self) -> List[Dict[str, Any]]:
        """获取可用模型列表"""
        return self._make_request("GET", "/models")
    
    def chat_completion(self, messages: list, model: str = "gpt-3.5-turbo", **kwargs) -> Dict[str, Any]:
        """聊天补全 API"""
        data = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        return self._make_request("POST", "/chat/completions", json=data)
    
    def text_completion(self, prompt: str, model: str = "text-davinci-003", **kwargs) -> Dict[str, Any]:
        """文本补全 API"""
        data = {
            "model": model,
            "prompt": prompt,
            **kwargs
        }
        return self._make_request("POST", "/completions", json=data)
    
    def image_generation(self, prompt: str, model: str = "stable-diffusion-3-5-large-turbo", **kwargs) -> Dict[str, Any]:
        """图像生成 API"""
        data = {
            "model": model,
            "prompt": prompt,
            **kwargs
        }
        return self._make_request("POST", "/images/generations", json=data)
    
    def audio_transcription(self, audio_file: str, **kwargs) -> Dict[str, Any]:
        """语音转文本 API"""
        data = {
            "file": audio_file,
            **kwargs
        }
        return self._make_request("POST", "/audio/transcriptions", json=data)
    
    def text_to_speech(self, text: str, **kwargs) -> Dict[str, Any]:
        """文本转语音 API"""
        data = {
            "text": text,
            **kwargs
        }
        return self._make_request("POST", "/audio/speech", json=data)
    
    def video_generation(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """视频生成 API"""
        data = {
            "prompt": prompt,
            **kwargs
        }
        return self._make_request("POST", "/video/submit", json=data)
    
    def get_video_status(self, request_id: str) -> Dict[str, Any]:
        """获取视频生成状态"""
        return self._make_request("POST", "/video/status", json={"request_id": request_id}) 