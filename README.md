# Aible OS

> 一个基于 AI Agent 的桌面操作系统，让你像安装 App 一样安装和使用 AI 能力。

Aible OS 是一款 macOS 桌面应用（Tauri + Python FastAPI），内置 5 个开箱即用的 AI App：写作助手、AI 绘画、翻译大师、代码助手、故事工坊。

---

## 🚀 快速使用

### 下载已打包的应用

从 Releases 下载 `Aible OS_x.x.x_aarch64.dmg`，安装后打开：

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

访问 `http://localhost:3000` 即可预览。

> **注意：** `standalone.py` 会使用 `uvicorn.run()` 直接启动 FastAPI 应用，适合开发调试。生产环境使用 Tauri 内嵌的 Rust 启动器。

---

## 🧩 什么是 AI App？

每个 AI App 是一个包含 `manifest.yaml` 和 `prompt.txt` 的目录：

**manifest.yaml** — 定义 App 的元数据：
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

**prompt.txt** — AI 的系统提示词，定义 App 的行为：
```
你是一个专业的翻译助手。
...
```

目前所有内置 App 使用 `llm.chat`（对话式 LLM）能力，未来可扩展支持工具调用、代码执行等。

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
│
├── frontend/                    # 前端（Tauri + Next.js）
│   ├── src/                     # React / TypeScript 源码
│   │   ├── app/                 # Next.js App Router
│   │   ├── components/          # 组件（AppCard, AppStore, AppWindow...）
│   │   └── lib/                 # 工具（api.ts）
│   ├── src-tauri/               # Tauri (Rust)
│   │   ├── src/                 # Rust 源码（启动器）
│   │   ├── runtime/             # 内嵌的后端运行时
│   │   │   ├── api/             # API 路由
│   │   │   ├── core/            # 引擎 & 加载器
│   │   │   ├── models/          # 数据模型
│   │   │   ├── apps/            # AI App 定义
│   │   │   ├── config.py        # 配置管理
│   │   │   ├── main.py          # FastAPI 应用
│   │   │   └── standalone.py    # 独立启动入口
│   │   ├── resources/           # Tauri 资源（执行脚本等）
│   │   └── binaries/            # 构建时脚本
│   ├── package.json
│   └── next.config.ts
│
└── runtime/                     # 后端源码（开发用，与内嵌同步）
    ├── api/
    ├── core/
    ├── models/
    ├── apps/
    ├── config.py
    ├── main.py
    ├── standalone.py
    ├── requirements.txt
    └── .env                     # 环境变量（示例）
```

---

## 🛠 技术栈

| 层 | 技术 |
|----|------|
| **桌面壳** | Tauri 2.x (Rust) |
| **前端** | Next.js 16 + React 19 + TypeScript + Tailwind CSS 4 |
| **后端** | Python 3.10+ / FastAPI + SQLAlchemy 2.0 + SQLite |
| **AI** | OpenAI 兼容 API（流式 SSE） |

---

## 🔒 安全

- API 密钥存储在用户目录的 `config.json`，不会被提交到 git
- 前端设置的密码框字段（API Key）使用 `type="password"` 掩码显示
- 运行时诊断面板在正式版中已移除，不会暴露内部路径
- `.env` 已加入 `.gitignore`

---

## 📄 License

MIT
