# 🤍 AI-女友（琪琪）

一个本地运行的 AI 桌面女友项目，支持浮窗聊天、记忆系统、个性化人设。

> 安静陪伴，不聒噪 🌅

## ✨ 功能特性

- 🗨️ **浮窗聊天**：桌面悬浮气泡，随时对话
- 🧠 **记忆系统**：长期记住对话内容和偏好
- 🎭 **人设定制**：可自定义性格、口头禅、头像
- 💬 **多轮对话**：基于大模型的自然对话
- 🖥️ **桌面端运行**：Windows 本地运行，保护隐私

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Windows 系统（当前版本）

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/drifter-stram/ai-girlfriend.git
cd ai-girlfriend
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置文件
```bash
# 复制配置模板，填入你的 API Key
cp config.example.json config.json
```
编辑 `config.json`，填入你的大模型 API 密钥。

4. 运行
```bash
python main.py
```

## 📁 项目结构

```
ai-girlfriend/
├── main.py              # 程序入口
├── config.example.json  # 配置模板
├── requirements.txt     # Python依赖
├── src/
│   ├── core/           # 核心模块（对话引擎、记忆、配置、人设）
│   └── ui/             # UI模块（浮窗、气泡、对话框、托盘）
├── assets/             # 资源文件（头像等）
└── docs/               # 文档
    └── v3_plan/        # V3版本规划与补丁
```

## 📝 版本说明

- **V1**：基础桌面浮窗聊天
- **V2**：记忆系统、人设定制
- **V3（规划中）**：局域网同步、移动端适配、桌面补丁

详细版本规划见 [docs/v3_plan/](./docs/v3_plan/)

## ⚠️ 注意事项

- `config.json` 包含你的 API Key，**请勿上传到公开仓库**
- 本项目仅供学习交流使用
- 使用大模型 API 会产生费用，请注意用量

## 📄 License

MIT License
