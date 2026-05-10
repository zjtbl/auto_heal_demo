# 当前项目代码扫描触发机制详解

> **分析项目**: `ai-test-agent-system`  
> **分析时间**: 2026-05-11  
> **核心问题**: 代码扫描是如何被触发的？是谁触发的代码扫描并建立元素库？

---

## 一、整体触发链路

```
用户请求 (HTTP API / Studio UI)
    │
    ▼
LangGraph API Server (start_server.py, 端口 2026)
    │
    ▼
graph.json 注册的 Agent Graph（当前仅注册了 chat_agent）
    │
    ▼
Web Agent 的 SYSTEM_PROMPT 指引 LLM 做模式选择
    │
    ▼
detect_test_mode() 工具 —— 路由决策
    │
    ├─ 返回 "MODE_B_COMPONENT" → 加载 component-aware-web-automation 技能 → 执行 7-Agent 流水线扫描
    ├─ 返回 "MODE_A_QA"       → 加载 pw-dogfood 技能 → 探索性测试
    └─ 返回 "ASK_CLARIFICATION" → 询问用户
```

---

## 二、核心触发机制：`detect_test_mode()` 工具

这是 **路由决策的关键**，位于 `tools.py` 第 34-71 行：

```python
def detect_test_mode(user_request: str) -> str:
```

它的工作原理是 **正则匹配用户输入文本**：

