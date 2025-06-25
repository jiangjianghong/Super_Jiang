# 模型工厂 用于创建模型实例
from openai import OpenAI
from config.config_models import MODELS_CONFIG

class AI:
    def __init__(self):
        self.message_history = []
        self.client = None
        self.model_name = None
        self.prompt = "You are a helpful assistant."

    def create_model(self, config_name: str, **kwargs):
        if config_name not in MODELS_CONFIG:
            raise ValueError(f"配置 '{config_name}' 不存在")

        config = MODELS_CONFIG[config_name]
        self.model_name = config["model_name"]
        self.client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
        
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
            self.message_history[0] = {"role": "system", "content": self.prompt}

    # 私有方法，用于实际进行 API 调用并处理流式迭代
    def _stream_response_generator(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True, # 这里强制为流式
            **kwargs
        )
        full_response_content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response_content += content
                yield content # 实时返回内容片段
        
        # 将完整的助手响应添加到历史 (仅针对invoke，single_invoke不需要)
        # 注意：这里需要考虑_stream_response_generator被single_invoke调用时的情况
        # 为了简化，我们可以让invoke和single_invoke自己负责添加到历史
        
        # 返回完整内容，供调用者处理（例如添加到历史）
        # yield 一个特殊标记或者直接返回完整内容的方式需要谨慎设计
        # 更好的方法是让调用者收集并添加到历史
        return full_response_content # 返回完整内容给调用方，但这不是通过 yield 返回的

    def invoke(self, user_mes: str, stream: bool = False, **kwargs):
        """发送消息并获取响应，支持流式输出"""
        self.message_history.append({"role": "user", "content": user_mes})
        
        if stream:
            # 如果是流式，我们返回一个生成器，该生成器同时将内容添加到历史
            def generator_with_history():
                collected_content = ""
                # 注意：这里调用 create 而不是 _stream_response_generator，因为后者已经处理了 yield
                # 这样做可以避免将 yield 放在 invoke 函数体中
                response_stream = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=self.message_history,
                    stream=True,
                    **kwargs
                )
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        collected_content += content
                        yield content
                # 流式结束后，将完整的回复添加到历史
                self.message_history.append({"role": "assistant", "content": collected_content})
            
            return generator_with_history() # 返回一个生成器对象
        else:
            # 非流式处理
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.message_history,
                stream=False, # 确保是非流式
                **kwargs
            )
            assistant_message = response.choices[0].message.content
            self.message_history.append({"role": "assistant", "content": assistant_message})
            return assistant_message

    def single_invoke(self, sys_prompt: str, user_mes: str, stream: bool = False, **kwargs):
        """单次对话，不保存历史记录，支持流式输出"""
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_mes}
        ]
        
        if stream:
            # 如果是流式，返回一个生成器
            def single_generator():
                response_stream = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    stream=True,
                    **kwargs
                )
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        yield content
            return single_generator() # 返回一个生成器对象
        else:
            # 非流式处理
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=False,
                **kwargs
            )
            return response.choices[0].message.content

    def clear_history(self):
        """清空对话历史，保留系统消息"""
        self.message_history = [{"role": "system", "content": self.prompt}]