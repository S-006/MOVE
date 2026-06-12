明白了，你需要的是一个 **给 GitHub Copilot 的“Skill”定义**——也就是一段结构化的指令，让 Copilot 能自动为你的 Python AI Agent 生成完整的 Web 模块，包括美观的界面和测试代码，而不是手把手让你自己写。

下面就是可以直接发给 Copilot（或作为 `.github/copilot-instructions.md` 或对话提示）的 **Skill**。

---

## Skill 名称: `add_web_interface_to_python_agent`

### 目标
为现有的 Python AI Agent 工具增加一个 HTTP Web 服务模块，用户通过**美观的网页界面**输入问题，Agent 自动处理并返回结果。同时生成对应的**单元测试**，确保模块正常工作。

### 当前项目状态
- 有一个 Python 文件（具体路径请 Copilot 自行推断或询问用户），其中包含一个可以通过命令行运行的 AI Agent。
- Agent 的核心函数假设为 `run_agent(user_input: str) -> str`（如果实际函数名不同，请自动适配或要求用户确认）。

### 要求

#### 1. Web 框架
- 使用 **FastAPI**（轻量、高性能、自动生成 API 文档）。
- 使用 **Uvicorn** 作为服务器。

#### 2. 功能端点
- `GET /`：返回一个美观的 HTML 页面（见下方界面要求）。
- `POST /chat`：接收 JSON `{"question": "用户问题"}`，调用 `run_agent`，返回 `{"answer": "agent回答"}`。
- 添加一个简单的健康检查端点 `GET /health`，返回 `{"status": "ok"}`。

#### 3. 前端界面要求（美观）
- 使用 **Tailwind CSS**（通过 CDN）或 **Bootstrap 5**（选择更现代的一种）。
- 页面包含：
  - 标题：AI Agent 对话界面。
  - 一个大的文本框（`<textarea>`）供用户输入问题。
  - 一个发送按钮，加载时显示“思考中…”的 loading 状态。
  - 一个用于展示回答的区域，支持 Markdown 风格的简单渲染（例如换行、加粗等，可选）。
  - 响应式设计，在手机和桌面都好看。
  - 深色/浅色模式可选（但非强制，如果简单实现则用浅色 + 半透明卡片效果）。
- 通过 Fetch API 调用 `/chat` 端点，处理错误（如网络错误、服务器错误）。

#### 4. 与现有 Agent 的集成
- 假设 `run_agent` 位于某个模块，你需要自动找到该函数或让用户指定。
- 生成的新文件命名为 `web_service.py`，放在项目根目录。
- 在 `web_service.py` 中导入 `run_agent`（如果导入路径不确定，使用动态导入或让用户调整）。

#### 5. 测试
- 使用 **pytest** 和 **httpx**（或 FastAPI 的 `TestClient`）编写测试文件 `test_web_service.py`。
- 测试覆盖：
  - 根路径返回 200 且包含预期的 HTML 元素（如标题、textarea）。
  - `/chat` 正常返回 JSON 且调用 `run_agent` 返回正确回答。
  - `/chat` 参数缺失时返回 400。
  - `/health` 返回 200。
  - 可以 mock `run_agent` 以避免依赖真实 Agent 逻辑。
- 提供运行测试的命令说明。

#### 6. 运行说明
- 在生成的代码顶部注释中说明如何启动服务：
  ```bash
  pip install fastapi uvicorn pytest httpx
  python web_service.py
  ```
- 也可以支持 `uvicorn web_service:app --reload` 的开发模式。

### 额外要求
- **不要**修改原有的 Agent 核心代码（除非必须暴露函数，但尽量只是导入）。
- 确保 CORS 未开放（本地开发可以不加，或添加必要的安全头）。
- 所有代码必须有清晰的注释，方便后续维护。

### 验收标准
1. 运行 `python web_service.py` 后，在浏览器打开 `http://localhost:8000` 能看到美观的聊天界面。
2. 输入问题，能正确显示 Agent 的回答。
3. 运行 `pytest test_web_service.py`，所有测试通过。
4. 代码风格符合 PEP 8，没有明显的冗余。

---

## 如何使用这个 Skill

将上面的完整内容复制粘贴到与 GitHub Copilot 的对话中，并说：

> “请根据上面的 Skill 定义，为我的 Python AI Agent 项目自动生成 web 模块、前端界面和测试代码。”

Copilot 将理解你的需求并生成相应的文件内容。如果它对现有 Agent 的入口函数不确定，会主动询问你。

如果你希望 Copilot **全自动** 完成（无需询问），可以在 Skill 开头添加：
> “假设 Agent 的核心函数名为 `run_agent`，位于 `agent.py` 文件中。”

这样 Copilot 就会直接生成代码。
