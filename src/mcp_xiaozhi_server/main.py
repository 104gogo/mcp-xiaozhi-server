from mcp.server.fastmcp import FastMCP
from .controller import XiaoZhiServerController

# Initialize FastMCP server with name "XiaoZhiServer"
mcp = FastMCP("XiaoZhiServer")

# Create an instance of XiaoZhiServerController for handling XiaoZhiServer API operations
controller = XiaoZhiServerController()

@mcp.tool()
async def modify_agent(agent_number: int, feature: str, new_value: str) -> dict:
    """修改智能体数据。
    参数：
    agent_number: 智能体编号（1表示第一个，2表示第二个，以此类推）
    feature: 要修改的功能，支持："大语言模型", "TTS模型", "角色音色", "角色模板", "名称"
    new_value: 新的值，如："豆包", "豆包语音合成", "男声", "湾湾小何", "新名字"
    """
    return controller.modify_xiaozhi_agent(agent_number, feature, new_value)
    
@mcp.tool()
def get_agent_list(query: str = "all") -> dict:
    """获取智能体列表信息。支持查询：'count'/'数量' - 获取智能体总数, 'first'/'第一个' - 获取第一个智能体信息, 'all' - 获取所有智能体列表"""
    return controller.get_xiaozhi_agent_list(query)
    


def run_server():
    """启动 MCP 服务器"""
    # Run the MCP server using standard input/output for communication
    mcp.run(transport='stdio')


if __name__ == "__main__":
    run_server()
    