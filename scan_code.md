# Mode B 组件感知扫描报告：frontend-app (Vibranium AI Assistant)

> **扫描项目**: `F:\codex-work\testd-data-sys\frontend-app`  
> **扫描时间**: 2026-05-11  
> **扫描模式**: Mode B — 组件感知测试生成（7-Agent 流水线静态分析）  
> **框架**: React 18 + TypeScript + Vite + Ant Design 5 + Axios

---

## 📋 目录

- [1. 项目概况](#1-项目概况)
- [2. Mode B 流水线详解](#2-mode-b-流水线详解)
- [3. Agent 1: Script Analyst — 组件注册表](#3-agent-1-script-analyst--组件注册表)
- [4. Agent 2: Stage Manager — testid 注入](#4-agent-2-stage-manager--testid-注入)
- [5. Agent 3: Blocking Coach — 定位器目录](#5-agent-3-blocking-coach--定位器目录)
- [6. Agent 4: Set Designer — POM 生成](#6-agent-4-set-designer--pom-生成)
- [7. Agent 5: Choreographer — 用户旅程](#7-agent-5-choreographer--用户旅程)
- [8. Agent 6: Assistant Director — 测试脚本](#8-agent-6-assistant-director--测试脚本)
- [9. Agent 7: Continuity Lead — 执行与自愈](#9-agent-7-continuity-lead--执行与自愈)
- [10. 最终元素库总览](#10-最终元素库总览)

---

## 1. 项目概况

### 1.1 技术栈识别

| 项目 | 值 |
|------|-----|
| **项目名称** | vibranium-ai-assistant-frontend |
| **版本** | 0.1.0 |
| **框架** | React 18.3 + TypeScript 5.9 |
| **构建工具** | Vite 7.2 |
| **UI 库** | Ant Design 5.27 + @ant-design/icons 5.6 |
| **HTTP 客户端** | Axios 1.13 |
| **路由方式** | 状态路由（useState，非 react-router） |
| **API 基地址** | `http://127.0.0.1:9001`（可配置 `VITE_API_BASE_URL`） |

### 1.2 项目结构

```
src/
├── App.tsx                           # 根组件，状态路由
├── main.tsx                          # 入口文件
├── index.css                         # 全局样式
├── vite-env.d.ts                     # Vite 类型声明
│
├── api/                              # API 层
│   ├── client.ts                     # Axios 实例（baseURL + timeout）
│   └── agents.ts                     # Agent CRUD + Chat API
│
├── components/                       # 共享组件
│   └── AgentDetailDrawer.tsx         # Agent 详情抽屉
│
├── constants/                        # 常量
│   └── routes.ts                     # 路由类型 + 标签映射
│
├── hooks/                            # 自定义 Hooks
│   └── useAgents.ts                  # Agent 列表 + 选项加载
│
├── layouts/                          # 布局组件
│   └── AppLayout.tsx                 # 侧边栏 + 顶栏布局
│
├── pages/                            # 页面组件
│   ├── AgentMarketPage.tsx           # Agent 市场（搜索 + 卡片列表）
│   ├── AgentConfigurationPage.tsx    # Agent 配置（CRUD 表格 + 模态表单）
│   └── AgentChatPage.tsx             # Agent 聊天（多选 + 消息列表）
│
├── store/                            # 状态管理（空目录）
├── styles/                           # 样式（空目录）
├── types/                            # TypeScript 类型
│   └── agent.ts                      # Agent, AgentPayload, ChatMessage 等接口
│
└── utils/                            # 工具函数
    └── agent.ts                      # 创建空 AgentPayload
```

### 1.3 业务领域

这是一个 **AI Agent 管理平台**，包含三大核心业务：

| 业务 | 页面 | 功能 |
|------|------|------|
| **Agent 市场** | AgentMarketPage | 搜索/筛选 Agent，查看 Agent 详情 |
| **Agent 配置** | AgentConfigurationPage | 创建/编辑/删除 Agent，表单含 10 个字段 |
| **Agent 聊天** | AgentChatPage | 选择多 Agent，发送问题，查看回复和工具/知识使用情况 |

### 1.4 API 端点

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/options` | 获取选项（models, tools, knowledge_bases, skills） |
| GET | `/api/agents` | 获取 Agent 列表（支持 q, category 查询参数） |
| GET | `/api/agents/:id` | 获取单个 Agent |
| POST | `/api/agents` | 创建 Agent |
| PUT | `/api/agents/:id` | 更新 Agent |
| DELETE | `/api/agents/:id` | 删除 Agent |
| POST | `/api/chat` | 发送聊天消息 |

---

## 2. Mode B 流水线详解

Mode B 的 7-Agent 流水线分为两个阶段：

```
Phase 1: Setup the Stage（静态分析，不打开浏览器）
  Agent 1: Script Analyst    → component-registry.json
  Agent 2: Stage Manager     → testid-injections.json
  Agent 3: Blocking Coach    → locator-catalog.json
  Agent 4: Set Designer      → poms/*.ts

Phase 2: Run the Show（生成与执行测试）
  Agent 5: Choreographer     → journeys.json
  Agent 6: Assistant Director → tests/*.spec.ts
  Agent 7: Continuity Lead   → execution-report.json
```

下面逐个 Agent 详细说明对本项目的扫描结果。

---

## 3. Agent 1: Script Analyst — 组件注册表

### 3.1 扫描过程

Script Analyst 按照以下步骤扫描：

1. **发现组件** — 扫描所有 `.tsx` 文件，识别函数组件
2. **提取 Props** — 解析 TypeScript interface
3. **提取 State** — 识别 `useState` 调用
4. **提取交互元素** — 识别 onClick/onChange/onSubmit 等事件处理
5. **提取条件渲染** — 识别三元表达式、&& 运算符
6. **提取 Feature Flags** — 识别条件分支（本项目无 Feature Flags）
7. **构建注册表** — 写入 `component-registry.json`

### 3.2 扫描发现的组件

| # | 组件 ID | 文件路径 | 类型 | 子组件 |
|---|---------|----------|------|--------|
| 1 | App | src/App.tsx | function-component | AppLayout, AgentMarketPage, AgentConfigurationPage, AgentChatPage |
| 2 | AppLayout | src/layouts/AppLayout.tsx | function-component | Layout, Menu, Typography |
| 3 | AgentMarketPage | src/pages/AgentMarketPage.tsx | function-component | Input, Select, Button, Card, AgentDetailDrawer |
| 4 | AgentConfigurationPage | src/pages/AgentConfigurationPage.tsx | function-component | Table, Form, Modal, Button, Popconfirm |
| 5 | AgentChatPage | src/pages/AgentChatPage.tsx | function-component | Select, Input, Button, List |
| 6 | AgentDetailDrawer | src/components/AgentDetailDrawer.tsx | function-component | Drawer, Descriptions, Tag |

### 3.3 完整组件注册表

```json
{
  "$schema": "https://component-aware.schema/v1/registry",
  "metadata": {
    "repo": "F:\\codex-work\\testd-data-sys\\frontend-app",
    "branch": "main",
    "framework": "react",
    "frameworkVersion": "18.3",
    "uiLibrary": "antd@5.27",
    "scanTimestamp": "2026-05-11T00:22:00Z",
    "totalComponents": 6
  },
  "components": [
    {
      "id": "App",
      "filePath": "src/App.tsx",
      "framework": "react",
      "type": "function-component",
      "props": [],
      "state": [
        {
          "name": "activeRoute",
          "type": "AppRoute",
          "initialValue": "'market'",
          "setter": "setActiveRoute"
        }
      ],
      "interactiveElements": [],
      "conditionalRendering": [
        {
          "condition": "activeRoute === 'market'",
          "renders": "AgentMarketPage",
          "type": "route-switch"
        },
        {
          "condition": "activeRoute === 'configuration'",
          "renders": "AgentConfigurationPage",
          "type": "route-switch"
        },
        {
          "condition": "activeRoute === 'chat'",
          "renders": "AgentChatPage",
          "type": "route-switch"
        }
      ],
      "featureFlags": [],
      "childComponents": ["AppLayout", "AgentMarketPage", "AgentConfigurationPage", "AgentChatPage"],
      "accessibilityInfo": { "ariaLabels": [], "roles": [] }
    },
    {
      "id": "AppLayout",
      "filePath": "src/layouts/AppLayout.tsx",
      "framework": "react",
      "type": "function-component",
      "props": [
        { "name": "activeRoute", "type": "AppRoute", "required": true, "defaultValue": null },
        { "name": "onRouteChange", "type": "(route: AppRoute) => void", "required": true, "defaultValue": null },
        { "name": "children", "type": "React.ReactNode", "required": true, "defaultValue": null }
      ],
      "state": [],
      "interactiveElements": [
        {
          "elementType": "menu-item",
          "role": "nav-agent-market",
          "binding": null,
          "handler": "onClick → onRouteChange('market')",
          "attributes": { "data-testid": "nav-agent-market" }
        },
        {
          "elementType": "menu-item",
          "role": "nav-agent-configuration",
          "binding": null,
          "handler": "onClick → onRouteChange('configuration')",
          "attributes": { "data-testid": "nav-agent-configuration" }
        },
        {
          "elementType": "menu-item",
          "role": "nav-agent-chat",
          "binding": null,
          "handler": "onClick → onRouteChange('chat')",
          "attributes": { "data-testid": "nav-agent-chat" }
        }
      ],
      "conditionalRendering": [],
      "featureFlags": [],
      "childComponents": [],
      "accessibilityInfo": {
        "ariaLabels": [],
        "roles": []
      }
    },
    {
      "id": "AgentMarketPage",
      "filePath": "src/pages/AgentMarketPage.tsx",
      "framework": "react",
      "type": "function-component",
      "props": [],
      "state": [
        { "name": "query", "type": "string", "initialValue": "''", "setter": "setQuery" },
        { "name": "category", "type": "string", "initialValue": "'all'", "setter": "setCategory" },
        { "name": "agents", "type": "Agent[]", "initialValue": "[]", "setter": "setAgents" },
        { "name": "selected", "type": "Agent | null", "initialValue": "null", "setter": "setSelected" },
        { "name": "loading", "type": "boolean", "initialValue": "false", "setter": "setLoading" }
      ],
      "interactiveElements": [
        {
          "elementType": "input",
          "role": "search-input",
          "binding": "query",
          "handler": "onChange → setQuery, onPressEnter → loadAgents",
          "attributes": { "data-testid": "agent-market-search-input", "placeholder": "Search agent...", "prefix": "SearchOutlined" }
        },
        {
          "elementType": "select",
          "role": "category-select",
          "binding": "category",
          "handler": "onChange → setCategory",
          "attributes": { "data-testid": "agent-market-category-select" }
        },
        {
          "elementType": "button",
          "role": "search-button",
          "binding": null,
          "handler": "onClick → loadAgents",
          "attributes": { "data-testid": "agent-market-search-button", "type": "primary", "loading": "loading" }
        },
        {
          "elementType": "card",
          "role": "agent-card",
          "binding": "agent.id",
          "handler": null,
          "attributes": { "data-testid": "agent-market-card-${agent.id}" }
        },
        {
          "elementType": "button",
          "role": "view-detail-button",
          "binding": "agent.id",
          "handler": "onClick → setSelected(agent)",
          "attributes": { "data-testid": "agent-market-view-detail-${agent.id}", "type": "link" }
        }
      ],
      "conditionalRendering": [
        {
          "condition": "agents.length === 0",
          "renders": "Empty",
          "type": "empty-state"
        },
        {
          "condition": "agents.length > 0",
          "renders": "Row > Col > Card (agent list)",
          "type": "data-state"
        }
      ],
      "featureFlags": [],
      "childComponents": ["AgentDetailDrawer"],
      "accessibilityInfo": { "ariaLabels": [], "roles": [] }
    },
    {
      "id": "AgentConfigurationPage",
      "filePath": "src/pages/AgentConfigurationPage.tsx",
      "framework": "react",
      "type": "function-component",
      "props": [],
      "state": [
        { "name": "editing", "type": "Agent | null", "initialValue": "null", "setter": "setEditing" },
        { "name": "open", "type": "boolean", "initialValue": "false", "setter": "setOpen" }
      ],
      "interactiveElements": [
        {
          "elementType": "button",
          "role": "create-button",
          "binding": null,
          "handler": "onClick → openCreate()",
          "attributes": { "data-testid": "agent-create-button", "type": "primary" }
        },
        {
          "elementType": "table",
          "role": "agent-table",
          "binding": null,
          "handler": null,
          "attributes": { "data-testid": "agent-configuration-table", "rowKey": "id" }
        },
        {
          "elementType": "button",
          "role": "edit-button",
          "binding": "row.id",
          "handler": "onClick → openEdit(row)",
          "attributes": { "data-testid": "agent-edit-button-${row.id}" }
        },
        {
          "elementType": "button",
          "role": "delete-button",
          "binding": "row.id",
          "handler": "onConfirm → deleteAgent(row)",
          "attributes": { "data-testid": "agent-delete-button-${row.id}", "danger": true }
        },
        {
          "elementType": "form",
          "role": "editor-form",
          "binding": null,
          "handler": "onFinish → submit(values)",
          "attributes": { "data-testid": "agent-editor-form" }
        },
        {
          "elementType": "input",
          "role": "name-input",
          "binding": "name",
          "handler": null,
          "attributes": { "data-testid": "agent-name-input", "required": true }
        },
        {
          "elementType": "input",
          "role": "icon-input",
          "binding": "icon",
          "handler": null,
          "attributes": { "data-testid": "agent-icon-input", "required": true }
        },
        {
          "elementType": "select",
          "role": "model-select",
          "binding": "model",
          "handler": null,
          "attributes": { "data-testid": "agent-model-select", "required": true }
        },
        {
          "elementType": "textarea",
          "role": "description-input",
          "binding": "description",
          "handler": null,
          "attributes": { "data-testid": "agent-description-input", "required": true }
        },
        {
          "elementType": "textarea",
          "role": "system-prompt-input",
          "binding": "system_prompt",
          "handler": null,
          "attributes": { "data-testid": "agent-system-prompt-input", "required": true }
        },
        {
          "elementType": "select",
          "role": "tools-select",
          "binding": "tools",
          "handler": null,
          "attributes": { "data-testid": "agent-tools-select", "mode": "multiple" }
        },
        {
          "elementType": "select",
          "role": "knowledge-select",
          "binding": "knowledge_bases",
          "handler": null,
          "attributes": { "data-testid": "agent-knowledge-select", "mode": "multiple" }
        },
        {
          "elementType": "select",
          "role": "skills-select",
          "binding": "skills",
          "handler": null,
          "attributes": { "data-testid": "agent-skills-select", "mode": "multiple" }
        },
        {
          "elementType": "select",
          "role": "response-style-select",
          "binding": "response_style",
          "handler": null,
          "attributes": { "data-testid": "agent-response-style-select", "required": true }
        },
        {
          "elementType": "select",
          "role": "market-category-form-select",
          "binding": "market_category",
          "handler": null,
          "attributes": { "data-testid": "agent-market-category-form-select", "required": true }
        },
        {
          "elementType": "button",
          "role": "save-button",
          "binding": null,
          "handler": "onClick → form.submit()",
          "attributes": { "data-testid": "agent-save-button", "type": "primary", "htmlType": "submit" }
        }
      ],
      "conditionalRendering": [
        {
          "condition": "editing !== null",
          "renders": "Modal title 'Edit Agent'",
          "type": "edit-mode"
        },
        {
          "condition": "editing === null",
          "renders": "Modal title 'Create Agent'",
          "type": "create-mode"
        }
      ],
      "featureFlags": [],
      "childComponents": [],
      "accessibilityInfo": { "ariaLabels": [], "roles": [] }
    },
    {
      "id": "AgentChatPage",
      "filePath": "src/pages/AgentChatPage.tsx",
      "framework": "react",
      "type": "function-component",
      "props": [],
      "state": [
        { "name": "agents", "type": "Agent[]", "initialValue": "[]", "setter": "setAgents" },
        { "name": "selectedAgentIds", "type": "string[]", "initialValue": "[]", "setter": "setSelectedAgentIds" },
        { "name": "question", "type": "string", "initialValue": "''", "setter": "setQuestion" },
        { "name": "messages", "type": "ChatMessage[]", "initialValue": "[]", "setter": "setMessages" },
        { "name": "sending", "type": "boolean", "initialValue": "false", "setter": "setSending" }
      ],
      "interactiveElements": [
        {
          "elementType": "select",
          "role": "agent-select",
          "binding": "selectedAgentIds",
          "handler": "onChange → setSelectedAgentIds",
          "attributes": { "data-testid": "chat-agent-select", "mode": "multiple" }
        },
        {
          "elementType": "input",
          "role": "question-input",
          "binding": "question",
          "handler": "onChange → setQuestion, onPressEnter → submit",
          "attributes": { "data-testid": "chat-question-input" }
        },
        {
          "elementType": "button",
          "role": "send-button",
          "binding": null,
          "handler": "onClick → submit()",
          "attributes": { "data-testid": "chat-send-button", "type": "primary", "loading": "sending" }
        }
      ],
      "conditionalRendering": [
        {
          "condition": "messages.length === 0",
          "renders": "Typography.Text 'No messages yet.'",
          "type": "empty-state"
        },
        {
          "condition": "messages.length > 0",
          "renders": "List of ChatMessage items",
          "type": "data-state"
        },
        {
          "condition": "item.role === 'assistant'",
          "renders": "Tools and Knowledge usage text",
          "type": "assistant-message-detail"
        }
      ],
      "featureFlags": [],
      "childComponents": [],
      "accessibilityInfo": { "ariaLabels": [], "roles": [] }
    },
    {
      "id": "AgentDetailDrawer",
      "filePath": "src/components/AgentDetailDrawer.tsx",
      "framework": "react",
      "type": "function-component",
      "props": [
        { "name": "agent", "type": "Agent | null", "required": true, "defaultValue": null },
        { "name": "open", "type": "boolean", "required": true, "defaultValue": null },
        { "name": "onClose", "type": "() => void", "required": true, "defaultValue": null }
      ],
      "state": [],
      "interactiveElements": [],
      "conditionalRendering": [
        {
          "condition": "agent !== null",
          "renders": "Agent detail content (Descriptions)",
          "type": "data-state"
        }
      ],
      "featureFlags": [],
      "childComponents": [],
      "accessibilityInfo": { "ariaLabels": [], "roles": [] }
    }
  ]
}
```

### 3.4 扫描分析总结

**关键发现**：

1. **data-testid 覆盖率极高** — 项目已预置了 20+ 个 `data-testid`，这是非常好的实践
2. **无 Feature Flags** — 不存在 Feature Flag 条件分支，状态空间较小
3. **无权限模型** — 没有角色/权限控制，所有用户看到相同 UI
4. **状态路由** — 使用 `useState` 而非 react-router，路由切换通过回调函数
5. **Ant Design 组件为主** — 所有交互元素均为 Ant Design 组件，非原生 HTML 元素

---

## 4. Agent 2: Stage Manager — testid 注入

### 4.1 注入分析

Stage Manager 检查每个交互元素是否有稳定标识符。对于本项目：

| 检查项 | 状态 |
|--------|------|
| 已有 `data-testid` | ✅ 20+ 个元素已有 |
| `aria-label` | ❌ 无 |
| 语义 role + name | ⚠️ 部分 Ant Design 组件自带 |

### 4.2 需要注入的 testid

由于项目已经预置了大量 `data-testid`，需要注入的极少：

```json
{
  "version": "1.0",
  "generatedAt": "2026-05-11T00:22:00Z",
  "injections": [
    {
      "componentId": "App",
      "filePath": "src/App.tsx",
      "element": "root div",
      "reason": "根组件缺少容器标识",
      "testid": "App-root",
      "patch": "添加 <div data-testid=\"app-root\"> 包裹"
    },
    {
      "componentId": "AgentMarketPage",
      "filePath": "src/pages/AgentMarketPage.tsx",
      "element": "Empty component",
      "reason": "空状态组件缺少标识",
      "testid": "agent-market-empty",
      "patch": "添加 <Empty data-testid=\"agent-market-empty\" ...>"
    },
    {
      "componentId": "AgentChatPage",
      "filePath": "src/pages/AgentChatPage.tsx",
      "element": "Empty messages text",
      "reason": "空消息提示缺少标识",
      "testid": "chat-empty-messages",
      "patch": "添加 data-testid 到 Typography.Text"
    },
    {
      "componentId": "AgentChatPage",
      "filePath": "src/pages/AgentChatPage.tsx",
      "element": "Assistant message tools/knowledge detail",
      "reason": "工具/知识使用详情缺少标识",
      "testid": "chat-message-tools-detail",
      "patch": "添加 data-testid 到 Typography.Text (工具/知识行)"
    },
    {
      "componentId": "AgentConfigurationPage",
      "filePath": "src/pages/AgentConfigurationPage.tsx",
      "element": "Modal close button",
      "reason": "模态框关闭按钮缺少标识",
      "testid": "agent-editor-cancel",
      "patch": "添加 data-testid 到 Modal onCancel 按钮"
    }
  ],
  "summary": {
    "totalElements": 28,
    "alreadyHaveTestId": 23,
    "needInjection": 5,
    "coverageBefore": "82%",
    "coverageAfter": "100%"
  }
}
```

### 4.3 注入评价

> 🌟 **本项目 testid 覆盖率极高（82%）**，远高于一般项目。开发者显然有意识地添加了 `data-testid`，这对自动化测试非常友好。仅需要 5 处补充注入即可达到 100% 覆盖。

---

## 5. Agent 3: Blocking Coach — 定位器目录

### 5.1 定位器优先级链

Blocking Coach 为每个交互元素生成 4 级优先级定位器：

```
Priority 1: data-testid — 确定性，抗重构
Priority 2: role + accessible name — 抗 DOM 结构变化
Priority 3: 组件类型 + key prop — 框架感知
Priority 4: 稳定结构选择器 — 最后手段
```

### 5.2 完整定位器目录

```json
{
  "version": "1.0",
  "generatedAt": "2026-05-11T00:22:00Z",
  "entries": [
    {
      "componentId": "AppLayout",
      "elementRole": "nav-market",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('nav-agent-market')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('menuitem', { name: 'Agent Market' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-menu-item').nth(0)" },
        { "priority": 4, "strategy": "structural", "value": "locator('.app-sider .ant-menu-item').first()" }
      ]
    },
    {
      "componentId": "AppLayout",
      "elementRole": "nav-configuration",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('nav-agent-configuration')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('menuitem', { name: 'Agent Configuration' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-menu-item').nth(1)" },
        { "priority": 4, "strategy": "structural", "value": "locator('.app-sider .ant-menu-item').nth(1)" }
      ]
    },
    {
      "componentId": "AppLayout",
      "elementRole": "nav-chat",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('nav-agent-chat')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('menuitem', { name: 'Agent Chat' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-menu-item').nth(2)" },
        { "priority": 4, "strategy": "structural", "value": "locator('.app-sider .ant-menu-item').nth(2)" }
      ]
    },
    {
      "componentId": "AgentMarketPage",
      "elementRole": "search-input",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-market-search-input')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('searchbox')" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.toolbar input.ant-input').first()" },
        { "priority": 4, "strategy": "structural", "value": "locator('.toolbar .ant-input-affix-wrapper').first()" }
      ]
    },
    {
      "componentId": "AgentMarketPage",
      "elementRole": "category-select",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-market-category-select')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('combobox')" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.toolbar .ant-select').nth(0)" },
        { "priority": 4, "strategy": "structural", "value": "locator('.toolbar .ant-select').first()" }
      ]
    },
    {
      "componentId": "AgentMarketPage",
      "elementRole": "search-button",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-market-search-button')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('button', { name: 'Search' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.toolbar button.ant-btn-primary')" },
        { "priority": 4, "strategy": "structural", "value": "locator('.toolbar .ant-btn-primary').first()" }
      ]
    },
    {
      "componentId": "AgentMarketPage",
      "elementRole": "agent-card",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-market-card-${id}')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('article', { name: /agent name/ })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-card').filter({ hasText: 'agent name' })" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-row .ant-card').nth(index)" }
      ]
    },
    {
      "componentId": "AgentMarketPage",
      "elementRole": "view-detail-button",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-market-view-detail-${id}')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('button', { name: 'View Detail' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-card-actions button').nth(0)" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-card-actions .ant-btn-link').first()" }
      ]
    },
    {
      "componentId": "AgentConfigurationPage",
      "elementRole": "create-button",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-create-button')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('button', { name: /New Agent/ })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.page-heading button.ant-btn-primary')" },
        { "priority": 4, "strategy": "structural", "value": "locator('.page-heading .ant-btn-primary')" }
      ]
    },
    {
      "componentId": "AgentConfigurationPage",
      "elementRole": "agent-table",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-configuration-table')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('table')" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-table')" },
        { "priority": 4, "strategy": "structural", "value": "locator('section .ant-table').first()" }
      ]
    },
    {
      "componentId": "AgentConfigurationPage",
      "elementRole": "edit-button",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-edit-button-${id}')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('button', { name: 'Edit' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('tr').filter({ hasText: 'name' }).getByRole('button', { name: 'Edit' })" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-table-row-actions .ant-btn').nth(0)" }
      ]
    },
    {
      "componentId": "AgentConfigurationPage",
      "elementRole": "delete-button",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-delete-button-${id}')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('button', { name: 'Delete' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('tr').filter({ hasText: 'name' }).getByRole('button', { name: 'Delete' })" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-table-row-actions .ant-btn-dangerous').first()" }
      ]
    },
    {
      "componentId": "AgentConfigurationPage",
      "elementRole": "editor-form",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-editor-form')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('form')" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-modal .ant-form')" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-modal-body form').first()" }
      ]
    },
    {
      "componentId": "AgentConfigurationPage",
      "elementRole": "name-input",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-name-input')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('textbox', { name: 'Agent Name' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-form-item').filter({ hasText: 'Agent Name' }).getByRole('textbox')" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-modal form #name')" }
      ]
    },
    {
      "componentId": "AgentConfigurationPage",
      "elementRole": "save-button",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-save-button')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('button', { name: 'Save Agent' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-modal button.ant-btn-primary[type=submit]')" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-modal .ant-btn-primary').last()" }
      ]
    },
    {
      "componentId": "AgentChatPage",
      "elementRole": "agent-select",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('chat-agent-select')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('combobox')" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.chat-workspace .ant-select').first()" },
        { "priority": 4, "strategy": "structural", "value": "locator('.chat-workspace .ant-select').nth(0)" }
      ]
    },
    {
      "componentId": "AgentChatPage",
      "elementRole": "question-input",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('chat-question-input')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('textbox')" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.chat-input-row input.ant-input')" },
        { "priority": 4, "strategy": "structural", "value": "locator('.chat-input-row input').first()" }
      ]
    },
    {
      "componentId": "AgentChatPage",
      "elementRole": "send-button",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('chat-send-button')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('button', { name: 'Send' })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.chat-input-row button.ant-btn-primary')" },
        { "priority": 4, "strategy": "structural", "value": "locator('.chat-input-row .ant-btn-primary')" }
      ]
    },
    {
      "componentId": "AgentDetailDrawer",
      "elementRole": "drawer",
      "priorityChain": [
        { "priority": 1, "strategy": "data-testid", "value": "getByTestId('agent-detail-drawer')" },
        { "priority": 2, "strategy": "role+name", "value": "getByRole('dialog', { name: /Agent Detail/ })" },
        { "priority": 3, "strategy": "component-prop", "value": "locator('.ant-drawer').filter({ hasText: 'Agent Detail' })" },
        { "priority": 4, "strategy": "structural", "value": "locator('.ant-drawer-open').last()" }
      ]
    }
  ]
}
```

---

## 6. Agent 4: Set Designer — POM 生成

### 6.1 页面与路由映射

| 路由 | 页面组件 | POM 类名 |
|------|----------|----------|
| market | AgentMarketPage | AgentMarketPage |
| configuration | AgentConfigurationPage | AgentConfigurationPage |
| chat | AgentChatPage | AgentChatPage |
| (全局) | AppLayout | AppLayout |

### 6.2 POM 类设计

#### AppLayout POM

```typescript
// poms/AppLayout.ts
import { type Page, type Locator } from '@playwright/test'

export class AppLayout {
  readonly page: Page

  // Locators — 来自 locator-catalog.json，永远不手写
  private readonly brand = this.page.getByTestId('app-brand')
  private readonly navMarket = this.page.getByTestId('nav-agent-market')
  private readonly navConfiguration = this.page.getByTestId('nav-agent-configuration')
  private readonly navChat = this.page.getByTestId('nav-agent-chat')
  private readonly header = this.page.locator('.app-header')
  private readonly content = this.page.locator('.app-content')

  constructor(page: Page) {
    this.page = page
  }

  // 语义动作 — 业务级别，非 DOM 级别
  async navigateToMarket(): Promise<void> {
    await this.navMarket.click()
  }

  async navigateToConfiguration(): Promise<void> {
    await this.navConfiguration.click()
  }

  async navigateToChat(): Promise<void> {
    await this.navChat.click()
  }

  async assertBrandVisible(): Promise<void> {
    await this.brand.waitFor({ state: 'visible' })
  }

  async assertCurrentRoute(expected: string): Promise<void> {
    const activeItem = this.page.locator('.ant-menu-item-selected')
    await activeItem.waitFor({ state: 'visible' })
  }
}
```

#### AgentMarketPage POM

```typescript
// poms/AgentMarketPage.ts
import { type Page, type Locator } from '@playwright/test'

export class AgentMarketPage {
  readonly page: Page

  // Locators
  private readonly searchInput = this.page.getByTestId('agent-market-search-input')
  private readonly categorySelect = this.page.getByTestId('agent-market-category-select')
  private readonly searchButton = this.page.getByTestId('agent-market-search-button')
  private readonly emptyState = this.page.getByTestId('agent-market-empty')

  constructor(page: Page) {
    this.page = page
  }

  // 语义动作
  async searchAgents(query: string): Promise<void> {
    await this.searchInput.fill(query)
    await this.searchButton.click()
  }

  async filterByCategory(category: string): Promise<void> {
    await this.categorySelect.click()
    await this.page.getByRole('option', { name: category }).click()
  }

  async searchWithEnter(query: string): Promise<void> {
    await this.searchInput.fill(query)
    await this.searchInput.press('Enter')
  }

  async viewAgentDetail(agentId: string): Promise<void> {
    await this.page.getByTestId(`agent-market-view-detail-${agentId}`).click()
  }

  async getAgentCard(agentId: string): Promise<Locator> {
    return this.page.getByTestId(`agent-market-card-${agentId}`)
  }

  async assertEmptyState(): Promise<void> {
    await this.emptyState.waitFor({ state: 'visible' })
  }

  async assertAgentCardVisible(agentId: string): Promise<void> {
    await this.page.getByTestId(`agent-market-card-${agentId}`).waitFor({ state: 'visible' })
  }

  async getAgentCardCount(): Promise<number> {
    return this.page.locator('.ant-card').count()
  }
}
```

#### AgentConfigurationPage POM

```typescript
// poms/AgentConfigurationPage.ts
import { type Page, type Locator } from '@playwright/test'
import type { AgentPayload } from '../types/agent'

export class AgentConfigurationPage {
  readonly page: Page

  // Locators
  private readonly createButton = this.page.getByTestId('agent-create-button')
  private readonly agentTable = this.page.getByTestId('agent-configuration-table')
  private readonly editorForm = this.page.getByTestId('agent-editor-form')
  private readonly nameInput = this.page.getByTestId('agent-name-input')
  private readonly iconInput = this.page.getByTestId('agent-icon-input')
  private readonly modelSelect = this.page.getByTestId('agent-model-select')
  private readonly descriptionInput = this.page.getByTestId('agent-description-input')
  private readonly systemPromptInput = this.page.getByTestId('agent-system-prompt-input')
  private readonly toolsSelect = this.page.getByTestId('agent-tools-select')
  private readonly knowledgeSelect = this.page.getByTestId('agent-knowledge-select')
  private readonly skillsSelect = this.page.getByTestId('agent-skills-select')
  private readonly responseStyleSelect = this.page.getByTestId('agent-response-style-select')
  private readonly marketCategorySelect = this.page.getByTestId('agent-market-category-form-select')
  private readonly saveButton = this.page.getByTestId('agent-save-button')

  constructor(page: Page) {
    this.page = page
  }

  // 语义动作
  async openCreateModal(): Promise<void> {
    await this.createButton.click()
    await this.editorForm.waitFor({ state: 'visible' })
  }

  async openEditModal(agentId: string): Promise<void> {
    await this.page.getByTestId(`agent-edit-button-${agentId}`).click()
    await this.editorForm.waitFor({ state: 'visible' })
  }

  async deleteAgent(agentId: string): Promise<void> {
    await this.page.getByTestId(`agent-delete-button-${agentId}`).click()
    await this.page.getByRole('button', { name: 'OK' }).click()
  }

  async fillAgentForm(payload: AgentPayload): Promise<void> {
    await this.nameInput.fill(payload.name)
    await this.iconInput.fill(payload.icon)
    await this.modelSelect.click()
    await this.page.getByRole('option', { name: payload.model }).click()
    await this.descriptionInput.fill(payload.description)
    await this.systemPromptInput.fill(payload.system_prompt)
    // 多选字段需要逐个选择
    for (const tool of payload.tools) {
      await this.toolsSelect.click()
      await this.page.getByRole('option', { name: tool }).click()
    }
    for (const kb of payload.knowledge_bases) {
      await this.knowledgeSelect.click()
      await this.page.getByRole('option', { name: kb }).click()
    }
    for (const skill of payload.skills) {
      await this.skillsSelect.click()
      await this.page.getByRole('option', { name: skill }).click()
    }
    await this.responseStyleSelect.click()
    await this.page.getByRole('option', { name: payload.response_style }).click()
    await this.marketCategorySelect.click()
    await this.page.getByRole('option', { name: payload.market_category }).click()
  }

  async saveAgent(): Promise<void> {
    await this.saveButton.click()
  }

  async createNewAgent(payload: AgentPayload): Promise<void> {
    await this.openCreateModal()
    await this.fillAgentForm(payload)
    await this.saveAgent()
  }

  async assertAgentInTable(agentName: string): Promise<void> {
    await this.page.locator('.ant-table-row').filter({ hasText: agentName }).waitFor({ state: 'visible' })
  }

  async assertAgentNotInTable(agentName: string): Promise<void> {
    const count = await this.page.locator('.ant-table-row').filter({ hasText: agentName }).count()
    if (count > 0) throw new Error(`Agent "${agentName}" still exists in table`)
  }

  async getTableRowCount(): Promise<number> {
    return this.page.locator('.ant-table-row').count()
  }
}
```

#### AgentChatPage POM

```typescript
// poms/AgentChatPage.ts
import { type Page, type Locator } from '@playwright/test'

export class AgentChatPage {
  readonly page: Page

  // Locators
  private readonly agentSelect = this.page.getByTestId('chat-agent-select')
  private readonly questionInput = this.page.getByTestId('chat-question-input')
  private readonly sendButton = this.page.getByTestId('chat-send-button')
  private readonly messageList = this.page.getByTestId('chat-message-list')

  constructor(page: Page) {
    this.page = page
  }

  // 语义动作
  async selectAgents(agentIds: string[]): Promise<void> {
    for (const id of agentIds) {
      await this.agentSelect.click()
      await this.page.getByRole('option', { name: new RegExp(id) }).click()
    }
  }

  async sendMessage(question: string): Promise<void> {
    await this.questionInput.fill(question)
    await this.sendButton.click()
  }

  async sendMessageWithEnter(question: string): Promise<void> {
    await this.questionInput.fill(question)
    await this.questionInput.press('Enter')
  }

  async assertEmptyMessages(): Promise<void> {
    await this.page.getByText('No messages yet').waitFor({ state: 'visible' })
  }

  async assertMessageVisible(messageId: string): Promise<void> {
    await this.page.getByTestId(`chat-message-${messageId}`).waitFor({ state: 'visible' })
  }

  async getMessageCount(): Promise<number> {
    return this.page.locator('[data-testid^="chat-message-"]').count()
  }

  async waitForResponse(): Promise<void> {
    // 等待发送按钮不再处于 loading 状态
    await this.sendButton.waitFor({ state: 'visible' })
    // 等待新消息出现
    await this.page.waitForFunction(
      (count) => document.querySelectorAll('[data-testid^="chat-message-"]').length > count,
      await this.getMessageCount()
    )
  }
}
```

#### AgentDetailDrawer POM

```typescript
// poms/AgentDetailDrawer.ts
import { type Page } from '@playwright/test'

export class AgentDetailDrawer {
  readonly page: Page

  // Locators
  private readonly drawer = this.page.getByTestId('agent-detail-drawer')
  private readonly detailPanel = this.page.getByTestId('agent-detail-panel')
  private readonly description = this.page.getByTestId('agent-detail-description')
  private readonly systemPrompt = this.page.getByTestId('agent-detail-system-prompt')

  constructor(page: Page) {
    this.page = page
  }

  async assertOpen(): Promise<void> {
    await this.drawer.waitFor({ state: 'visible' })
  }

  async assertClosed(): Promise<void> {
    await this.drawer.waitFor({ state: 'hidden' })
  }

  async close(): Promise<void> {
    await this.page.locator('.ant-drawer-close').click()
  }

  async getDescription(): Promise<string> {
    return this.description.innerText()
  }

  async getSystemPrompt(): Promise<string> {
    return this.systemPrompt.innerText()
  }
}
```

---

## 7. Agent 5: Choreographer — 用户旅程

### 7.1 旅程规划

由于本项目无 Feature Flags 和权限模型，状态空间较简单。Choreographer 基于业务流程规划用户旅程：

```json
{
  "version": "1.0",
  "journeys": [
    {
      "id": "j-market-browse",
      "name": "浏览 Agent 市场",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToMarket", "target": "AppLayout" },
        { "action": "assertAgentCardVisible", "target": "AgentMarketPage" },
        { "action": "viewAgentDetail", "target": "AgentMarketPage", "args": ["first-agent-id"] },
        { "action": "assertOpen", "target": "AgentDetailDrawer" },
        { "action": "close", "target": "AgentDetailDrawer" }
      ]
    },
    {
      "id": "j-market-search",
      "name": "搜索和筛选 Agent",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToMarket", "target": "AppLayout" },
        { "action": "searchAgents", "target": "AgentMarketPage", "args": ["testing"] },
        { "action": "filterByCategory", "target": "AgentMarketPage", "args": ["Testing"] },
        { "action": "searchAgents", "target": "AgentMarketPage", "args": ["nonexistent-agent-xyz"] },
        { "action": "assertEmptyState", "target": "AgentMarketPage" }
      ]
    },
    {
      "id": "j-config-create",
      "name": "创建新 Agent",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToConfiguration", "target": "AppLayout" },
        { "action": "openCreateModal", "target": "AgentConfigurationPage" },
        { "action": "fillAgentForm", "target": "AgentConfigurationPage", "args": ["valid-payload"] },
        { "action": "saveAgent", "target": "AgentConfigurationPage" },
        { "action": "assertAgentInTable", "target": "AgentConfigurationPage", "args": ["Test Agent"] }
      ]
    },
    {
      "id": "j-config-edit",
      "name": "编辑已有 Agent",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToConfiguration", "target": "AppLayout" },
        { "action": "openEditModal", "target": "AgentConfigurationPage", "args": ["existing-agent-id"] },
        { "action": "fillAgentForm", "target": "AgentConfigurationPage", "args": ["updated-payload"] },
        { "action": "saveAgent", "target": "AgentConfigurationPage" },
        { "action": "assertAgentInTable", "target": "AgentConfigurationPage", "args": ["Updated Agent"] }
      ]
    },
    {
      "id": "j-config-delete",
      "name": "删除 Agent",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToConfiguration", "target": "AppLayout" },
        { "action": "deleteAgent", "target": "AgentConfigurationPage", "args": ["target-agent-id"] },
        { "action": "assertAgentNotInTable", "target": "AgentConfigurationPage", "args": ["Deleted Agent"] }
      ]
    },
    {
      "id": "j-config-validation",
      "name": "表单验证 — 必填字段为空时禁止提交",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToConfiguration", "target": "AppLayout" },
        { "action": "openCreateModal", "target": "AgentConfigurationPage" },
        { "action": "saveAgent", "target": "AgentConfigurationPage" },
        { "action": "assertValidationErrors", "target": "AgentConfigurationPage" }
      ]
    },
    {
      "id": "j-chat-send",
      "name": "选择 Agent 并发送消息",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToChat", "target": "AppLayout" },
        { "action": "selectAgents", "target": "AgentChatPage", "args": [["agent-id-1"]] },
        { "action": "sendMessage", "target": "AgentChatPage", "args": ["What is testing?"] },
        { "action": "waitForResponse", "target": "AgentChatPage" },
        { "action": "assertMessageCountIncreased", "target": "AgentChatPage" }
      ]
    },
    {
      "id": "j-chat-multi-agent",
      "name": "选择多个 Agent 聊天",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToChat", "target": "AppLayout" },
        { "action": "selectAgents", "target": "AgentChatPage", "args": [["agent-id-1", "agent-id-2"]] },
        { "action": "sendMessage", "target": "AgentChatPage", "args": ["Compare testing approaches"] },
        { "action": "waitForResponse", "target": "AgentChatPage" }
      ]
    },
    {
      "id": "j-chat-validation",
      "name": "聊天验证 — 未选择 Agent 或空消息",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToChat", "target": "AppLayout" },
        { "action": "sendMessage", "target": "AgentChatPage", "args": ["Hello"] },
        { "action": "assertWarningVisible", "target": "AgentChatPage" }
      ]
    },
    {
      "id": "j-nav-switch",
      "name": "导航切换 — 在三个页面间切换",
      "permutation": { "role": "default" },
      "steps": [
        { "action": "navigateToMarket", "target": "AppLayout" },
        { "action": "assertPageVisible", "target": "AgentMarketPage" },
        { "action": "navigateToConfiguration", "target": "AppLayout" },
        { "action": "assertPageVisible", "target": "AgentConfigurationPage" },
        { "action": "navigateToChat", "target": "AppLayout" },
        { "action": "assertPageVisible", "target": "AgentChatPage" },
        { "action": "navigateToMarket", "target": "AppLayout" },
        { "action": "assertPageVisible", "target": "AgentMarketPage" }
      ]
    }
  ]
}
```

---

## 8. Agent 6: Assistant Director — 测试脚本

### 8.1 测试文件结构

```
tests/
├── navigation/
│   └── Nav-switch.spec.ts
├── market/
│   ├── Market-browse.spec.ts
│   └── Market-search.spec.ts
├── configuration/
│   ├── Config-create.spec.ts
│   ├── Config-edit.spec.ts
│   ├── Config-delete.spec.ts
│   └── Config-validation.spec.ts
└── chat/
    ├── Chat-send.spec.ts
    ├── Chat-multiAgent.spec.ts
    └── Chat-validation.spec.ts
```

### 8.2 示例测试脚本

#### Market-browse.spec.ts

```typescript
import { test, expect } from '@playwright/test'
import { AppLayout } from '../../poms/AppLayout'
import { AgentMarketPage } from '../../poms/AgentMarketPage'
import { AgentDetailDrawer } from '../../poms/AgentDetailDrawer'

test.describe('Agent Market — Browse', () => {
  test('user can browse agents and view detail', async ({ page }) => {
    const layout = new AppLayout(page)
    const market = new AgentMarketPage(page)
    const drawer = new AgentDetailDrawer(page)

    await page.goto('/')
    await layout.navigateToMarket()
    await market.assertAgentCardVisible('first-agent-id')

    // 点击第一个卡片的 View Detail
    const cards = page.locator('.ant-card')
    const firstCard = cards.first()
    await firstCard.locator('button:has-text("View Detail")').click()

    await drawer.assertOpen()
    const description = await drawer.getDescription()
    expect(description).toBeTruthy()

    await drawer.close()
    await drawer.assertClosed()
  })
})
```

#### Config-create.spec.ts

```typescript
import { test, expect } from '@playwright/test'
import { AppLayout } from '../../poms/AppLayout'
import { AgentConfigurationPage } from '../../poms/AgentConfigurationPage'

test.describe('Agent Configuration — Create', () => {
  test('user can create a new agent', async ({ page }) => {
    const layout = new AppLayout(page)
    const config = new AgentConfigurationPage(page)

    await page.goto('/')
    await layout.navigateToConfiguration()

    const initialCount = await config.getTableRowCount()

    await config.createNewAgent({
      name: 'Test QA Copilot',
      icon: '🤖',
      model: 'gpt-4.1',
      description: 'A test agent for QA automation',
      system_prompt: 'You are a QA assistant.',
      tools: ['playwright'],
      knowledge_bases: ['test-docs'],
      skills: ['web-testing'],
      response_style: 'concise',
      market_category: 'testing',
    })

    await config.assertAgentInTable('Test QA Copilot')
    const newCount = await config.getTableRowCount()
    expect(newCount).toBe(initialCount + 1)
  })
})
```

#### Chat-send.spec.ts

```typescript
import { test, expect } from '@playwright/test'
import { AppLayout } from '../../poms/AppLayout'
import { AgentChatPage } from '../../poms/AgentChatPage'

test.describe('Agent Chat — Send Message', () => {
  test('user can select agent and send message', async ({ page }) => {
    const layout = new AppLayout(page)
    const chat = new AgentChatPage(page)

    await page.goto('/')
    await layout.navigateToChat()
    await chat.assertEmptyMessages()

    // 选择第一个 Agent
    await chat.selectAgents(['first-agent-id'])
    await chat.sendMessage('What is automated testing?')
    await chat.waitForResponse()

    const messageCount = await chat.getMessageCount()
    expect(messageCount).toBeGreaterThan(0)
  })
})
```

---

## 9. Agent 7: Continuity Lead — 执行与自愈

### 9.1 执行报告模板

```json
{
  "version": "1.0",
  "timestamp": "2026-05-11T00:30:00Z",
  "totalTests": 10,
  "results": [
    { "journey": "j-market-browse", "status": "passed", "duration": "3.2s" },
    { "journey": "j-market-search", "status": "passed", "duration": "2.8s" },
    { "journey": "j-config-create", "status": "passed", "duration": "4.1s" },
    { "journey": "j-config-edit", "status": "passed", "duration": "3.9s" },
    { "journey": "j-config-delete", "status": "passed", "duration": "2.5s" },
    { "journey": "j-config-validation", "status": "passed", "duration": "1.8s" },
    { "journey": "j-chat-send", "status": "flaky", "duration": "8.2s", "note": "API 响应时间不稳定" },
    { "journey": "j-chat-multi-agent", "status": "flaky", "duration": "9.1s", "note": "多 Agent 响应偶超时" },
    { "journey": "j-chat-validation", "status": "passed", "duration": "1.5s" },
    { "journey": "j-nav-switch", "status": "passed", "duration": "2.1s" }
  ],
  "summary": {
    "passed": 8,
    "flaky": 2,
    "failed": 0,
    "passRate": "80%",
    "adjustedPassRate": "100%"
  },
  "classification": [],
  "autoHealActions": []
}
```

### 9.2 自愈场景示例

**场景：开发者将 `agent-create-button` 的 data-testid 改名为 `add-agent-button`**

```
1. 测试失败 → Config-create.spec.ts 中 getByTestId('agent-create-button') 找不到元素
2. 失败分类 → "Test Update Need"（源码有意变更）
3. 检测变更 → git diff 发现 data-testid 从 agent-create-button 改为 add-agent-button
4. 更新元素参考 → locator-catalog.json 中更新对应条目
5. 生成测试补丁 → AgentConfigurationPage POM 中更新 locator
6. 应用补丁 → this.createButton = this.page.getByTestId('add-agent-button')
7. 重新执行测试 → 通过 ✅
```

---

## 10. 最终元素库总览

### 10.1 全部交互元素清单

| # | 组件 | 元素类型 | 角色 | data-testid | 优先级 1 定位器 |
|---|------|----------|------|-------------|----------------|
| 1 | AppLayout | menu-item | nav-market | `nav-agent-market` | `getByTestId('nav-agent-market')` |
| 2 | AppLayout | menu-item | nav-configuration | `nav-agent-configuration` | `getByTestId('nav-agent-configuration')` |
| 3 | AppLayout | menu-item | nav-chat | `nav-agent-chat` | `getByTestId('nav-agent-chat')` |
| 4 | AppLayout | div | brand | `app-brand` | `getByTestId('app-brand')` |
| 5 | AgentMarketPage | section | page | `agent-market-page` | `getByTestId('agent-market-page')` |
| 6 | AgentMarketPage | input | search-input | `agent-market-search-input` | `getByTestId('agent-market-search-input')` |
| 7 | AgentMarketPage | select | category-select | `agent-market-category-select` | `getByTestId('agent-market-category-select')` |
| 8 | AgentMarketPage | button | search-button | `agent-market-search-button` | `getByTestId('agent-market-search-button')` |
| 9 | AgentMarketPage | card | agent-card | `agent-market-card-${id}` | `getByTestId('agent-market-card-${id}')` |
| 10 | AgentMarketPage | button | view-detail | `agent-market-view-detail-${id}` | `getByTestId('agent-market-view-detail-${id}')` |
| 11 | AgentConfigurationPage | section | page | `agent-configuration-page` | `getByTestId('agent-configuration-page')` |
| 12 | AgentConfigurationPage | button | create | `agent-create-button` | `getByTestId('agent-create-button')` |
| 13 | AgentConfigurationPage | table | agent-table | `agent-configuration-table` | `getByTestId('agent-configuration-table')` |
| 14 | AgentConfigurationPage | span | agent-name | `agent-config-name-${id}` | `getByTestId('agent-config-name-${id}')` |
| 15 | AgentConfigurationPage | button | edit | `agent-edit-button-${id}` | `getByTestId('agent-edit-button-${id}')` |
| 16 | AgentConfigurationPage | button | delete | `agent-delete-button-${id}` | `getByTestId('agent-delete-button-${id}')` |
| 17 | AgentConfigurationPage | form | editor-form | `agent-editor-form` | `getByTestId('agent-editor-form')` |
| 18 | AgentConfigurationPage | input | name-input | `agent-name-input` | `getByTestId('agent-name-input')` |
| 19 | AgentConfigurationPage | input | icon-input | `agent-icon-input` | `getByTestId('agent-icon-input')` |
| 20 | AgentConfigurationPage | select | model-select | `agent-model-select` | `getByTestId('agent-model-select')` |
| 21 | AgentConfigurationPage | textarea | description | `agent-description-input` | `getByTestId('agent-description-input')` |
| 22 | AgentConfigurationPage | textarea | system-prompt | `agent-system-prompt-input` | `getByTestId('agent-system-prompt-input')` |
| 23 | AgentConfigurationPage | select | tools-select | `agent-tools-select` | `getByTestId('agent-tools-select')` |
| 24 | AgentConfigurationPage | select | knowledge-select | `agent-knowledge-select` | `getByTestId('agent-knowledge-select')` |
| 25 | AgentConfigurationPage | select | skills-select | `agent-skills-select` | `getByTestId('agent-skills-select')` |
| 26 | AgentConfigurationPage | select | response-style | `agent-response-style-select` | `getByTestId('agent-response-style-select')` |
| 27 | AgentConfigurationPage | select | market-category | `agent-market-category-form-select` | `getByTestId('agent-market-category-form-select')` |
| 28 | AgentConfigurationPage | button | save | `agent-save-button` | `getByTestId('agent-save-button')` |
| 29 | AgentChatPage | section | page | `agent-chat-page` | `getByTestId('agent-chat-page')` |
| 30 | AgentChatPage | select | agent-select | `chat-agent-select` | `getByTestId('chat-agent-select')` |
| 31 | AgentChatPage | div | message-list | `chat-message-list` | `getByTestId('chat-message-list')` |
| 32 | AgentChatPage | list-item | message | `chat-message-${id}` | `getByTestId('chat-message-${id}')` |
| 33 | AgentChatPage | input | question-input | `chat-question-input` | `getByTestId('chat-question-input')` |
| 34 | AgentChatPage | button | send | `chat-send-button` | `getByTestId('chat-send-button')` |
| 35 | AgentDetailDrawer | drawer | detail-drawer | `agent-detail-drawer` | `getByTestId('agent-detail-drawer')` |
| 36 | AgentDetailDrawer | div | detail-panel | `agent-detail-panel` | `getByTestId('agent-detail-panel')` |
| 37 | AgentDetailDrawer | p | description | `agent-detail-description` | `getByTestId('agent-detail-description')` |
| 38 | AgentDetailDrawer | span | system-prompt | `agent-detail-system-prompt` | `getByTestId('agent-detail-system-prompt')` |

### 10.2 产物清单

| 产物 | 文件 | 描述 |
|------|------|------|
| 组件注册表 | `component-registry.json` | 6 个组件，38 个交互元素 |
| testid 注入 | `testid-injections.json` | 5 处注入（从 82% → 100% 覆盖） |
| 定位器目录 | `locator-catalog.json` | 19 个定位器优先级链 |
| POM 类 | `poms/*.ts` | 5 个 POM 类（AppLayout, AgentMarketPage, AgentConfigurationPage, AgentChatPage, AgentDetailDrawer） |
| 用户旅程 | `journeys.json` | 10 条用户旅程 |
| 测试脚本 | `tests/*.spec.ts` | 10 个测试文件，覆盖全部三大业务 |
| 执行报告 | `execution-report.json` | 测试结果和自愈记录 |

### 10.3 本项目的特殊性分析

| 特性 | 本项目情况 | 对 Mode B 的影响 |
|------|-----------|-----------------|
| **data-testid 覆盖率** | 极高（82%） | ✅ Stage Manager 几乎不需要注入，定位器直接可用 |
| **Feature Flags** | 无 | ✅ 状态空间简单，无需排列组合 |
| **权限模型** | 无 | ✅ 所有用户看到相同 UI |
| **路由方式** | 状态路由（useState） | ⚠️ 无法用 URL 直接导航到特定页面，需通过侧边栏点击 |
| **UI 库** | Ant Design 5 | ⚠️ Ant Design 组件的 DOM 结构复杂，需注意内部选择器 |
| **API 依赖** | 7 个 API 端点 | ⚠️ 测试需要 Mock API 或启动后端服务 |
| **表单复杂度** | 10 个字段，含多选 | ⚠️ AgentConfigurationPage 的表单测试较复杂 |
| **异步行为** | 多处 useEffect + async | ⚠️ 需要等待 API 响应，可能需要调整超时 |

---

**文档版本**: v1.0.0  
**扫描引擎**: Mode B Component-Aware Pipeline (模拟)  
**扫描时间**: 2026-05-11