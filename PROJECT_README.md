# AI Test Agent System - 项目全景文档

> **项目定位**：基于 LangGraph + deepagents 框架构建的企业级 AI 驱动多智能体测试自动化系统，支持 Web UI、API、测试用例生成三大测试场景，通过 Skills 驱动的自愈机制实现可持续的测试自动化。

---

## 📋 目录

- [1. 项目概览](#1-项目概览)
- [2. 核心架构](#2-核心架构)
- [3. 三大智能体详解](#3-三大智能体详解)
  - [3.1 Web Agent - UI 自动化测试](#31-web-agent---ui-自动化测试)
  - [3.2 API Agent - RESTful API 测试](#32-api-agent---restful-api-测试)
  - [3.3 Testcase Agent - 测试用例生成](#33-testcase-agent---测试用例生成)
- [4. 核心技术组件](#4-核心技术组件)
- [5. Skills 驱动模式](#5-skills-驱动模式)
- [6. 项目结构](#6-项目结构)
- [7. 快速开始](#7-快速开始)
- [8. 开发指南](#8-开发指南)

---

## 1. 项目概览

### 1.1 项目目标

`ai-test-agent-system` 是一个企业级的 **AI 驱动多智能体测试自动化平台**，旨在通过 LLM 理解测试意图、自动选择测试策略、生成结构化测试资产，解决传统自动化测试的痛点：

- **定位器脆弱性**：UI 变更导致测试频繁失败 → **Auto-Heal 自愈机制**
- **覆盖率不足**：难以覆盖所有状态组合 → **组件感知 + Feature Flag 支持**
- **维护成本高**：需要大量人工维护 → **Skills 驱动，流程可配置**
- **知识分散**：测试逻辑与业务逻辑分离 → **RAG 知识库**

### 1.2 核心特性

| 特性 | 描述 |
|------|------|
| **三大智能体** | Web Agent（UI）、API Agent（API）、Testcase Agent（用例生成） |
| **双模式架构** | 探索性 QA（Mode A）+ 组件感知测试生成（Mode B） |
| **Skills 驱动** | 测试流程外化到 Markdown 文件，无需改代码即可调整 |
| **Auto-Heal** | 元素变更自动检测并修复测试 |
| **RAG 知识库** | 历史测试知识复用 |
| **多模态支持** | 支持图片、PDF、文档输入 |
| **前端 UI** - Next.js + React 提供可视化交互界面 |

---

## 2. 核心架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端 UI (Next.js)                       │
│              testing-deep-agents-ui/                            │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP/WebSocket
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph API Server                         │
│                      start_server.py                            │
└────┬────────────────┬────────────────┬────────────────────────┘
     │                │                │
     ↓                ↓                ↓
┌─────────┐    ┌──────────┐    ┌──────────────┐
│  Web    │    │   API    │    │  Testcase    │
│  Agent  │    │  Agent   │    │    Agent     │
│ (UI测试)│    │ (API测试) │    │  (用例生成)  │
└────┬────┘    └─────┬────┘    └──────┬───────┘
     │               │                │
     ↓               ↓                ↓
┌─────────┐    ┌──────────┐    ┌──────────────┐
│ Skills  │    │  Skills  │    │    Skills    │
│ 层      │    │   层     │    │     层       │
└────┬────┘    └─────┬────┘    └──────┬───────┘
     │               │                │
     ↓               ↓                ↓
┌─────────────────────────────────────────────────────┐
│              Workspace (工作空间)                    │
│  ├── web/skills/      (Web 测试技能)               │
│  ├── api/skills/      (API 测试技能)               │
│  ├── testcase/skills/ (用例生成技能)               │
│  └── rag/skills/      (RAG 检索技能)               │
└─────────────────────────────────────────────────────┘
```

### 2.2 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **LLM** | DeepSeek Chat + 豆包多模态 | 文本理解和图像识别 |
| **框架** | LangGraph + deepagents | Agent 编排和工具管理 |
| **前端** | Next.js 14 + React + Tailwind CSS | 用户界面 |
| **后端** | Python 3.10+ | Agent 和 MCP 服务 |
| **测试引擎** | Playwright | 浏览器自动化和 API 测试 |
| **知识库** | RAG (Retrieval-Augmented Generation) | 历史知识检索 |

---

## 3. 三大智能体详解

### 3.1 Web Agent - UI 自动化测试

**路径**: `src/app/agents/web/agent.py`

#### 核心能力

Web Agent 支持**两种互斥的工作模式**，根据用户输入自动选择：

| 模式 | 适用场景 | 核心能力 | 输出 |
|------|----------|----------|------|
| **Mode A: 探索性 QA** | 只有 URL，无源码 | 6 阶段系统化探索、证据收集 | Bug 报告、截图、Trace、视频 |
| **Mode B: 组件感知** | 有源代码仓库 | 7-Agent 流水线静态分析 | POM、测试脚本、组件注册表 |

#### Mode A: 探索性 QA 测试

**适用场景**: 只知道被测网站的 URL，没有源码。

**6 阶段工作流**:

1. **Phase 1: Plan & Setup** - 创建输出目录、构建测试计划、启动浏览器
2. **Phase 2: Systematic Exploration** - 导航页面、测试交互元素、探测边缘情况
3. **Phase 3: Evidence Collection** - 截图、Trace、控制台、网络、视频证据
4. **Phase 4: Advanced Testing** - 性能、安全、可访问性、响应式、多角色测试
5. **Phase 5: Categorize & Prioritize** - 审查问题、去重、分类
6. **Phase 6: Report** - 生成结构化报告

**输出目录结构**:
```
web-output/qa/{label}_{timestamp}/
├── screenshots/          # PNG 截图
├── traces/               # Playwright trace 文件
├── videos/               # WebM 屏幕录制
├── storage/              # 认证状态 JSON
└── report.md             # 最终结构化报告
```

#### Mode B: 组件感知测试生成

**适用场景**: 有前端项目的源代码仓库路径，需要生成可维护的 Playwright 测试脚本。

**7-Agent 流水线**:

**Phase 1: Setup the Stage**（静态分析）
1. **Script Analyst (剧本分析师)** - 扫描源码，构建组件注册表 (`component-registry.json`)
2. **Stage Manager (舞台经理)** - 注入 `data-testid` 标识符 (`testid-injections.json`)
3. **Blocking Coach (阻塞教练)** - 生成定位器优先级链 (`locator-catalog.json`)
4. **Set Designer (布景设计师)** - 生成 Page Object Model 类 (`poms/*.ts`)

**Phase 2: Run the Show**（生成与执行）
5. **Choreographer (编舞师)** - 规划用户旅程 (`journeys.json`)
6. **Assistant Director (助理导演)** - 生成测试代码 (`tests/*.spec.ts`)
7. **Continuity Lead (连续性负责人)** - 执行并分类失败 (`execution-report.json`)

**输出目录结构**:
```
web-output/tests/{project_name}_{timestamp}/
├── component-registry.json      # 组件注册表
├── testid-injections.json       # data-testid 注入目录
├── locator-catalog.json         # 定位器优先级链
├── poms/                        # Page Object Model
│   ├── LoginPage.ts
│   └── DashboardPage.ts
├── journeys.json                # 用户旅程规划
├── tests/                       # Playwright 测试脚本
│   ├── login/Login-standard.spec.ts
│   └── login/Login-lockedOut.spec.ts
└── execution-report.json        # 执行报告
```

#### 核心工具

| 工具 | 作用 | 实现 |
|------|------|------|
| `detect_test_mode` | 自动判断走 Mode A 还是 Mode B | 正则表达式匹配 URL 和路径 |
| `check_environment` | 验证 `playwright-cli` 和 `agent-browser` 可用性 | 子进程调用 |
| `ensure_output_dir` | 创建带时间戳的输出目录结构 | 文件系统操作 |

---

### 3.2 API Agent - RESTful API 测试

**路径**: `src/app/agents/api/agent.py`

#### 核心能力

API Agent 实现 **MASTEST 方法论**（arXiv:2511.18038），提供端到端的 RESTful API 测试自动化。

#### 工作流程

1. **Parse** - 解析 OpenAPI 规范，提取 API 端点信息
2. **Scenarios** - 生成单元场景（单端点）和系统场景（多端点序列）
3. **Scripts** - 生成 Playwright TypeScript 测试脚本
4. **Syntax** - 检查脚本语法正确性
5. **Execute** - 执行测试脚本
6. **Quality** - LLM 分析数据类型正确性、状态码覆盖率
7. **Report** - 生成质量报告

#### 核心原则

- **One operation at a time** - 逐个操作、逐个场景工作，避免 token 限制
- **Human in the loop** - 每个阶段完成后暂停等待人工审核
- **Source of truth** - 以 OpenAPI 规范为准，不猜测参数和类型

#### Skills 体系

| Skill | 作用 |
|-------|------|
| `test-scenario-design` | 单元和系统场景生成 |
| `playwright-api-testing` | Playwright TypeScript 脚本编写 |
| `api-test-quality` | 质量度量和缺陷检测 |

---

### 3.3 Testcase Agent - 测试用例生成

**路径**: `src/app/agents/testcase/agent.py`

#### 核心能力

Testcase Agent 是一位**企业级资深测试架构师**，将模糊需求转化为高质量、可执行、可量化的测试资产。

#### 核心工作铁律

**先 RAG，后分析；无检索，不设计**

1. **RAG 检索** - 首先激活 `rag-query` Skill，查询历史测试用例、业务规则、领域知识
2. **需求分析** - 激活 `requirement-analysis` Skill，生成需求解析报告
3. **测试策略** - 激活 `test-strategy` Skill，制定测试策略
4. **用例设计** - 激活 `test-case-design` + `test-data-generator` Skills
5. **质量评审** - 激活 `quality-review` Skill，四维度评分
6. **输出格式化** - 激活 `output-formatter` Skill，导出多种格式

#### 六大 Skills 体系

| Phase | Skill | 产出要求 |
|-------|-------|---------|
| Phase 1 | `requirement-analysis` | 需求解析报告（功能矩阵 + 风险清单 + 用例预估） |
| Phase 2 | `test-strategy` | 测试策略报告（类型选择 + 优先级 + 深度分配） |
| Phase 3 | `test-case-design` + `test-data-generator` | 逐模块测试用例 + 具体测试数据 |
| Phase 4 | `quality-review` | 质量评审报告（综合评分 ≥ 75分） |
| Phase 5 | `output-formatter` | 最终交付物（Markdown/Excel/CSV 等） |
| Phase 6 | `rag-query` | 历史知识检索 |

#### 用例质量红线

1. **可追溯性** - 用例编号格式 `TC-[项目]-[模块]-[序号]`
2. **可验证性** - 预期结果禁止模糊词，必须可客观判定
3. **数据完整性** - 每条用例必须提供具体测试数据值
4. **原子性** - 一个用例只验证一个检查点
5. **独立性** - 前置条件必须可独立准备
6. **安全性** - 涉及用户输入的功能点必须包含安全测试用例
7. **边界性** - 有取值范围的字段必须覆盖边界值

#### 多模态支持

- **文本输入** - 纯文本需求描述
- **图片输入** - 支持上传 PRD 截图、原型图、UI 设计稿
- **PDF 输入** - 支持 PDF 格式的需求文档
- **动态模型切换** - 检测到图片自动切换到豆包多模态视觉模型

---

## 4. 核心技术组件

### 4.1 Skills 驱动模式

**什么是 Skills?**

Skills 是存储在文件中的 **Markdown 格式指令文档**，定义了详细的执行步骤。Agent 通过 `read_file` 加载 skill 内容，按指引执行。

**优势**:

| 优势 | 说明 |
|------|------|
| **可维护性** | 修改测试流程只需改 Skill 文件 |
| **可读性** | Markdown 格式，人类可读 |
| **版本控制** | 可纳入 Git，变更可追踪 |
| **模块化** | 每个 Skill 独立，可复用 |
| **可扩展性** | 新增能力只需添加新 Skill |

**加载方式**:

```python
from deepagents.middleware import SkillsMiddleware

skills_middleware = SkillsMiddleware(
    backend=file_backend,
    sources=["/web/skills/"],
)

agent = create_agent(
    model=llm,
    tools=[...],
    middleware=[skills_middleware],
    system_prompt=SYSTEM_PROMPT,
)
```

### 4.2 RAG 知识库

**路径**: `src/app/mcp/rag_server.py`

**功能**:

1. **知识检索** - 查询历史测试用例、业务规则、领域知识
2. **上下文注入** - 将检索到的知识注入到 Agent 的对话上下文中
3. **知识库管理** - 支持文档上传、索引构建、更新

**MCP 工具**:

- `rag_query` - 执行 RAG 检索
- `add_document` - 添加文档到知识库
- `update_index` - 更新索引

### 4.3 MCP (Model Context Protocol) 服务

**设计动机**:

将源码分析能力封装为**标准化的 MCP 服务**，任何兼容的 AI Agent 都可以通过工具调用获取元素参考信息。

**核心工具**:

1. **scan_repository** - 扫描前端代码库，提取组件和元素信息
2. **query_element** - 查询特定组件的元素定位信息
3. **suggest_testid_injections** - 为缺少稳定定位符的元素生成 `data-testid` 建议
4. **detect_changes** - 检测代码库变更，识别受影响的组件和元素
5. **update_references** - 更新元素参考（组件注册表、定位器目录等）

### 4.4 Auto-Heal 自愈机制

**核心概念**:

当 UI 自动化测试因元素定位失败时，系统能够自动检测、定位问题并修复，而无需人工介入。

**自愈流程**:

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

**失败分类**:

| 失败类型 | 描述 | 处理方式 |
|---------|------|---------|
| **代码 Bug** | 应用真的坏了 | 标记为 Bug，报告给开发 |
| **测试更新需求** | 源码有意变更 | 触发自愈流程 |
| **环境问题** | 网络错误、超时 | 重试或调整 |

---

## 5. Skills 驱动模式

### 5.1 Skills 目录结构

```
src/workspace/
├── web/skills/                 # Web Agent Skills
│   ├── pw-dogfood/            # 探索性 QA（Mode A）
│   ├── component-aware-web-automation/  # 组件感知（Mode B）
│   ├── agent-browser-vs-playwright-cli/ # 框架选型
│   ├── playwright-cli/        # Playwright CLI 参考
│   └── agent-browser/         # Agent Browser 参考
│
├── api/skills/                 # API Agent Skills
│   ├── test-scenario-design/  # 场景设计
│   ├── playwright-api-testing/ # API 测试脚本
│   └── api-test-quality/      # 质量度量
│
├── testcase/skills/            # Testcase Agent Skills
│   ├── requirement-analysis/  # 需求分析
│   ├── test-strategy/         # 测试策略
│   ├── test-case-design/      # 用例设计
│   ├── test-data-generator/   # 测试数据生成
│   ├── quality-review/        # 质量评审
│   └── output-formatter/      # 输出格式化
│
└── rag/skills/                 # RAG Skills
    └── rag-query/             # RAG 检索
```

### 5.2 Skills 文件示例

**Web Agent - Mode A (pw-dogfood)**:

```markdown
# Playwright Dogfood Testing - 6-Phase Workflow

## Phase 1: Plan & Setup
1. Create output directory structure
2. Build test plan
3. Launch browser

## Phase 2: Systematic Exploration
1. Navigate to the target URL
2. Test all interactive elements
3. Probe edge cases

## Phase 3: Evidence Collection
1. Capture screenshots
2. Record traces
3. Collect console logs
4. Capture network traffic
5. Record videos

## Phase 4: Advanced Testing
1. Performance testing
2. Security testing
3. Accessibility testing
4. Responsive design testing
5. Multi-role testing

## Phase 5: Categorize & Prioritize
1. Review all findings
2. Remove duplicates
3. Categorize issues

## Phase 6: Report
1. Generate structured report
2. Include evidence links
```

---

## 6. 项目结构

```
ai-test-agent-system/              # 后端（Python）
├── .env                           # DeepSeek API 密钥配置
├── graph.json                     # LangGraph API 图谱注册
├── pyproject.toml                 # 依赖管理
├── start_server.py                # LangGraph API Server 启动入口
├── uv.lock                        # 锁定依赖版本
│
├── src/
│   ├── app/
│   │   ├── core/                  # 核心配置
│   │   │   ├── config.py         # 全局配置
│   │   │   └── llms.py           # LLM 模型工厂
│   │   │
│   │   ├── agents/                # 智能体目录
│   │   │   ├── api/              # API 测试智能体
│   │   │   │   ├── agent.py
│   │   │   │   └── tools/
│   │   │   ├── web/              # Web UI 自动化测试智能体
│   │   │   │   ├── agent.py
│   │   │   │   ├── tools.py
│   │   │   │   └── validate_agent.py
│   │   │   └── testcase/         # 测试用例生成智能体
│   │   │       ├── agent.py
│   │   │       └── tools.py
│   │   │
│   │   ├── middleware/            # Agent 中间件
│   │   │   ├── pdf_context.py    # PDF 上下文注入
│   │   │   └── rag_context.py    # RAG 检索上下文
│   │   │
│   │   ├── processors/            # 处理器
│   │   │   └── pdf.py            # PDF 文档解析
│   │   │
│   │   └── mcp/                   # MCP 服务器
│   │       └── rag_server.py     # RAG MCP Server
│   │
│   └── workspace/                 # Agent 工作空间
│       ├── web/                   # Web Agent 工作区
│       │   ├── skills/            # Skills 文件目录
│       │   │   ├── pw-dogfood/
│       │   │   ├── component-aware-web-automation/
│       │   │   ├── agent-browser-vs-playwright-cli/
│       │   │   ├── playwright-cli/
│       │   │   └── agent-browser/
│       │   └── ARTIFACT_CONTRACT.md  # 产物契约规范
│       │
│       ├── api/                   # API Agent 工作区
│       │   ├── skills/
│       │   └── playwright.config.ts
│       │
│       ├── testcase/              # Testcase Agent 工作区
│       │   └── skills/
│       │
│       ├── rag/                   # RAG 工作区
│       │   └── skills/
│       │
│       └── web-output/            # 测试输出目录
│           ├── qa/                # Mode A 输出
│           └── tests/             # Mode B 输出
│
├── testing-deep-agents-ui/        # 前端 UI（Next.js）
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/       # React 组件
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   ├── ConfigDialog.tsx
│   │   │   │   └── ...
│   │   │   ├── hooks/            # 自定义 Hooks
│   │   │   │   ├── useChat.ts
│   │   │   │   ├── useFileUpload.ts
│   │   │   │   └── useThreads.ts
│   │   │   ├── types/            # TypeScript 类型
│   │   │   └── utils/            # 工具函数
│   │   ├── components/ui/         # UI 组件库
│   │   └── providers/            # Context Providers
│   ├── package.json
│   ├── next.config.ts
│   └── readme.md
│
├── readme.md                      # 项目 README
├── PROJECT_README.md             # 本文档（项目全景）
└── auto-heal-read.md             # Auto-Heal 详细文档
```

---

## 7. 快速开始

### 7.1 环境准备

**系统要求**:
- Python 3.10+
- Node.js 18+
- Git

### 7.2 配置环境变量

创建 `.env` 文件:

```bash
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com
WORKSPACE_DIR=/path/to/workspace
OUTPUT_ROOT=/path/to/output
```

### 7.3 安装依赖

**后端**:
```bash
cd ai-test-agent-system
pip install -r requirements.txt
# 或使用 uv
uv pip install -r requirements.txt
```

**前端**:
```bash
cd testing-deep-agents-ui
npm install
```

### 7.4 启动服务

**启动 LangGraph API Server**:
```bash
cd ai-test-agent-system
python start_server.py
```

**启动 RAG MCP Server**:
```bash
cd ai-test-agent-system
python src/app/mcp/rag_server.py --transport=sse --port=8008
```

**启动前端 UI**:
```bash
cd testing-deep-agents-ui
npm run dev
```

### 7.5 运行测试

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

**API 测试**

```bash
curl -X POST http://localhost:8000/api/api/agent \
  -H "Content-Type: application/json" \
  -d '{"user_request": "测试 https://api.example.com/openapi.json"}'
```

**测试用例生成**

```bash
curl -X POST http://localhost:8000/api/testcase/agent \
  -H "Content-Type: application/json" \
  -d '{"user_request": "为用户登录功能生成测试用例"}'
```

---

## 8. 开发指南

### 8.1 添加新的 Agent

1. 在 `src/app/agents/` 下创建新目录
2. 创建 `agent.py` 和 `tools.py`
3. 在 `graph.json` 中注册 Agent
4. 在 `start_server.py` 中添加路由

### 8.2 添加新的 Skill

1. 在对应的 `src/workspace/*/skills/` 目录下创建新文件夹
2. 创建 `SKILL.md` 文件
3. 在 Agent 的 `SYSTEM_PROMPT` 中添加激活指令

### 8.3 添加新的 MCP 工具

1. 在 `src/app/mcp/` 目录下创建 MCP Server
2. 定义工具函数
3. 在 Agent 中注册工具

### 8.4 前端开发

**技术栈**:
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui

**主要组件**:
- `ChatInterface` - 聊天界面
- `ThreadList` - 会话列表
- `ConfigDialog` - 配置对话框
- `FileViewDialog` - 文件查看器

---

## 9. 常见问题

### Q1: 为什么使用 Skills 而不是硬编码?

**A**: Skills 提供了灵活性和可维护性：
- 修改测试流程只需改 Skill 文件，无需改代码
- Markdown 格式，人类可读可编辑
- 可以通过版本控制追踪变更
- 新增测试能力只需添加新 Skill

### Q2: MCP 服务和 Skill 有什么区别?

**A**: 
- **MCP 服务** - 提供标准化的工具接口，服务端直接执行，性能更高，适合数据查询和计算密集型任务
- **Skill** - 用于流程定义和操作指南，由 Agent 解释和执行

### Q3: 自愈机制会自动应用补丁吗?

**A**: 默认为半自动模式：系统生成补丁，人工审核后选择应用或拒绝。可配置为全自动模式（高风险）。

### Q4: 支持哪些前端框架?

**A**: 已支持 React（.tsx/.jsx），计划中：Vue、Angular、Svelte。

### Q5: 如何切换 LLM 模型?

**A**: 在 `src/app/core/llms.py` 中配置：
```python
from langchain.chat_models import init_chat_model

# DeepSeek
deepseek_model = init_chat_model("deepseek:deepseek-chat")

# 豆包多模态
image_llm_model = init_chat_model("doubao:vision-pro")
```

---

## 10. 参考资料

### 10.1 项目文档

- [项目 README](readme.md)
- [Auto-Heal 详细文档](auto-heal-read.md)
- [Artifact 契约规范](ai-test-agent-system/src/workspace/web/ARTIFACT_CONTRACT.md)
- [Web Agent 详解](ai-test-agent-system/src/read.md)

### 10.2 外部资源

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [deepagents 文档](https://github.com/deepagents/deepagents)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Playwright 官方文档](https://playwright.dev/)
- [MASTEST 论文](https://arxiv.org/abs/2511.18038)

### 10.3 相关技术

- **LangGraph** - Agent 编排框架
- **LangChain** - LLM 应用开发框架
- **deepagents** - Agent 构建库
- **Playwright** - 浏览器自动化和测试框架
- **Next.js** - React 框架
- **FastMCP** - MCP 服务框架

---

**文档版本**: v2.0.0
**最后更新**: 2026-05-10
**维护者**: AI Test Agent System Team

---

## 附录

### A. 术语表

| 术语 | 全称 | 说明 |
|------|------|------|
| LLM | Large Language Model | 大语言模型 |
| RAG | Retrieval-Augmented Generation | 检索增强生成 |
| MCP | Model Context Protocol | 模型上下文协议 |
| POM | Page Object Model | 页面对象模型 |
| API | Application Programming Interface | 应用程序接口 |
| UI | User Interface | 用户界面 |
| QA | Quality Assurance | 质量保证 |
| MASTEST | Model-Assisted Systematic Test | 模型辅助系统测试 |

### B. 贡献指南

欢迎贡献代码、文档、Skills 和测试用例！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### C. 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

---

**🎯 项目愿景**: 通过 AI 驱动的多智能体系统，实现测试自动化的新时代 - 智能化、自适应、自愈性。