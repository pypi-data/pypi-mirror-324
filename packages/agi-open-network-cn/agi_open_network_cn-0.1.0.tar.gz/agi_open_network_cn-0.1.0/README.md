# AGI Open Network China Models

A simple yet powerful framework for accessing Chinese AI models. Currently supports the full range of SiliconFlow models, with plans to support more Chinese AI service providers in the future.

## Features

- 🚀 Simple and intuitive API interface
- 🎯 Support for multiple model types (Chat, Text, Image, Audio, Video)
- 🔧 Flexible configuration options
- 📚 Comprehensive documentation and examples
- 🛠 Complete type hints

## Installation

```bash
pip install agi-open-network-cn
```

## Quick Start

### SiliconFlow Models

```python
from agi_open_network_cn import (
    SiliconFlowClient,
    SiliconFlowChatModel,
    SiliconFlowImageModel,
    SiliconFlowAudioModel,
)

# Initialize client
client = SiliconFlowClient(api_key="your-api-key")

# Use ChatGLM
chat_model = SiliconFlowChatModel(client, model_name="chatglm-turbo")
response = chat_model.simple_chat("Tell me about ChatGLM")
print(response)

# Use Stable Diffusion to generate images
image_model = SiliconFlowImageModel(client)
image_url = image_model.simple_generate("A cute Chinese dragon")
print(image_url)

# Speech to text
audio_model = SiliconFlowAudioModel(client)
text = audio_model.simple_transcribe("speech.mp3")
print(text)
```

## Supported Models and Features

### SiliconFlow

#### Chat Models
- ChatGLM Series
  - chatglm-turbo: General-purpose model with balanced performance
  - chatglm-pro: Professional version with enhanced capabilities
  - chatglm-std: Standard version with good cost-performance ratio
  - chatglm-lite: Lightweight version for faster responses
- Qwen Series
  - qwen-turbo: Qwen general version
  - qwen-plus: Qwen enhanced version
- GPT Series
  - gpt-3.5-turbo
  - gpt-4

#### Image Models
- Stable Diffusion Series
  - stable-diffusion-3-5-large-turbo: Latest version, faster generation
  - stable-diffusion-xl: Large model for higher quality
- FLUX Series
  - FLUX.1-schnell: High-performance image generation
  - Pro/black-forest-labs/FLUX.1-schnell: Professional version

#### Audio Features
- Speech to Text: Supports multiple languages and scenarios
- Text to Speech: High naturalness with emotional expression
- Custom Voice: Support for voice cloning

#### Video Features
- Text to Video: Supports various styles and scenarios
- Async Generation: Support for long video generation
- Auto Status Query: Convenient progress tracking

## Advanced Usage

### Custom Model Parameters

```python
# Using advanced parameters
response = chat_model.chat(
    messages=[
        {"role": "system", "content": "You are a professional Python teacher"},
        {"role": "user", "content": "Explain decorators"},
    ],
    temperature=0.7,
    max_tokens=2000,
    top_p=0.9,
)
```

### Batch Processing

```python
# Batch image generation
prompts = [
    "Chinese ink painting: Mountains and waters",
    "Chinese ink painting: Plum blossoms",
    "Chinese ink painting: Bamboo",
]

for prompt in prompts:
    image_url = image_model.simple_generate(prompt)
    print(f"{prompt}: {image_url}")
```

### Async Video Generation

```python
from agi_open_network_cn import SiliconFlowVideoModel

video_model = SiliconFlowVideoModel(client)
response = video_model.generate("A video showcasing Chinese traditional culture")
request_id = response["request_id"]

# Poll for results
while True:
    status = video_model.get_status(request_id)
    if status["status"] == "completed":
        print(f"Video URL: {status['url']}")
        break
    time.sleep(10)
```

## Error Handling

```python
from agi_open_network_cn.exceptions import AGIOpenNetworkError

try:
    response = chat_model.simple_chat("Hello")
except AGIOpenNetworkError as e:
    print(f"Error occurred: {e}")
```

## Contributing

We welcome all forms of contributions, including but not limited to:

- Submitting issues and suggestions
- Improving documentation
- Adding new features
- Fixing bugs
- Adding new model providers

## License

MIT License

## Contact Us

- Website: https://www.agiopen.network
- GitHub: https://github.com/agiopennetwork/agi-open-network-cn
- Email: info@agiopen.network 