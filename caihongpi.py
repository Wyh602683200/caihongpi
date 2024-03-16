import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://api.qqsuu.cn/api/" #https://api.qqsuu.cn/

@plugins.register(name="caihongpi",
                  desc="获取彩虹屁",
                  version="1.0",
                  author="wyh",
                  desire_priority=100)


class caihongpi(Plugin):

    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【夸我】获取彩虹屁"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()
        
        if self.content == "夸我":
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.caihongpi()
            if result != None:
                reply.type = ReplyType.TEXT
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS


    def caihongpi(self):
        url = BASE_URL_DM + "dm-caihongpi"
        params = "type=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            # 主接口
            response = requests.get(url=url, params=params, headers=headers,timeout=2)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('code') == 200 and  json_data['data']['content']:
                    text = json_data['data']['content']
                    logger.info(f"主接口获取成功：{text}")
                    return text
                else:
                    logger.error(f"主接口返回值异常:{json_data}")
                    raise ValueError('not found')
            else:
                logger.error(f"主接口请求失败:{response.text}")
                raise Exception('request failed')
        except Exception as e:
            logger.error(f"接口异常：{e}")
                
        logger.error("所有接口都挂了,无法获取")
        return None










