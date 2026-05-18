# Aible OS

> 一个基于 AI Agent 的桌面操作系统 —— 像安装手机 App 一样安装和使用 AI 能力。

**Aible OS** 是一款 macOS 桌面应用（Tauri + Python FastAPI），让你在一个简洁的桌面上管理和使用各种 AI Agent。内置 5 个开箱即用的 AI App，并且支持从应用商店安装更多能力。

---

## ✨ 界面预览

```
┌──────────────────────────────────────────────────────┐
│  Aible OS                                ⚙️  🛒     │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  ✍️       │  │  🎨      │  │  🌐      │          │
│  │ 写作助手  │  │ AI 绘画  │  │ 翻译大师 │          │
│  ├──────────┤  ├──────────┤  ├──────────┤          │
│  │ 工具      │  │ 创作     │  │ 工具     │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│                                                      │
│  ┌──────────┐  ┌──────────┐                          │
│  │  💻      │  │  📖      │                          │
│  │ 代码助手 │  │ 故事工坊 │                          │
│  ├──────────┤  ├──────────┤                          │
│  │ 开发     │  │ 创作     │                          │
│  └──────────┘  └──────────┘                          │
│                         + 前往商店发现更多 →          │
└──────────────────────────────────────────────────────┘
```

### 🎨 设计风格

- **极简桌面** — 纯白卡片网格布局，圆角大图标，氛围轻松
- **沉浸式聊天** — 点击 App 卡片展开全屏对话界面，支持流式 SSE 输出
- **明快色彩** — 每个 App 有独立毛玻璃主题色（写作助手的蓝色 → 绘画的紫色 → 故事的金色）
- **桌面级体验** — 原生 macOS 窗口控制，设置面板侧边弹出，应用商店全屏浏览

---

## 🧩 AI App 机制

### 当前：提示词驱动（v0.1）

每个 AI App 由一个 `manifest.yaml`（元数据）+ `prompt.txt`（系统提示词）定义：

**manifest.yaml**
```yaml
app_id: translate-master
name: 翻译大师
tagline: 多语言翻译，地道表达
description: 支持中、英、日、韩、法、德等多语种互译，保留原文风格。
icon: 🌐
category: 工具
color: from-green-500 to-emerald-600
author: Aible OS
capabilities:
  - llm.chat
```

**prompt.txt**
```
你是一个专业的翻译助手。...
```

这种模式上手简单——任何人都可以通过写一个 `manifest.yaml` + `prompt.txt` 来创建一个 AI App。

### 🔮 未来：工具化 Agent（Roadmap）

v0.1 只是第一步。后续版本将支持更强大的 App 类型：

| 能力 | 说明 | 示例 |
|------|------|------|
| `llm.chat` | 对话式 LLM | ✅ 当前所有 App |
| `llm.tools` | LLM + 工具调用 | 📌 代码执行、文件读写、API 调用 |
| `agent.custom` | 自定义 Agent 逻辑 | 📌 Python/JS 脚本扩展，多步推理 |
| `agent.multi` | 多 Agent 协作 | 📌 不同 App 之间编排协作 |

**这意味着未来的 App 将不只是"一个提示词"，而是真正的智能体——能读文件、写代码、调用 API、联网搜索、实时协作。**

---

## 🚀 快速使用

### 下载已打包的应用（推荐）

