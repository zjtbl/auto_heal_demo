# Auto-Heal: AI 驱动的前端自动化测试系统

> **项目定位**：基于 LangGraph + deepagents 框架构建的 AI 驱动多智能体测试自动化系统，支持探索性 QA 测试和组件感知测试生成双模式，通过 Skills 驱动的自愈机制实现可持续的 UI 自动化测试。

---

## 📋 目录

- [1. 项目背景与核心理念](#1-项目背景与核心理念)
- [2. 系统架构](#2-系统架构)
- [3. Skills 驱动模式详解](#3-skills-驱动模式详解)
- [4. 元素参考 MCP 服务](#4-元素参考-mcp-服务)
- [5. Auto-Heal 自愈机制](#5-auto-heal-自愈机制)
- [6. 开发路线图](#6-开发路线图)
- [7. 快速开始](#7-快速开始)

---

## 1. 项目背景与核心理念

### 1.1 项目概览

`ai-test-agent-system` 是一个企业级的 **AI 驱动的多智能体测试自动化系统**，旨在通过 LLM 理解测试意图、自动选择测试策略、生成结构化报告，解决传统 UI 自动化测试的痛点：

- **定位器脆弱性**：UI 变更导致测试频繁失败
- **覆盖率不足**：难以覆盖所有状态组合（Feature Flag、权限等）
- **维护成本高**：需要大量人工维护和修复
- **知识分散**：测试逻辑与业务逻辑分离，难以同步

### 1.2 核心理念

#### 理念一：代码 + Skills 混合设计

```
代码层（Python）          Skills 层（Markdown）
├── 决策层               ├── 执行流程定义
├── 路由逻辑             ├── 详细操作步骤
├── 工具注册             ├── 命令参考
├── 环境配置             ├── 最佳实践
└── 数据管理             └── 模板与规范
```

- **代码负责"做什么"**：路由判断、环境检查、目录创建、工具注册
- **Skills 负责"怎么做"**：具体的测试流程、命令参数、操作步骤
- **优势**：修改测试流程只需改 Skills 文件，无需改代码

#### 理念二：双模式架构

| 模式 | 适用场景 | 核心能力 | 输出 |
|------|----------|----------|------|
| **Mode A: 探索性 QA** | 只有 URL，无源码 | 6 阶段系统化探索、证据收集 | Bug 报告、截图、Trace、视频 |
| **Mode B: 组件感知** | 有源代码仓库 | 7-Agent 流水线静态分析 | POM、测试脚本、组件注册表 |

#### 理念三：上游优先（Upstream over Runtime）

传统 AI 测试停留在 "DOM 抓取" 阶段 —— 从渲染后的 HTML 反向推断意图，这存在根本性盲点：

- **无业务上下文**：浏览器只能看到"渲染了什么"，看不到"为什么存在"
- **状态覆盖不全**：只能看到当前渲染状态，无法覆盖 Feature Flag 和权限的所有组合
- **定位器契约断裂**：生成的定位器与源码无关，UI 变更即失效

**我们的做法**：将理解从运行时**上游化**到源码层面，通过组件感知的静态分析实现确定性自动化。

#### 理念四：自愈能力（Auto-Heal）

当元素变更时，系统应能自动检测并更新，而非依赖人工修复：

1. **扫描源码**：自动识别组件结构和可交互元素
2. **注入标识符**：为缺少稳定定位符的元素注入 `data-testid`
3. **更新定位器**：根据源码变更自动更新定位器目录
4. **修复测试**：自动更新受影响的测试脚本

---

## 2. 系统架构

### 2.1 整体架构图

```
用户请求
    │
    ├─→ [detect_test_mode] 代码层：判断走 Mode A 还是 Mode B
    │
    ├─→ Mode A (探索性 QA)
    │       ├─→ 加载 agent-browser-vs-playwright-cli skill (框架选型)
    │       ├─→ 加载 pw-dogfood skill (6 阶段测试流程)
    │       └─→ 输出: report.md + 证据文件
    │
    └─→ Mode B (组件感知)
            ├─→ 加载 component-aware-web-automation skill
            ├─→ 7-Agent 流水线：
            │       ├─ Agent 1: Script Analyst (剧本分析师) → component-registry.json
            │       ├─ Agent 2: Stage Manager (舞台经理) → testid-injections.json
            │       ├─ Agent 3: Blocking Coach (阻塞教练) → locator-catalog.json
            │       ├─ Agent 4: Set Designer (布景师) → poms/*.ts
            │       ├─ Agent 5: Choreographer (编舞师) → journeys.json
            │       ├─ Agent 6: Assistant Director (助理导演) → tests/*.spec.ts
            │       └─ Agent 7: Continuity Lead (连续性负责人) → execution-report.json
            └─→ 输出: Playwright 测试套件 + POM
```

### 2.2 代码层 vs Skills 层职责划分

| 层级 | 职责 | 文件 |
|------|------|------|
| **代码层** | 路由决策、工具注册、环境管理 | `src/app/agents/web/agent.py`<br>`src/app/agents/web/tools.py` |
| **Skills 层** | 测试流程定义、详细操作步骤、命令参考 | `src/workspace/web/skills/` |

#### 代码层职责（`agent.py` + `tools.py`）

1. **模式路由**：`detect_test_mode()` - 解析用户输入，返回 Mode A / Mode B / 询问
2. **环境检查**：`check_environment()` - 验证 `playwright-cli` 和 `agent-browser` 可用性
3. **目录管理**：`ensure_output_dir()` - 创建带时间戳的输出目录结构
4. **工具注册**：将上述 3 个工具注册到 Agent
5. **系统提示词**：`SYSTEM_PROMPT` - 用自然语言告诉 LLM 何时加载哪个 Skill

#### Skills 层职责（`src/workspace/web/skills/`）

| Skill 文件 | 作用 |
|------------|------|
| `pw-dogfood/SKILL.md` | Mode A 的 6 阶段测试流程（探索、交互、证据收集、高级测试、分类、报告） |
| `component-aware-web-automation/SKILL.md` | Mode B 的 7-Agent 流水线（静态分析、定位器生成、POM、测试生成） |
| `agent-browser-vs-playwright-cli/SKILL.md` | 框架选型决策指南 |
| `playwright-cli/SKILL.md` | Playwright CLI 命令参考 |
| `agent-browser/SKILL.md` | Agent Browser 使用参考 |

### 2.3 项目目录结构

```
ai-test-agent-system/
├── .env                              # DeepSeek API 密钥配置
├── graph.json                        # LangGraph API 图谱注册
├── pyproject.toml                    # 依赖管理
├── start_server.py                   # LangGraph API Server 启动入口
├── uv.lock                           # 锁定依赖版本
│
├── src/
│   ├── app/
│   │   ├── core/                     # 核心配置
│   │   ├── agents/                   # 智能体目录
│   │   │   ├── api/                  # API 测试智能体
│   │   │   ├── web/                  # ⭐ Web UI 自动化测试智能体
│   │   │   └── testcase/             # 测试用例生成智能体
│   │   ├── middleware/               # Agent 中间件
│   │   ├── processors/               # 处理器
│   │   └── mcp/                      # MCP 服务器
│   │       └── rag_server.py         # RAG MCP Server
│   │
│   └── workspace/                    # Agent 工作空间
│       ├── web/                      # Web Agent 工作区
│       │   ├── skills/               # Skills 文件目录
│       │   │   ├── pw-dogfood/
│       │   │   ├── component-aware-web-automation/
│       │   │   ├── agent-browser-vs-playwright-cli/
│       │   │   ├── playwright-cli/
│       │   │   └── agent-browser/
│       │   └── ARTIFACT_CONTRACT.md # 产物契约规范
│       │
│       └── web-output/               # 测试输出目录
│           ├── qa/                   # Mode A 输出
│           └── tests/                # Mode B 输出
│
└── testing-deep-agents-ui/           # 前端 UI（Next.js）
```

---

## 3. Skills 驱动模式详解

### 3.1 什么是 Skills？

**Skills** 是存储在文件中的 **Markdown 格式指令文档**，定义了详细的执行步骤。Agent 通过 `read_file` 加载 skill 内容，按指引执行。

这是一种**将知识外化到文件中**的设计模式，使 Agent 行为可通过修改 Skill 文件来调整，无需改代码。

### 3.2 Skills 的加载和调用方式

```python
# agent.py
from deepagents.middleware import SkillsMiddleware

# 1. 创建 Skills 中间件
skills_middleware = SkillsMiddleware(
    backend=file_backend,
    sources=["/web/skills/"],
)

# 2. 注册到 Agent
agent = create_agent(
    model=llm,
    tools=[...],
    backend=composite_backend,
    middleware=[skills_middleware],
    system_prompt=SYSTEM_PROMPT,
)
```

Agent 在执行时，通过 `read_file` 工具加载对应的 Skill 文件。

### 3.3 现有 Skills 文件详解

#### Skill 1: pw-dogfood（探索性 QA 测试）

**路径**：`src/workspace/web/skills/pw-dogfood/SKILL.md`

**职责**：指导 Agent 系统化地执行 QA 测试，利用 `playwright-cli` 的高级能力

**6 阶段流程**：

1. **Phase 1: Plan & Setup** - 创建输出目录、构建测试计划、启动浏览器
2. **Phase 2: Systematic Exploration** - 导航页面、测试交互元素、探测边缘情况
3. **Phase 3: Evidence Collection** - 截图、Trace、控制台、网络、视频证据
4. **Phase 4: Advanced Testing** - 性能、安全、可访问性、响应式、多角色测试
5. **Phase 5: Categorize & Prioritize** - 审查问题、去重、分类
6. **Phase 6: Report** - 生成结构化报告

#### Skill 2: component-aware-web-automation（组件感知测试生成）

**路径**：`src/workspace/web/skills/component-aware-web-automation/SKILL.md`

**职责**：通过源码静态分析，生成确定性的 Playwright 测试

**7-Agent 流水线**：

**Phase 1: Setup the Stage**（静态分析）
1. Script Analyst - 构建组件注册表
2. Stage Manager - 注入 data-testid
3. Blocking Coach - 生成定位器优先级链
4. Set Designer - 生成 POM 类

**Phase 2: Run the Show**（生成与执行）
5. Choreographer - 规划用户旅程
6. Assistant Director - 生成测试代码
7. Continuity Lead - 执行并分类失败

### 3.4 Skills 的优势

| 优势 | 说明 |
|------|------|
| **可维护性** | 修改测试流程只需改 Skill 文件 |
| **可读性** | Markdown 格式，人类可读 |
| **版本控制** | 可纳入 Git，变更可追踪 |
| **模块化** | 每个 Skill 独立，可复用 |
| **可扩展性** | 新增能力只需添加新 Skill |

---

## 4. 元素参考 MCP 服务

### 4.1 设计动机

当前 Mode B 的 Agent 1（Script Analyst）是通过 **Skill 文件的人工指令**来分析源码的。这种方式有以下局限：

1. **非标准化**：其他 AI Agent 无法直接使用
2. **执行成本高**：每次都需要 LLM 读取解析 Skill
3. **难以集成**：需要手动触发
4. **无缓存机制**：重复分析浪费资源

**解决方案**：将源码分析能力封装为 **标准化的 MCP 服务**，任何兼容的 AI Agent 都可以通过工具调用获取元素参考信息。

### 4.2 服务职责

元素参考 MCP 服务提供以下能力：

1. **扫描前端代码**：分析组件结构、可交互元素、定位器
2. **增量更新**：监听代码变更，自动更新元素参考
3. **提供查询接口**：AI Agent 查询特定元素的定位信息
4. **生成定位器**：为缺少稳定定位符的元素生成 `data-testid` 建议
5. **变更检测**：检测元素变更，触发自愈流程

### 4.3 MCP 工具定义

#### 工具 1: scan_repository
扫描整个前端代码库，提取组件和元素信息

#### 工具 2: query_element
查询特定组件的元素定位信息

#### 工具 3: suggest_testid_injections
为缺少稳定定位符的元素生成 data-testid 注入建议

#### 工具 4: detect_changes
检测代码库变更，识别受影响的组件和元素

#### 工具 5: update_references
更新元素参考（组件注册表、定位器目录等）

### 4.4 与现有架构的整合方式

#### 整合点 1：增强 Mode B 的 Agent 1

**之前**：Agent 1 读取 Skill 文件，根据指令手动分析源码

**之后**：Agent 1 调用 MCP 工具 `scan_repository()`，直接获取结构化的组件注册表

#### 整合点 2：自动化变更检测

通过 Git Hook 或 Webhook 触发 `detect_changes()`，自动识别受影响的组件和元素

#### 整合点 3：AI Agent 的工具注册

在 `agent.py` 中注册 MCP 工具，让 AI Agent 可以直接调用

### 4.5 服务实现建议

**技术栈**：
- **框架**：FastMCP
- **语言**：Python 3.10+
- **静态分析**：AST + 框架编译器
- **存储**：JSON 文件或 SQLite
- **Git 集成**：gitpython

---

## 5. Auto-Heal 自愈机制

### 5.1 核心概念

**Auto-Heal（自愈）** 是指当 UI 自动化测试因元素定位失败时，系统能够自动检测、定位问题并修复，而无需人工介入。

### 5.2 失败分类

| 失败类型 | 描述 | 处理方式 |
|---------|------|---------|
| **代码 Bug** | 应用真的坏了 | 标记为 Bug，报告给开发 |
| **测试更新需求** | 源码有意变更 | 触发自愈流程 |
| **环境问题** | 网络错误、超时 | 重试或调整 |

### 5.3 自愈流程

```
测试失败
    │
    ├─→ [失败分类] Continuity Lead Agent
    ├─→ [检测变更] detect_changes()
    ├─→ [更新元素参考] update_references()
    ├─→ [生成测试补丁] Assistant Director Agent
    ├─→ [应用补丁] 可选（自动或人工审核）
    └─→ [重新执行测试]
```

### 5.4 自愈示例

**场景**：开发人员将 `LoginForm` 组件中的 `data-testid` 重命名

**步骤**：
1. 测试失败
2. 失败分类：测试更新需求
3. 检测变更：识别受影响的元素
4. 更新元素参考：重新扫描组件
5. 生成测试补丁：更新 POM 和测试脚本
6. 应用补丁并重新测试

---

## 6. 开发路线图

### 6.1 近期目标（1-2 个月）

- [ ] 实现 Element Reference MCP Server 基础框架
- [ ] 实现 React 组件扫描器
- [ ] 实现核心 MCP 工具
- [ ] 整合到 Mode B 流程

### 6.2 中期目标（3-6 个月）

- [ ] 实现其他框架扫描器（Vue、Angular、Svelte）
- [ ] 实现高级 MCP 工具
- [ ] 实现自愈机制
- [ ] Git 集成
- [ ] UI 增强

### 6.3 远期目标（6-12 个月）

- [ ] 智能定位器生成
- [ ] 测试覆盖率分析
- [ ] 预测性维护
- [ ] 多仓库支持
- [ ] 企业级功能

---

## 7. 快速开始

### 7.1 环境准备

**系统要求**：
- Python 3.10+
- Node.js 18+
- Git

### 7.2 配置环境变量

创建 `.env` 文件：

```bash
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com
WORKSPACE_DIR=/path/to/workspace
OUTPUT_ROOT=/path/to/output
```

### 7.3 启动服务

```bash
# 启动 LangGraph API Server
python start_server.py

# 启动 RAG MCP Server
python src/app/mcp/rag_server.py --transport=sse --port=8008

# 启动前端 UI
cd testing-deep-agents-ui
npm run dev
```

### 7.4 运行测试

**Mode A: 探索性 QA 测试**

```bash
curl -X POST http://localhost:8000/api/web/agent \
  -H "Content-Type: application/json" \
  -d '{"user_request": "请测试 https://example.com 的登录功能"}'
```

**Mode B: 组件感知测试生成**

```bash
curl -X POST http://localhost:8000/api/web/agent \
  -H "Content-Type: application/json" \
  -d '{"user_request": "请为项目 /path/to/frontend-repo 生成 Playwright 测试"}'
```

---

## 8. 常见问题

### Q1: 为什么使用 Skills 而不是硬编码？

**A**: Skills 提供了灵活性和可维护性：
- 修改测试流程只需改 Skill 文件，无需改代码
- Markdown 格式，人类可读可编辑
- 可以通过版本控制追踪变更
- 新增测试能力只需添加新 Skill

### Q2: MCP 服务和 Skill 有什么区别？

**A**: MCP 服务提供标准化的工具接口，服务端直接执行，性能更高，适合数据查询和计算密集型任务。Skill 用于流程定义和操作指南。

### Q3: 自愈机制会自动应用补丁吗？

**A**: 默认为半自动模式：系统生成补丁，人工审核后选择应用或拒绝。可配置为全自动模式（高风险）。

### Q4: 支持哪些前端框架？

**A**: 已支持 React（.tsx/.jsx），计划中：Vue、Angular、Svelte。

---

## 9. 参考资料

### 9.1 项目文档

- [项目 README](readme.md)
- [Web Agent 详解](src/read.md)
- [Artifact 契约规范](src/workspace/web/ARTIFACT_CONTRACT.md)

### 9.2 外部资源

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [deepagents 文档](https://github.com/deepagents/deepagents)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Playwright 官方文档](https://playwright.dev/)

---

**文档版本**: v1.0.0
**最后更新**: 2025-01-10
**维护者**: AI Test Agent System Team