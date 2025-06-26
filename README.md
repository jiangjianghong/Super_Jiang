# Super_Jiang 智能体项目

此项目拟构建一个智能体，集成多种AI模型和工具功能。

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置设置
项目需要配置AI模型和工具的API密钥：

#### 模型配置
```bash
cp config/config_models.py.example config/config_models.py
```
然后编辑 `config/config_models.py`，填入你的AI模型API密钥。

#### 工具配置  
```bash
cp config/config_tools.py.example config/config_tools.py
```
然后编辑 `config/config_tools.py`，填入你的工具API密钥（如Google搜索API等）。

### 3. 运行测试
```bash
python try.py
```

## 项目结构
- `config/` - 配置文件目录
- `model_factory/` - AI模型工厂
- `prompt_factory/` - 提示词工厂  
- `tools_factory/` - 工具工厂
- `try.py` - 测试运行文件

## 注意事项
- 配置文件包含敏感信息，已被 `.gitignore` 忽略
- 请妥善保管你的API密钥，不要提交到版本控制系统