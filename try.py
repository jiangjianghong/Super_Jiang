from model_factory.mode_factory import AI
import time


ai = AI()
ai.create_model("test_01")

user_message_1 = "你需要用最快的速度一次性返回一个一万字的故事，故事内容是：6 。不要有空行，不要有换行符，直接返回一万字的故事。"
print(f"--- 尝试调用 ai.invoke('{user_message_1}', stream=False) ---")
response = ai.invoke(user_message_1, stream=True) 
for chunk in response:
    print(f"{chunk}", end='', flush=True)
    time.sleep(0.1)  # 模拟流式输出的延迟

