# 模型工厂 用于创建模型实例
from openai import OpenAI
from config.config_models import MODELS_CONFIG

class AI:
    def __init__(self):
        self.message_history = []

    def create_model(self, config_name: str, **kwargs):
        if config_name not in MODELS_CONFIG:
            raise ValueError(f"配置 '{config_name}' 不存在")

        config = MODELS_CONFIG[config_name]
        self.model_name = config["model_name"]
        self.client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
        # 系统提示词
        prompt = kwargs.get("prompt", None)
        if prompt:
            self.prompt = prompt
        else:
            self.prompt = "You are a helpful assistant."
        self.message_history = [{"role": "system", "content": self.prompt}]

    def set_prompt(self, prompt: str):
        """设置系统提示词"""
        if prompt:
            self.prompt = prompt
            # 更新消息历史中的系统消息
            self.message_history[0] = {"role": "system", "content": self.prompt}

    def invoke(self, user_mes: str, **kwargs):
        """发送消息并获取响应"""
        # 添加用户消息到历史
        self.message_history.append({"role": "user", "content": user_mes})
        
        # 获取AI响应
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.message_history,
            **kwargs
        )
        
        # 提取响应内容
        assistant_message = response.choices[0].message.content
        
        # 添加助手响应到历史
        self.message_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message

    def single_invoke(self, user_mes: str, **kwargs):
        """单次对话，不保存历史记录"""
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": user_mes}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **kwargs
        )
        
        return response.choices[0].message.content

    def clear_history(self):
        """清空对话历史，保留系统消息"""
        self.message_history = [{"role": "system", "content": self.prompt}]