# MCP 小智服务器

MCP 小智服务器是一个基于 Model Context Protocol (MCP) 的智能体管理工具，可以对小智平台的智能体进行各种操作和配置。

## 功能特性

- 修改智能体的大语言模型
- 修改智能体的 TTS 模型
- 修改智能体的角色音色
- 修改智能体的角色模板
- 修改智能体的名称
- 获取智能体列表信息

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

# 获取智能体列表
list_result = controller.get_xiaozhi_agent_list("all")
print(list_result)
```

## 支持的功能

### 1. 修改智能体配置

#### 修改大语言模型
```python
controller.modify_xiaozhi_agent(1, "大语言模型", "豆包")
controller.modify_xiaozhi_agent(1, "语言模型", "智谱")
controller.modify_xiaozhi_agent(1, "LLM", "通义")
```

#### 修改 TTS 模型
```python
controller.modify_xiaozhi_agent(1, "TTS模型", "豆包语音合成")
controller.modify_xiaozhi_agent(1, "语音合成", "阿里语音合成")
```

#### 修改角色音色
```python
controller.modify_xiaozhi_agent(1, "角色音色", "男声")
controller.modify_xiaozhi_agent(1, "音色", "女声")
```

#### 修改角色模板
```python
controller.modify_xiaozhi_agent(1, "角色模板", "助手")
controller.modify_xiaozhi_agent(1, "模板", "客服")
```

#### 修改名称
```python
controller.modify_xiaozhi_agent(1, "名称", "新名字")
```

### 2. 获取智能体列表信息

#### 获取所有智能体列表
```python
# 获取所有智能体的完整信息
result = controller.get_xiaozhi_agent_list("all")
print(f"共有 {result['data']['total_count']} 个智能体")
```

#### 获取智能体总数
```python
# 使用中文关键词
result = controller.get_xiaozhi_agent_list("数量")
print(result['data']['message'])  # 输出: "一共有 X 个智能体"

# 使用英文关键词
result = controller.get_xiaozhi_agent_list("count")
print(f"总数: {result['data']['total_count']}")
```

#### 获取第一个智能体信息
```python
# 获取第一个智能体的完整信息
result = controller.get_xiaozhi_agent_list("第一个")
first_agent = result['data']
print(f"第一个智能体: {first_agent.get('agentName')}")

# 只获取第一个智能体的名称
result = controller.get_xiaozhi_agent_list("第一个名称")
print(result['data']['message'])  # 输出: "第一个智能体的名字是: XXX"

# 获取第一个智能体的设备数量
result = controller.get_xiaozhi_agent_list("第一个设备")
print(result['data']['message'])  # 输出: "第一个智能体 'XXX' 有 N 个设备"
```

#### 支持的查询关键词

**获取总数**：
- 中文：`数量`, `多少`, `总数`, `个数`
- 英文：`count`

**获取第一个智能体**：
- 中文：`第一个`, `第一`, `首个`
- 英文：`first`

**特定信息查询**：
- 名称：`名字`, `名称`, `name`
- 设备：`设备`, `device`

## MCP 工具

当作为 MCP 服务器运行时，提供以下工具：

### modify_agent
修改智能体配置的工具。

**参数**：
- `agent_number` (int): 智能体编号（1表示第一个）
- `feature` (str): 要修改的功能
- `new_value` (str): 新的值

### get_agent_list
获取智能体列表信息的工具。

**参数**：
- `query` (str, 可选): 查询类型，默认为 "all"

## 开发

### 虚拟环境设置（推荐）

#### 使用 Conda
```bash
# 创建环境
conda create -n mcp-xiaozhi python=3.11
conda activate mcp-xiaozhi

# 安装依赖
pip install -r requirements.txt
```

#### 使用 Python venv
```bash
# 创建环境
python -m venv venv

# 激活环境 (Windows)
venv\Scripts\activate
# 激活环境 (macOS/Linux)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 本地运行

```bash
# 以开发模式安装
pip install -e .

# 运行服务器
python -m mcp_xiaozhi_server.cli --host https://api.xiaozhi.com --token your_token

# 或者直接运行
mcp-xiaozhi-server --host https://api.xiaozhi.com --token your_token
```

### 构建和发布

```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 检查包
python -m twine check dist/*

# 发布到 PyPI
python -m twine upload dist/*
```

## 配置方式

支持两种配置方式：

### 1. 命令行参数（推荐）
```bash
mcp-xiaozhi-server --host https://api.xiaozhi.com --token your_api_token
```

### 2. 环境变量
```bash
export XIAOZHI_API_HOST="https://api.xiaozhi.com"
export XIAOZHI_API_TOKEN="your_api_token"
```

然后使用：
```python
from mcp_xiaozhi_server.config import Config
config = Config.from_env()
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.1.0
- 初始版本
- 支持修改智能体配置（大语言模型、TTS模型、角色音色、角色模板、名称）
- 支持获取智能体列表信息
- 支持多种查询方式和关键词