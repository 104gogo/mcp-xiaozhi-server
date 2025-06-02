"""
配置管理模块
"""

import os
from typing import Tuple


class Config:
    """配置类"""
    
    def __init__(self, api_host: str = None, api_token: str = None):
        self.api_host = api_host
        self.api_token = api_token
    
    @classmethod
    def from_env(cls) -> 'Config':
        """从环境变量创建配置"""
        return cls(
            api_host=os.getenv('XIAOZHI_API_HOST'),
            api_token=os.getenv('XIAOZHI_API_TOKEN')
        )
    
    def validate(self) -> None:
        """验证配置是否完整"""
        if not self.api_host:
            raise ValueError("API 主机地址不能为空")
        if not self.api_token:
            raise ValueError("API 令牌不能为空")
    
    def get_api_config(self) -> Tuple[str, str]:
        """获取 API 配置元组"""
        self.validate()
        return self.api_host, self.api_token


# 全局配置实例
_config: Config = None


def set_config(config: Config) -> None:
    """设置全局配置"""
    global _config
    _config = config


def get_api_config() -> Tuple[str, str]:
    """获取 API 配置
    
    返回:
        Tuple[str, str]: (api_host, api_token)
    
    抛出:
        ValueError: 当配置未设置或不完整时
    """
    if _config is None:
        raise ValueError("配置未初始化，请先调用 set_config()")
    return _config.get_api_config() 