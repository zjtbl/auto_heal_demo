## 📁 项目结构总结

`ai-test-agent-system` 是一个基于 **LangGraph + deepagents** 框架构建的 **AI 驱动的多智能体测试自动化系统**。整体架构如下：

```
ai-test-agent-system/
├── .env                          # DeepSeek API 密钥配置
├── graph.json                    # LangGraph API 图谱注册（仅注册了 chat_agent → api/agent.py）
├── pyproject.toml                # 依赖管理（playwright, langchain, deepagents 等）
├── start_server.py               # LangGraph API Server 启动入口
├── uv.lock                       # 锁定依赖版本
├── src/
│   └── app/
│       ├── core/                 # 核心配置
│       │   ├── config.py         # 全局配置（LLM API Key, 模型选择等）
│       │   └── llms.py           # LLM 模型工厂（DeepSeek + 豆包多模态）
│       ├── agents/               # 🎯 **智能体（Agent）目录 — 核心业务**
│       │   ├── api/              #   MASTEST - RESTful API 测试智能体
│       │   ├── web/              #   **⭐ Web UI 自动化测试智能体（你的重点）**
│       │   └── testcase/         #   测试用例生成智能体（含 RAG 知识检索）
│       ├── middleware/            # Agent 中间件
│       │   ├── pdf_context.py    # PDF 上下文注入中间件
│       │   └── rag_context.py    # RAG 检索上下文中间件
│       ├── processors/
│       │   └── pdf.py            # PDF 文档解析处理器
│       └── mcp/
│           └── rag_server.py     # RAG MCP Server（知识库检索）
```

---

## 🎯 做 UI 自动化测试应重点关注哪个目录？

**答案：`src/app/agents/web/` 目录**

这是整个项目中**唯一专门处理 UI 自动化测试**的智能体。具体包含：

| 文件 | 作用 |
|------|------|
| `agent.py` | Web 自动化测试 Agent 定义（核心入口） |
| `tools.py` | 自定义工具 + 后端配置 |
| `validate_agent.py` | Agent 的冒烟测试脚本 |

另外，依赖的 **Skills 技能目录**（位于 `src/workspace/web/skills/`）也至关重要，包含：
- `pw-dogfood/` — Playwright 端到端测试执行技能
- `component-aware-web-automation/` — 组件感知的自动化测试生成技能
- `agent-browser-vs-playwright-cli/` — 浏览器框架选型技能
- `playwright-cli/` — Playwright CLI 使用参考
- `agent-browser/` — Agent Browser 使用参考

---

## 🔍 详解：当前项目如何实现 UI 自动化测试

### 一、整体架构：**双模式（Dual-Mode）架构**

`agent.py` 的第 1-89 行定义了一个 **Web 自动化测试 Agent**，采用双模式架构：

```
用户输入
    │
    ├── 只有 URL（无代码仓库路径）
    │   └── 🅰️ Mode A: 探索性 QA 测试
    │
    ├── 有代码仓库路径（含 URL 或仅路径）
    │   └── 🅱️ Mode B: 组件感知测试生成
    │
    └── 都没有
        └── 询问用户澄清
```

### 二、Mode A：探索性 QA 测试（Exploratory QA）

**适用场景**：只知道被测网站的 URL，没有源码。

**工作流程**（6 个阶段）：
1. **框架选型** → 加载 `agent-browser-vs-playwright-cli` skill，决定用 Playwright 还是 Agent Browser
2. **执行测试** → 加载 `pw-dogfood` skill，按 6 阶段工作流执行：
   - 打开网页 → 截图 → 点击交互 → 填写表单 → 验证结果 → 记录缺陷
3. **CLI 参考** → 需要时加载 `playwright-cli` 或 `agent-browser` skill 获取具体命令
4. **保存证据** → 所有截图、trace、视频保存到 `{output_root}/qa/{timestamp}/` 目录
5. **生成报告** → 输出 `report.md` 测试报告

