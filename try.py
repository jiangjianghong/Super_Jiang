from model_factory.mode_factory import AI
from prompt_factory.prompt_base import get_prompt_base
import json
from tools_factory.tools import execute_tool

ai = AI()
ai.create_model("test_01")
prompt = get_prompt_base()
# print(f"提示词为：\n {prompt} \n")
ai.set_prompt(prompt)

response = ai.invoke("小米su7的颜色")
response_json = json.loads(response)
print(f"大模型输出为:\n {response_json}\n")
for key in response_json:
    if key == "tool":
        tools_name = response_json["tool"]
        tools_args = response_json["args"]
        tools_res = execute_tool(tools_name, tools_args)
        print(tools_res)




