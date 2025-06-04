"""
命令行界面模块
"""

import argparse
import sys
from .config import Config, set_config
from .main import run_server


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="MCP 小智服务器 - 智能体管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --host https://api.xiaozhi.com --token your_api_token
  %(prog)s --host https://api.xiaozhi.com --token your_api_token
        """
    )
    
    parser.add_argument(
        '--host',
        required=True,
        help='小智 API 主机地址 (必填)'
    )
    
    parser.add_argument(
        '--token',
        required=True,
        help='小智 API 访问令牌 (必填)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='mcp-xiaozhi-server 0.3.0'
    )
    
    return parser


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 创建并设置配置
    config = Config(api_host=args.host, api_token=args.token)
    
    try:
        config.validate()
        set_config(config)
        print(f"小智服务器启动中...")
        print(f"API 主机: {args.host}")
        print(f"配置验证通过，服务器启动...")
        
        # 启动服务器
        run_server()
        
    except ValueError as e:
        print(f"配置错误: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"启动失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 