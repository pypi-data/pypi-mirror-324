"""
AGI Open Network China Models
中国领先的 AI 模型调用框架
"""

from .providers.siliconflow import (
    SiliconFlowClient,
    ChatModel as SiliconFlowChatModel,
    TextModel as SiliconFlowTextModel,
    ImageModel as SiliconFlowImageModel,
    AudioModel as SiliconFlowAudioModel,
    VideoModel as SiliconFlowVideoModel,
)

__version__ = "0.1.0"
__all__ = [
    "SiliconFlowClient",
    "SiliconFlowChatModel",
    "SiliconFlowTextModel",
    "SiliconFlowImageModel",
    "SiliconFlowAudioModel",
    "SiliconFlowVideoModel",
] 