import logging
import requests
import json
from .config import get_api_config

# 设置日志
logger = logging.getLogger(__name__)

class XiaoZhiServerController:
    """
    小智服务器控制器
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def modify_xiaozhi_agent(self, agent_number: int, feature: str, new_value: str) -> dict:
        """修改智能体数据。
        参数：
        agent_number: 智能体编号（1表示第一个，2表示第二个，以此类推）
        feature: 要修改的功能，支持："大语言模型", "TTS模型", "角色音色", "角色模板", "名称"
        new_value: 新的值，如："豆包", "豆包语音合成", "男声", "湾湾小何", "新名字"
        """
        
        try:
            # 动态获取API配置
            api_host, api_token = get_api_config()
            
            # 转换为数组索引（用户输入1代表第一个，对应索引0）
            agent_index = agent_number - 1
            if agent_index < 0:
                return {"success": False, "error": "智能体编号必须大于0"}
            
            # 第一步：获取智能体列表
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"开始修改第{agent_number}个智能体的{feature}为{new_value}")
            
            # 获取智能体列表
            response = requests.get(f"{api_host}/xiaozhi/agent/list", headers=headers, timeout=10)
            if response.status_code != 200:
                return {"success": False, "error": f"获取智能体列表失败，状态码: {response.status_code}"}
            
            agent_list_data = response.json()
            if agent_list_data.get("code") != 0:
                return {"success": False, "error": f"获取智能体列表失败: {agent_list_data.get('msg')}"}
            
            agents = agent_list_data.get("data", [])
            if len(agents) <= agent_index:
                return {"success": False, "error": f"没有找到第{agent_number}个智能体，当前共有{len(agents)}个智能体"}
            
            target_agent = agents[agent_index]
            agent_id = target_agent.get("id")
            agent_name = target_agent.get("agentName")
            
            logger.info(f"找到目标智能体: {agent_name} (ID: {agent_id})")
            
            # 第二步：获取智能体详细信息
            detail_response = requests.get(f"{api_host}/xiaozhi/agent/{agent_id}", headers=headers, timeout=10)
            if detail_response.status_code != 200:
                return {"success": False, "error": f"获取智能体详情失败，状态码: {detail_response.status_code}"}
            
            detail_data = detail_response.json()
            if detail_data.get("code") != 0:
                return {"success": False, "error": f"获取智能体详情失败: {detail_data.get('msg')}"}
            
            agent_detail = detail_data.get("data", {})
            logger.info(f"获取智能体详情成功")
            
            # 第三步：根据功能类型处理修改
            update_data = agent_detail.copy()
            
            if feature in ["大语言模型", "语言模型", "LLM", "模型"]:
                # 获取模型列表
                models_response = requests.get(f"{api_host}/xiaozhi/models/names?modelType=LLM&modelName=", headers=headers, timeout=10)
                if models_response.status_code != 200:
                    return {"success": False, "error": f"获取模型列表失败，状态码: {models_response.status_code}"}
                
                models_data = models_response.json()
                if models_data.get("code") != 0:
                    return {"success": False, "error": f"获取模型列表失败: {models_data.get('msg')}"}
                
                models = models_data.get("data", [])
                
                # 匹配模型名称
                target_model_id = None
                new_value_lower = new_value.lower()
                
                # 定义模型关键词映射
                model_keywords = {
                    "豆包": ["豆包", "doubao"],
                    "智谱": ["智谱", "chatglm", "glm"],
                    "通义": ["通义", "ali", "阿里"],
                    "coze": ["coze"],
                    "deepseek": ["deepseek"],
                    "dify": ["dify"]
                }
                
                # 先尝试关键词匹配
                for keyword, search_terms in model_keywords.items():
                    if any(term in new_value_lower for term in search_terms):
                        for model in models:
                            model_name_lower = model.get("modelName", "").lower()
                            if any(term in model_name_lower for term in search_terms):
                                target_model_id = model.get("id")
                                logger.info(f"匹配到模型: {model.get('modelName')} (ID: {target_model_id})")
                                break
                        if target_model_id:
                            break
                
                # 如果关键词匹配失败，尝试直接名称匹配
                if not target_model_id:
                    for model in models:
                        if new_value_lower in model.get("modelName", "").lower():
                            target_model_id = model.get("id")
                            logger.info(f"直接匹配到模型: {model.get('modelName')} (ID: {target_model_id})")
                            break
                
                if target_model_id:
                    update_data["llmModelId"] = target_model_id
                    logger.info(f"准备更新大语言模型为: {target_model_id}")
                else:
                    available_models = [model.get("modelName") for model in models]
                    return {"success": False, "error": f"未找到匹配的大语言模型'{new_value}'，可用模型: {', '.join(available_models)}"}
            
            elif feature in ["TTS模型", "TTS", "语音合成", "语音合成模型"]:
                # 获取TTS模型列表
                tts_models_response = requests.get(f"{api_host}/xiaozhi/models/names?modelType=TTS&modelName=", headers=headers, timeout=10)
                if tts_models_response.status_code != 200:
                    return {"success": False, "error": f"获取TTS模型列表失败，状态码: {tts_models_response.status_code}"}
                
                tts_models_data = tts_models_response.json()
                if tts_models_data.get("code") != 0:
                    return {"success": False, "error": f"获取TTS模型列表失败: {tts_models_data.get('msg')}"}
                
                tts_models = tts_models_data.get("data", [])
                
                # 匹配TTS模型名称
                target_tts_model_id = None
                new_value_lower = new_value.lower()
                
                # 定义TTS模型关键词映射
                tts_model_keywords = {
                    "豆包": ["豆包", "doubao"],
                    "阿里": ["阿里", "aliyun", "阿里云"],
                    "硅基": ["硅基", "silicon", "硅基流动"],
                    "coze": ["coze"],
                    "自定义": ["自定义", "custom"],
                    "acgn": ["acgn"]
                }
                
                # 先尝试关键词匹配
                for keyword, search_terms in tts_model_keywords.items():
                    if any(term in new_value_lower for term in search_terms):
                        for tts_model in tts_models:
                            model_name_lower = tts_model.get("modelName", "").lower()
                            if any(term in model_name_lower for term in search_terms):
                                target_tts_model_id = tts_model.get("id")
                                logger.info(f"匹配到TTS模型: {tts_model.get('modelName')} (ID: {target_tts_model_id})")
                                break
                        if target_tts_model_id:
                            break
                
                # 如果关键词匹配失败，进行模糊匹配
                if not target_tts_model_id:
                    for tts_model in tts_models:
                        model_name = tts_model.get("modelName", "")
                        model_name_lower = model_name.lower()
                        
                        # 模糊匹配：检查用户输入是否包含在模型名称中
                        if new_value_lower in model_name_lower:
                            target_tts_model_id = tts_model.get("id")
                            logger.info(f"模糊匹配到TTS模型: {model_name} (ID: {target_tts_model_id})")
                            break
                        
                        # 反向模糊匹配：检查模型名称中的关键部分是否匹配用户输入
                        name_parts = model_name_lower.replace("tts", "").replace("语音合成", "").strip()
                        if name_parts and name_parts in new_value_lower:
                            target_tts_model_id = tts_model.get("id")
                            logger.info(f"反向模糊匹配到TTS模型: {model_name} (ID: {target_tts_model_id})")
                            break
                
                if target_tts_model_id:
                    update_data["ttsModelId"] = target_tts_model_id
                    logger.info(f"准备更新TTS模型为: {target_tts_model_id}")
                    
                    # 获取新TTS模型的音色列表，设置第一个音色为默认音色
                    voices_response = requests.get(f"{api_host}/xiaozhi/models/{target_tts_model_id}/voices?voiceName=", 
                                                headers=headers, timeout=10)
                    if voices_response.status_code == 200:
                        voices_data = voices_response.json()
                        if voices_data.get("code") == 0:
                            voices = voices_data.get("data", [])
                            if voices:
                                first_voice_id = voices[0].get("id")
                                first_voice_name = voices[0].get("name")
                                update_data["ttsVoiceId"] = first_voice_id
                                logger.info(f"同步更新音色为第一个音色: {first_voice_name} (ID: {first_voice_id})")
                            else:
                                logger.warning(f"TTS模型 {target_tts_model_id} 没有可用音色")
                        else:
                            logger.warning(f"获取TTS模型音色列表失败: {voices_data.get('msg')}")
                    else:
                        logger.warning(f"获取TTS模型音色列表失败，状态码: {voices_response.status_code}")
                else:
                    available_tts_models = [model.get("modelName") for model in tts_models]
                    return {"success": False, "error": f"未找到匹配的TTS模型'{new_value}'，可用模型: {', '.join(available_tts_models)}"}
            
            elif feature in ["角色音色", "音色", "声音", "语音"]:
                # 获取当前智能体的TTS模型ID
                current_tts_model_id = agent_detail.get("ttsModelId")
                if not current_tts_model_id:
                    return {"success": False, "error": "无法获取当前TTS模型ID"}
                
                # 获取该TTS模型的音色列表
                voices_response = requests.get(f"{api_host}/xiaozhi/models/{current_tts_model_id}/voices?voiceName=", 
                                            headers=headers, timeout=10)
                if voices_response.status_code != 200:
                    return {"success": False, "error": f"获取音色列表失败，状态码: {voices_response.status_code}"}
                
                voices_data = voices_response.json()
                if voices_data.get("code") != 0:
                    return {"success": False, "error": f"获取音色列表失败: {voices_data.get('msg')}"}
                
                voices = voices_data.get("data", [])
                
                # 匹配音色
                target_voice_id = None
                new_value_lower = new_value.lower()
                
                # 定义音色关键词映射（只保留通用的男声女声匹配）
                voice_keywords = {
                    "男声": ["男声", "男", "male"],
                    "女声": ["女声", "女", "female"]
                }
                
                # 先尝试关键词匹配
                for keyword, search_terms in voice_keywords.items():
                    if any(term in new_value_lower for term in search_terms):
                        for voice in voices:
                            voice_name_lower = voice.get("name", "").lower()
                            if any(term in voice_name_lower for term in search_terms):
                                target_voice_id = voice.get("id")
                                logger.info(f"匹配到音色: {voice.get('name')} (ID: {target_voice_id})")
                                break
                        if target_voice_id:
                            break
                
                # 如果关键词匹配失败，进行模糊匹配
                if not target_voice_id:
                    for voice in voices:
                        voice_name = voice.get("name", "")
                        voice_name_lower = voice_name.lower()
                        
                        # 模糊匹配：检查用户输入是否包含在音色名称中
                        if new_value_lower in voice_name_lower:
                            target_voice_id = voice.get("id")
                            logger.info(f"模糊匹配到音色: {voice_name} (ID: {target_voice_id})")
                            break
                        
                        # 反向模糊匹配：检查音色名称中的关键部分是否匹配用户输入
                        # 提取音色名称中的关键词（去掉前缀如"EdgeTTS"）
                        name_parts = voice_name_lower.replace("edgetts", "").replace("tts", "").strip()
                        if name_parts and name_parts in new_value_lower:
                            target_voice_id = voice.get("id")
                            logger.info(f"反向模糊匹配到音色: {voice_name} (ID: {target_voice_id})")
                            break
                
                if target_voice_id:
                    update_data["ttsVoiceId"] = target_voice_id
                    logger.info(f"准备更新TTS音色ID为: {target_voice_id}")
                else:
                    available_voices = [voice.get("name") for voice in voices]
                    return {"success": False, "error": f"未找到匹配的音色'{new_value}'，可用音色: {', '.join(available_voices)}"}
            
            elif feature in ["角色模板", "模板", "智能体模板"]:
                # 获取角色模板列表
                template_response = requests.get(f"{api_host}/xiaozhi/agent/template", headers=headers, timeout=10)
                if template_response.status_code != 200:
                    return {"success": False, "error": f"获取角色模板列表失败，状态码: {template_response.status_code}"}
                
                template_data = template_response.json()
                if template_data.get("code") != 0:
                    return {"success": False, "error": f"获取角色模板列表失败: {template_data.get('msg')}"}
                
                templates = template_data.get("data", [])
                
                # 匹配模板名称
                target_template = None
                new_value_lower = new_value.lower()
                
                # 进行模糊匹配
                for template in templates:
                    template_name = template.get("agentName", "")
                    template_name_lower = template_name.lower()
                    
                    # 模糊匹配：检查用户输入是否包含在模板名称中
                    if new_value_lower in template_name_lower:
                        target_template = template
                        logger.info(f"模糊匹配到角色模板: {template_name}")
                        break
                    
                    # 反向模糊匹配：检查模板名称是否在用户输入中
                    if template_name_lower in new_value_lower:
                        target_template = template
                        logger.info(f"反向模糊匹配到角色模板: {template_name}")
                        break
                
                if target_template:
                    # 更新智能体名称和系统提示词
                    update_data["agentName"] = target_template.get("agentName")
                    update_data["systemPrompt"] = target_template.get("systemPrompt")
                    
                    logger.info(f"准备更新角色模板为: {target_template.get('agentName')}")
                    logger.info(f"系统提示词长度: {len(target_template.get('systemPrompt', ''))}")
                else:
                    available_templates = [template.get("agentName") for template in templates]
                    return {"success": False, "error": f"未找到匹配的角色模板'{new_value}'，可用模板: {', '.join(available_templates)}"}
            
            elif feature in ["名称", "名字"]:
                if new_value.strip():
                    update_data["agentName"] = new_value.strip()
                    logger.info(f"准备更新智能体名称为: {new_value}")
                else:
                    return {"success": False, "error": "新名称不能为空"}
            
            else:
                supported_features = ["大语言模型", "TTS模型", "角色音色", "角色模板", "名称"]
                return {"success": False, "error": f"暂不支持修改'{feature}'，目前支持的功能: {', '.join(supported_features)}"}
            
            # 第四步：执行更新
            put_response = requests.put(f"{api_host}/xiaozhi/agent/{agent_id}", 
                                    headers=headers, 
                                    json=update_data, 
                                    timeout=10)
            
            if put_response.status_code != 200:
                return {"success": False, "error": f"更新智能体失败，状态码: {put_response.status_code}"}
            
            put_result = put_response.json()
            if put_result.get("code") != 0:
                return {"success": False, "error": f"更新智能体失败: {put_result.get('msg')}"}
            
            logger.info(f"智能体 {agent_name} 的 {feature} 修改成功")
            return {
                "success": True, 
                "data": {
                    "agent_number": agent_number,
                    "agent_name": agent_name,
                    "agent_id": agent_id,
                    "feature": feature,
                    "new_value": new_value,
                    "message": f"智能体 '{agent_name}' 的 {feature} 已修改为 '{new_value}'"
                }
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求异常: {str(e)}")
            return {"success": False, "error": f"网络请求失败: {str(e)}"}
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            return {"success": False, "error": f"响应数据解析失败: {str(e)}"}
        except ValueError as e:
            logger.error(f"环境变量错误: {str(e)}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"修改智能体时发生未知错误: {str(e)}")
            return {"success": False, "error": f"修改失败: {str(e)}"}

    def get_xiaozhi_agent_list(self, query: str = "all") -> dict:
        """获取智能体列表信息。支持查询：'count'/'数量' - 获取智能体总数, 'first'/'第一个' - 获取第一个智能体信息, 'all' - 获取所有智能体列表"""
        
        try:
            # 动态获取API配置
            api_host, api_token = get_api_config()
            
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
            
            # 发送GET请求
            response = requests.get(f"{api_host}/xiaozhi/agent/list", headers=headers, timeout=10)
            
            # 检查响应状态
            if response.status_code != 200:
                logger.error(f"API请求失败，状态码: {response.status_code}")
                return {
                    "success": False, 
                    "error": f"API请求失败，状态码: {response.status_code}"
                }
            
            # 解析JSON响应
            data = response.json()
            
            # 检查API返回的code
            if data.get("code") != 0:
                logger.error(f"API返回错误，code: {data.get('code')}, msg: {data.get('msg')}")
                return {
                    "success": False,
                    "error": f"API返回错误: {data.get('msg', '未知错误')}"
                }
            
            # 获取智能体列表
            agent_list = data.get("data", [])
            
            # 根据查询类型返回相应数据
            query_lower = query.lower()
            
            # 查询智能体总数
            if any(keyword in query_lower for keyword in ["count", "数量", "多少", "总数", "个数"]):
                result = {
                    "total_count": len(agent_list),
                    "message": f"一共有 {len(agent_list)} 个智能体"
                }
                logger.info(f"获取智能体总数: {len(agent_list)}")
                return {"success": True, "data": result}
            
            # 查询第一个智能体信息
            elif any(keyword in query_lower for keyword in ["first", "第一个", "第一", "首个"]):
                if len(agent_list) > 0:
                    first_agent = agent_list[0]
                    
                    # 如果查询包含"名字"或"名称"
                    if any(keyword in query_lower for keyword in ["名字", "名称", "name"]):
                        result = {
                            "agent_name": first_agent.get("agentName"),
                            "message": f"第一个智能体的名字是: {first_agent.get('agentName')}"
                        }
                        logger.info(f"获取第一个智能体名字: {first_agent.get('agentName')}")
                        return {"success": True, "data": result}
                    
                    # 如果查询包含"设备"
                    elif any(keyword in query_lower for keyword in ["设备", "device"]):
                        device_count = first_agent.get("deviceCount", 0)
                        result = {
                            "device_count": device_count,
                            "agent_name": first_agent.get("agentName"),
                            "message": f"第一个智能体 '{first_agent.get('agentName')}' 有 {device_count} 个设备"
                        }
                        logger.info(f"获取第一个智能体设备数: {device_count}")
                        return {"success": True, "data": result}
                    
                    # 返回第一个智能体的完整信息
                    else:
                        logger.info(f"获取第一个智能体完整信息: {first_agent.get('agentName')}")
                        return {"success": True, "data": first_agent}
                else:
                    return {
                        "success": False,
                        "error": "没有找到任何智能体"
                    }
            
            # 返回所有智能体列表
            else:
                result = {
                    "total_count": len(agent_list),
                    "agents": agent_list
                }
                logger.info(f"获取所有智能体列表，共 {len(agent_list)} 个")
                return {"success": True, "data": result}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求异常: {str(e)}")
            return {"success": False, "error": f"网络请求失败: {str(e)}"}
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            return {"success": False, "error": f"响应数据解析失败: {str(e)}"}
        except ValueError as e:
            logger.error(f"环境变量错误: {str(e)}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            return {"success": False, "error": f"未知错误: {str(e)}"}