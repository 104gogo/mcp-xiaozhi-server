# MCP 小智服务器

MCP 小智服务器是一个基于 Model Context Protocol (MCP) 的智能体管理工具，可以对小智平台的智能体进行各种操作和配置。

## 功能特性

- 修改智能体的大语言模型
- 修改智能体的 TTS 模型
- 修改智能体的角色音色
- 修改智能体的角色模板
- 修改智能体的名称

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install mcp-xiaozhi-server
```

### 从源码安装

```bash
git clone https://github.com/yourusername/mcp-xiaozhi-server.git
cd mcp-xiaozhi-server
pip install -e .
```

## 使用方法

### 命令行启动

安装后，可以通过命令行启动服务器：

```bash
mcp-xiaozhi-server --host https://api.xiaozhi.com --token your_api_token
```

### 参数说明

- `--host`: 小智 API 主机地址（必填）
- `--token`: 小智 API 访问令牌（必填）
- `--version`, `-v`: 显示版本信息

### 作为 Python 模块使用

```python
from mcp_xiaozhi_server import XiaoZhiServerController
from mcp_xiaozhi_server.config import Config, set_config

# 设置配置
config = Config(api_host="https://api.xiaozhi.com", api_token="your_api_token")
set_config(config)

# 创建控制器
controller = XiaoZhiServerController()

# 修改智能体
result = controller.modify_xiaozhi_agent(
    agent_number=1,
    feature="大语言模型", 
    new_value="豆包"
)
print(result)
```

## 支持的功能

### 修改大语言模型
```python
controller.modify_xiaozhi_agent(1, "大语言模型", "豆包")
controller.modify_xiaozhi_agent(1, "语言模型", "智谱")
controller.modify_xiaozhi_agent(1, "LLM", "通义")
```

### 修改 TTS 模型
```python
controller.modify_xiaozhi_agent(1, "TTS模型", "豆包语音合成")
controller.modify_xiaozhi_agent(1, "语音合成", "阿里语音合成")
```

### 修改角色音色
```python
controller.modify_xiaozhi_agent(1, "角色音色", "男声")
controller.modify_xiaozhi_agent(1, "音色", "女声")
```

### 修改角色模板
```python
controller.modify_xiaozhi_agent(1, "角色模板", "助手")
controller.modify_xiaozhi_agent(1, "模板", "客服")
```

### 修改名称
```python
controller.modify_xiaozhi_agent(1, "名称", "新名字")
```

## 开发

### 克隆仓库

```bash
git clone https://github.com/yourusername/mcp-xiaozhi-server.git
cd mcp-xiaozhi-server
```

### 安装开发依赖

```bash
pip install -e .
```

### 运行

```bash
python -m mcp_xiaozhi_server.cli --host https://api.xiaozhi.com --token your_token
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！