[![Download](https://img.shields.io/github/v/release/magictong/aible-os?label=Download&color=blue)](https://github.com/magictong/aible-os/releases/latest)

从 [Releases](https://github.com/magictong/aible-os/releases) 下载 `Aible_OS_x.x.x_aarch64.dmg` 安装包，解压安装后打开：

1. 点击右上角 ⚙️ 设置
2. 填写 LLM API Key / Base URL / Model
3. 点"保存"（配置立即生效，无需重启）
4. 回到桌面，选择一个 AI App 开始使用

### 从源码构建

```bash
# 依赖
brew install python@3.10 node@20 rust

# 后端 Python 依赖
cd runtime
pip3 install -r requirements.txt
pip3 install sse-starlette
cd ..

# 前端依赖
cd frontend
npm install
cd ..

# 构建桌面应用
cd frontend
PATH="$HOME/.cargo/bin:$PATH" npx tauri build
```

构建产物在 `frontend/src-tauri/target/release/bundle/`，支持 .app 和 .dmg 格式。

### 开发模式运行

```bash
# 终端 1: 启动后端
cd runtime
python3 standalone.py --port 8765

# 终端 2: 启动前端开发服务器
cd frontend
npm run dev
```

访问 `http://localhost:3000` 即可预览实时刷新开发版本。

> **注意：** `standalone.py` 使用 `uvicorn.run()` 直接启动 FastAPI 应用，适合开发调试。生产环境使用 Tauri 内嵌的 Rust 启动器。

---

## 🔧 配置

### 设置页面（推荐）

打开 App → 右上角 ⚙️ → 填入以下信息 → 保存：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `LLM_API_KEY` | API 密钥 | （必填） |
| `LLM_BASE_URL` | API 地址 | `https://open.bigmodel.cn/api/paas/v4` |
| `LLM_MODEL` | 模型名称 | `glm-4-plus` |

### 配置文件

用户设置保存在 `~/Library/Application Support/Aible OS/config.json`：

```json
{
  "LLM_API_KEY": "sk-xxx",
  "LLM_BASE_URL": "https://open.bigmodel.cn/api/paas/v4",
  "LLM_MODEL": "glm-4-plus"
}
```

### 配置优先级

```
用户保存的 config.json  >  环境变量 / .env  >  代码内默认值
```

---

## 📁 项目结构

```
aible-os/
├── README.md
├── .gitignore
├── .env.example
│
├── frontend/                    # 前端（Tauri + Next.js 16）
│   ├── src/                     # React / TypeScript 源码
│   │   ├── app/                 # Next.js App Router（桌面主页）
│   │   ├── components/          # 组件（AppCard, AppStore, AppWindow...）
│   │   └── lib/                 # API 客户端（api.ts）
│   ├── src-tauri/               # Tauri (Rust)
│   │   ├── src/                 # Rust 启动器源码
│   │   ├── runtime/             # 内嵌的 Python 后端运行时（与 runtime/ 同步）
│   │   ├── resources/           # Tauri 资源文件
│   │   └── binaries/            # 编译后端 + 启动脚本
│   ├── package.json
│   └── next.config.ts
│
├── runtime/                     # Python 后端源码
│   ├── api/                     # FastAPI 路由
│   │   ├── apps.py              # App 安装/卸载/列表
│   │   ├── chat.py              # 对话流式 SSE
│   │   ├── settings.py          # 配置管理
│   │   └── auth.py              # 认证
│   ├── core/                    # 核心引擎
│   │   ├── engine.py            # LLM 引擎（流式调用）
│   │   ├── session.py           # 对话会话管理
│   │   └── app_loader.py        # App 加载器
│   ├── models/                  # SQLAlchemy 数据模型
│   ├── config.py                # 配置读写（优先级处理）
│   ├── main.py                  # FastAPI 应用入口
│   ├── standalone.py            # 独立启动脚本
│   └── requirements.txt
│
├── apps/                        # AI App 定义目录
│   └── built-in/                # 内置 App
│       ├── ai-painter/
│       ├── code-helper/
│       ├── storyteller/
│       ├── translate-master/
│       └── writing-assistant/
│
└── scripts/                     # 构建脚本
    ├── build-venv.sh            # 构建内嵌 Python 运行时
    └── start.sh                 # 开发用启动脚本
```

---

## 🛠 技术栈

| 层 | 技术 |
|----|------|
| **桌面壳** | Tauri 2.x (Rust) — 轻量原生壳，打包不到 5MB |
| **前端** | Next.js 16 + React 19 + TypeScript + Tailwind CSS 4 |
| **后端** | Python 3.10+ / FastAPI + SQLAlchemy 2.0 + SQLite / aiosqlite |
| **AI 协议** | OpenAI 兼容 API（流式 SSE），支持任意 LLM 服务商 |
| **状态管理** | SQLite + 应用内内存会话缓存 |
| **构建打包** | Tauri bundle → macOS .app / .dmg |

---

## 🤝 贡献

Aible OS 欢迎社区贡献！你可以：

- **创建 AI App** — 只需要写一个 `manifest.yaml` 和一个 `prompt.txt`，就能做出自己的 AI App
- **开发工具箱** — 当 `llm.tools` 能力上线后，可以给 App 添加代码执行、文件读写、API 调用等工具
- **提交 PR** — 改进前端界面、优化后端性能、增加新能力
- **反馈 Issue** — 遇到的 Bug、想要的功能、使用建议

---

## 🔒 安全

- API 密钥存储在用户目录的 `config.json`
- 前端密码框使用 `type="password"` 掩码显示
- 运行时内部路径不会暴露到前端
- `.env` 已加入 `.gitignore`
- 配置更新后即时生效，无需重启

---

## 📄 License

MIT — 欢迎 Fork、修改、分发。这是我的第一个 AI 开源项目 🎉
