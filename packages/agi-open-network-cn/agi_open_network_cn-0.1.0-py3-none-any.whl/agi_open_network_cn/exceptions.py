"""
AGI Open Network 异常处理模块
"""

class AGIOpenNetworkError(Exception):
    """AGI Open Network 基础异常类"""
    pass

class ProviderError(AGIOpenNetworkError):
    """提供商相关错误"""
    pass

class AuthenticationError(AGIOpenNetworkError):
    """认证错误"""
    pass

class RateLimitError(AGIOpenNetworkError):
    """速率限制错误"""
    pass

class InvalidRequestError(AGIOpenNetworkError):
    """无效请求错误"""
    pass

class APIError(AGIOpenNetworkError):
    """API 调用错误"""
    pass

class ModelNotFoundError(AGIOpenNetworkError):
    """模型不存在错误"""
    pass 