| 匹配条件 | 返回值 | 走哪条路 |
|----------|--------|----------|
| 输入含 repo 路径标记（`C:\`、`/home/`、`src/`、`source code`、`repo`、`.git` 等）且无 URL | `MODE_B_COMPONENT` | 组件感知扫描 |
| 输入含 URL 且无 repo 路径 | `MODE_A_QA` | 探索性测试 |
| 同时含 URL 和 repo 路径 | `MODE_B_COMPONENT` | **组件感知扫描优先** |
| 都不含 | `ASK_CLARIFICATION` | 询问用户 |

**举例**：
- 用户输入：`"帮我测试 F:\codex-work\testd-data-sys\frontend-app 这个项目"` → 匹配 `C:\` 路径 → `MODE_B_COMPONENT` → 触发代码扫描
- 用户输入：`"测试 https://example.com 这个网站"` → 匹配 URL → `MODE_A_QA` → 探索性测试
- 用户输入：`"帮我测试"` → 都不匹配 → `ASK_CLARIFICATION`

---

## 三、扫描的执行者：LLM Agent 本身（不是脚本！）

这是最关键的理解：**代码扫描不是由某个独立脚本或服务执行的，而是由 LLM Agent 本身完成的**。

具体流程：

1. **LLM 调用 `detect_test_mode()`** → 确认走 Mode B
2. **LLM 读取 Skill 文件** → 通过 `SkillsMiddleware` 加载 `component-aware-web-automation/SKILL.md`
3. **LLM 按 Skill 指引逐步执行** → 使用 Agent 内置工具：
   - `glob` / `grep` → 扫描项目文件结构、发现组件
   - `read_file` → 读取组件源代码
   - `write_file` → 生成 `component-registry.json`、`locator-catalog.json` 等
   - `execute` → 运行 shell 命令（如 `npx playwright test`）
4. **Agent 通过 workspace 文件系统传递产物** → 前一个 Agent 的输出文件是下一个 Agent 的输入

---

## 四、SkillsMiddleware 的作用

```python
skills_middleware = SkillsMiddleware(
    backend=file_backend,
    sources=["/web/skills/"],
)
```

- 它将 `src/workspace/web/skills/` 目录下的 Markdown 文件注册为"技能"
- 当 LLM 需要某个技能时，它通过 `read_file` 加载对应的 SKILL.md
- SKILL.md 本质上是 **给 LLM 看的详细操作手册**，告诉 LLM 应该怎么一步步做
- **LLM 是"读着说明书干活的工人"**，技能文件就是"说明书"

---

## 五、后端执行环境

```python
shell_backend = LocalShellBackend(root_dir=workspace_dir, virtual_mode=False, timeout=180)
file_backend = FilesystemBackend(root_dir=workspace_dir, virtual_mode=True)
composite_backend = CompositeBackend(default=shell_backend, routes={"/": file_backend})
```

- **Shell 后端**：真实执行 shell 命令（如 `npx playwright test`、`grep`、`find`）
- **文件后端**：虚拟模式，Agent 的 `write_file`/`read_file` 操作在 workspace 目录下进行
- Agent 产出的 `component-registry.json` 等文件写入 workspace 文件系统

---

## 六、⚠️ 一个重要问题：Web Agent 尚未注册！

当前 `graph.json` 只注册了 `chat_agent`（指向 `api/agent.py`），**Web Agent 并未注册**。这意味着：

- 启动 `start_server.py` 后，通过 LangGraph API 无法直接访问 Web Agent
- 如果要实际触发 Mode B 扫描，需要：
  1. 在 `graph.json` 中注册 Web Agent，或
  2. 通过代码直接调用 `agent` 对象（如 `agent.invoke({"messages": [...]})`)

---

## 七、完整调用链路图

```
┌──────────────────────────────────────────────────────────────────┐
│                        用户发送请求                               │
│  "帮我测试 F:\codex-work\testd-data-sys\frontend-app 这个项目"    │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              LangGraph API Server (端口 2026)                     │
│              start_server.py → uvicorn → langgraph_api           │
│              读取 graph.json 获取 Agent 定义                      │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              Web Agent (agent.py)                                 │
│              LLM = DeepSeek Chat                                  │
│              SYSTEM_PROMPT 指引：判断 Mode A 还是 Mode B          │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              detect_test_mode("帮我测试 F:\...frontend-app")       │
│              正则匹配到 "F:\" → 返回 "MODE_B_COMPONENT"           │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              LLM 决定加载 Skill 文件                               │
│              SkillsMiddleware → read_file                         │
│              加载 component-aware-web-automation/SKILL.md         │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              LLM 按照 SKILL.md 指引逐步执行 7-Agent 流水线        │
│                                                                   │
│  Phase 1:                                                         │
│    Agent 1 Script Analyst   → glob/grep/read_file 扫描源代码      │
│                               → write_file 生成 registry.json     │
│    Agent 2 Stage Manager    → read_file 读取 registry             │
│                               → write_file 生成 injections.json   │
│    Agent 3 Blocking Coach   → read_file 读取 registry+injections  │
│                               → write_file 生成 locator-catalog   │
│    Agent 4 Set Designer     → read_file 读取 catalog              │
│                               → write_file 生成 poms/*.ts         │
│                                                                   │
│  Phase 2:                                                         │
│    Agent 5 Choreographer    → read_file 读取 POM + catalog        │
│                               → write_file 生成 journeys.json     │
│    Agent 6 Assistant Director → read_file 读取 journeys + POMs    │
│                               → write_file 生成 tests/*.spec.ts   │
│    Agent 7 Continuity Lead  → execute 运行 npx playwright test    │
│                               → write_file 生成 execution-report  │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              产物输出到 workspace 文件系统                          │
│              output_root/tests/{project_name}_{timestamp}/        │
│              ├── component-registry.json                          │
│              ├── testid-injections.json                           │
│              ├── locator-catalog.json                             │
│              ├── journeys.json                                    │
│              ├── poms/                                            │
│              │   ├── AppLayout.ts                                 │
│              │   ├── AgentMarketPage.ts                           │
│              │   └── ...                                          │
│              ├── tests/                                           │
│              │   ├── Market-browse.spec.ts                        │
│              │   └── ...                                          │
│              └── execution-report.json                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 八、总结：谁触发了代码扫描？

| 层级 | 角色 | 动作 |
|------|------|------|
| **用户** | 触发源 | 发送包含项目路径的请求 |
| **LangGraph API** | 入口 | 接收请求，路由到 Agent |
| **SYSTEM_PROMPT** | 调度器 | 指引 LLM 判断走 Mode A 还是 B |
| **`detect_test_mode()`** | 路由器 | 正则匹配确认走 Mode B |
| **LLM (DeepSeek)** | 执行者 | 按照 Skill 指引，用内置工具扫描代码、生成元素库 |
| **SkillsMiddleware** | 知识库 | 提供 SKILL.md"说明书" |
| **CompositeBackend** | 执行环境 | Shell 执行命令 + 文件系统读写 |

**核心结论**：代码扫描是由 **LLM Agent 自主驱动**的——它根据用户输入判断需要扫描，然后按照技能文件的指引，利用 `grep`/`glob`/`read_file` 等内置工具逐步分析源代码，最终生成组件注册表、定位器目录、POM 类等产物。没有一个独立的"扫描脚本"在运行，扫描逻辑完全由 **LLM + Skill 文件 + 内置工具** 三者协作完成。

---

**文档版本**: v1.0.0  
**分析时间**: 2026-05-11