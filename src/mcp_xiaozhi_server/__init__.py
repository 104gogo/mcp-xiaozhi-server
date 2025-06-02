"""
MCP 小智服务器包
"""

from .xiaozhi_server import XiaoZhiServerController
from .cli import main

__version__ = "0.1.0"
__all__ = ["XiaoZhiServerController", "main"] 