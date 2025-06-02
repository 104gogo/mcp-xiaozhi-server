#!/usr/bin/env python3
"""
构建和发布脚本
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """运行命令并检查结果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}完成")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败:")
        print(f"错误: {e.stderr}")
        sys.exit(1)


def clean_build():
    """清理构建目录"""
    print("🧹 清理旧的构建文件...")
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        run_command(f"rm -rf {pattern}", f"删除 {pattern}")


def build_package():
    """构建包"""
    print("📦 构建 Python 包...")
    run_command("python -m build", "构建包")


def check_package():
    """检查包"""
    print("🔍 检查包...")
    run_command("python -m twine check dist/*", "检查包")


def install_locally():
    """本地安装包进行测试"""
    print("🔧 本地安装包...")
    run_command("pip install -e .", "本地安装")


def test_installation():
    """测试安装"""
    print("🧪 测试安装...")
    try:
        import mcp_xiaozhi_server
        print(f"✅ 包导入成功，版本: {mcp_xiaozhi_server.__version__}")
    except ImportError as e:
        print(f"❌ 包导入失败: {e}")
        sys.exit(1)


def publish_to_pypi():
    """发布到 PyPI"""
    choice = input("是否要发布到 PyPI? (y/N): ").lower()
    if choice == 'y':
        print("🚀 发布到 PyPI...")
        run_command("python -m twine upload dist/*", "上传到 PyPI")
        print("🎉 发布完成!")
    else:
        print("⏭️ 跳过发布到 PyPI")


def main():
    """主函数"""
    print("=" * 50)
    print("🏗️  MCP 小智服务器构建脚本")
    print("=" * 50)
    
    # 确保在项目根目录
    if not Path("setup.py").exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    try:
        # 清理
        clean_build()
        
        # 构建
        build_package()
        
        # 检查
        check_package()
        
        # 本地安装测试
        install_locally()
        
        # 测试导入
        test_installation()
        
        # 询问是否发布
        publish_to_pypi()
        
        print("\n🎉 所有步骤完成!")
        print("\n📝 使用说明:")
        print("   安装: pip install mcp-xiaozhi-server")
        print("   运行: xiaozhi-server --host <HOST> --token <TOKEN>")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 操作被用户取消")
        sys.exit(1)


if __name__ == "__main__":
    main() 