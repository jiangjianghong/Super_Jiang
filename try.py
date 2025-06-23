from model_factory.mode_factory import AI


ai = AI()
ai.create_model("test_01")

user_message_1 = "写一个一千字的文章，主题是“人工智能的未来”"
print(f"--- 尝试调用 ai.invoke('{user_message_1}', stream=False) ---")
response = ai.invoke(user_message_1, stream=True) 
for chunk in response:
    print(f"{chunk}", end='', flush=True)