**关键工具链**：
- `detect_test_mode(user_request)` → 自动判断走 Mode A 还是 Mode B
- `check_environment()` → 验证 `playwright-cli` 和 `agent-browser` 是否可用
- `ensure_output_dir(mode, label)` → 创建带时间戳的输出目录

### 三、Mode B：组件感知测试生成（Component-Aware）

**适用场景**：有前端项目的源代码仓库路径，需要生成可维护的 Playwright 测试脚本。

**工作流程**（7 个 Agent 流水线）：
```
Script Analyst (脚本分析师)
    → Stage Manager (舞台经理)
    → Blocking Coach (阻塞教练)
    → Set Designer (布景设计师)
    → Choreographer (编舞师)
    → Assistant Director (助理导演)
    → Continuity Lead (连续性负责人)
```

每个 Agent 的输出通过 workspace 文件系统传递，生成以下交付物：
- `component-registry.json` — 组件注册表
- `locator-catalog.json` — 定位器目录
- `poms/*.ts` — Page Object Model 文件
- `tests/*.spec.ts` — Playwright 测试脚本

### 四、技术实现细节

#### 1. **基于 `deepagents` 框架**
使用 `create_deep_agent()` 创建 Agent，这是一种基于 LangGraph 的高级 Agent 框架，支持：
- **SkillsMiddleware** — 加载外部技能文件（Markdown 格式的指令文档）
- **CompositeBackend** — 组合本地 Shell 执行 + 文件系统操作
- **自定义工具** — 通过 `@tool` 装饰器注册

```python
agent = create_agent(
    model=llm,                              # DeepSeek Chat 模型
    tools=[detect_test_mode, check_environment, ensure_output_dir],
    backend=composite_backend,              # Shell + 文件系统组合后端
    middleware=[skills_middleware],          # 技能中间件
    system_prompt=SYSTEM_PROMPT,            # 系统提示词
)
```

#### 2. **技能（Skills）驱动**
Skills 是存储在文件中的 Markdown 文档，定义了详细的执行步骤。Agent 通过 `read_file` 加载 skill 内容，按指引执行。这是一种**将知识外化到文件中**的设计模式，使 Agent 行为可通过修改 Skill 文件来调整，无需改代码。

#### 3. **浏览器操控方式**
项目依赖 Playwright（`playwright>=1.58.0`），通过两种方式操控浏览器：
- **Playwright CLI** — 通过命令行 `npx playwright test` 执行测试
- **Agent Browser** — 另一种浏览器自动化框架（备选）

#### 4. **后端执行环境**
```python
shell_backend = LocalShellBackend(
    root_dir=workspace_dir,
    virtual_mode=False,          # 真实执行模式
    timeout=180,                 # 3 分钟超时
)
file_backend = FilesystemBackend(
    root_dir=workspace_dir,
    virtual_mode=True,           # 虚拟模式（不实际写磁盘）
)
composite_backend = CompositeBackend(
    default=shell_backend,       # 默认走 Shell
    routes={"/": file_backend},  # 文件操作走文件后端
)
```

### 五、项目中其他与 UI 自动化间接相关的部分

| 模块 | 关系 |
|------|------|
| **`agents/testcase/`** | 测试用例生成 Agent，可生成用例但不执行 UI 操作 |
| **`agents/api/hermes_agent.py`** | 实验性的 Hermes Agent（暂未启用） |
| **`mcp/rag_server.py`** | RAG 知识库，可为测试用例生成提供历史知识 |
| **`processors/pdf.py`** | PDF 解析，用于从需求文档提取信息生成测试用例 |

### 六、总结

要实现 UI 自动化测试，应主要关注 **`src/app/agents/web/`** 目录。当前项目的 UI 自动化测试方案本质上是：

> **一个由 LLM（DeepSeek）驱动的智能 Agent，通过加载预定义的技能文档（Skills），利用 Playwright CLI 执行浏览器操作，支持探索性测试和代码仓库级组件测试两种模式。**

这套方案的优势在于通过 AI 理解测试意图、自动选择测试策略、生成结构化报告，但实际执行的底层仍然是 Playwright 浏览器自动化技术。