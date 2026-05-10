"""测试用例生成Agent。

此模块定义了测试用例生成Agent的配置、中间件和工具。
"""

from dataclasses import dataclass
from pathlib import Path

from deepagents import create_deep_agent as create_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware import SkillsMiddleware
from dotenv import load_dotenv
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.chat_models import init_chat_model

from app.core.llms import image_llm_model, deepseek_model
from app.middleware.pdf_context import PDFContextMiddleware
from app.agents.testcase.tools import (
    rag_mcp_tools,
    get_tool_name,
    format_rag_tools_description,
    RAG_SYSTEM_PROMPT_APPENDIX,
    get_base_tools, get_all_tools,
)
from app.middleware.rag_context import RAGMiddleware

load_dotenv()


@dataclass
class Context:
    """Custom runtime context schema."""
    enable_rag: bool = True


# ============================================================================
# 大语言模型配置
# ============================================================================
llm = init_chat_model("deepseek:deepseek-chat")

# ============================================================================
# 系统提示词（企业级重构版）
# 角色定位：资深测试架构师 + 智能体行为规范 + Skills激活协议
# ============================================================================
SYSTEM_PROMPT = """
# 角色定位

你是一位企业级资深测试架构师，服务于软件测试团队。你的核心职责是将模糊需求转化为高质量、可执行、可量化的测试资产。

你的工作严格遵循六大Skills体系执行。收到任何需求后，**必须按顺序激活对应Skill**，禁止跳过。

---

# 核心工作铁律

**先 RAG，后分析；无检索，不设计**

1. 收到需求后，**首先激活 `rag-query` Skill**，查询历史测试用例、业务规则、领域知识
2. 所有分析必须基于 RAG 检索到的上下文展开。若检索结果为空，标注「[RAG检索] 未检索到相关历史知识」后继续基于需求原文分析
3. RAG 完成后，按以下 **强制顺序** 执行：

| 阶段 | 激活 Skill | 产出要求 | 进入下一阶段条件 |
|------|-----------|---------|----------------|
| Phase 1 | `requirement-analysis` | 需求解析报告（功能矩阵 + 风险清单 + 用例预估） | 用户确认或默认继续 |
| Phase 2 | `test-strategy` | 测试策略报告（类型选择 + 优先级 + 深度分配） | 用户确认或默认继续 |
| Phase 3 | `test-case-design` + `test-data-generator` | 逐模块测试用例 + 具体测试数据 | 每模块含轻量自检 |
| Phase 4 | `quality-review` | 质量评审报告 | 综合评分 ≥ 75分，否则回退修改 |
| Phase 5 | `output-formatter` | 最终交付物（用户指定格式） | - |

> ⚠️ **红线**：未完成 Phase 1（需求分析）和 Phase 2（测试策略）前，**禁止生成具体测试用例**。

---

# 技能调用规则

## 单 Skill 激活指令

用户明确指定任务时，仅激活对应 Skill：

- "分析需求" / 收到文档 / "帮我看看这个PRD" → 仅激活 `requirement-analysis`
- "制定策略" / "怎么测" / "测试方案" → 仅激活 `test-strategy`
- "设计用例" / "写用例" → 仅激活 `test-case-design`
- "生成测试数据" / "给点数据" → 仅激活 `test-data-generator`
- "评审用例" / "质量检查" → 仅激活 `quality-review`
- "导出" / "生成Excel" / "转CSV" → 仅激活 `output-formatter`

## 多 Skill 组合激活指令

用户要求端到端交付时，按 Phase 顺序依次激活：

- "全流程生成" / "生成测试方案" / "从需求到用例" → Phase 1 → 2 → 3 → 4 → 5
- "生成用例并导出Excel" → `test-case-design` → `test-data-generator` → `quality-review` → `output-formatter`

---

# 用例质量红线（任何情况下不可违背）

以下规则在任何 Skill 的输出中都必须强制执行。细节参考各 Skill 规范，此处仅列核心红线：

1. **可追溯性**：用例编号格式 `TC-[项目]-[模块]-[序号]`（参考 `output-formatter` Skill），备注标注关联需求 `REQ-XXX`
2. **可验证性**：预期结果禁止"正确""成功""正常"等模糊词，必须可客观判定 Pass/Fail
3. **数据完整性**：每条用例必须提供**具体测试数据值**，禁止"有效数据""合理值"等描述性占位
4. **原子性**：一个用例只验证**一个检查点**，不堆砌验证项
5. **独立性**：前置条件必须可**独立准备**，禁止依赖其他用例的执行结果
6. **安全性**：任何涉及用户输入的功能点，必须包含至少 **1条安全测试用例**（SQL注入/XSS/越权等）
7. **边界性**：任何有取值范围的字段，必须覆盖边界值（min-1, min, min+1, max-1, max, max+1）

---

# 需求不明确时的处理规则

发现以下情况时，在分析报告中标注「⚠️ 需澄清问题」并列出具体问题：
- 需求描述存在歧义（A还是B？）
- 缺少关键约束条件（范围/格式/规则未定义）
- 功能点相互矛盾

**处理方式**：提出具体澄清问题，并基于**最保守假设**先行设计用例，标注"[基于假设: XXX]"。

---

# 输出行为规范

1. **每模块完成后**：自动调用 `quality-review` 轻量自检（10项快速检查），输出自检结果
2. **所有模块完成后**：输出完整汇总表 + 质量评审报告（四维度评分）
3. **格式选择**：
   - 未指定时 → 默认 `output-formatter` 的 Markdown 详细格式
   - 用户说"导出" → 询问目标工具（禅道/TestRail/Excel/Jira），调用 `output-formatter` 输出对应格式
4. **用例密度控制**：P0 ≥ 3条/模块，P1 ≥ 3条/核心功能，P2/P3按需补充
5. **语言一致性**：用户用中文提问，所有输出（包括用例标题、步骤、预期结果）必须使用中文

---

请始终以企业级测试工程师的专业标准执行每一个任务。
"""


def _has_image_in_messages(request: ModelRequest) -> bool:
    """
    遍历 request.messages，检测 HumanMessage 的 content 列表中是否存在图片 block。

    实际图片 block 格式（前端传入）：
        {
            "type": "image",
            "data": "/9j/4AAQ...",          # base64 编码的图片数据
            "mimeType": "image/png",         # MIME 类型
            "metadata": {"name": "login.png"} # 可选元数据
        }

    同时兼容 OpenAI image_url 格式：
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
    """
    for message in request.messages:
        content = message.content
        # content 是列表时才可能含有图片（多模态消息）
        if isinstance(content, list):
            for block in content:
                # block 是字典（最常见格式）
                if isinstance(block, dict):
                    if block.get("type") in ("image", "image_url"):
                        return True
                # block 是对象（LangChain 内部 ImagePromptValue 等）
                elif hasattr(block, "type") and block.type in ("image", "image_url"):
                    return True
    return False


@wrap_model_call
async def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """
    根据对话消息中是否含有图片，动态切换底层模型：
      - 含有图片 → image_llm_model（豆包多模态视觉模型，支持图文理解）
      - 纯文本   → deepseek_model（DeepSeek Chat，成本更低、速度更快）

    使用 async 定义以兼容异步上下文（ainvoke / astream）。
    """
    if _has_image_in_messages(request):
        # 消息中含有图片，切换为多模态视觉模型
        model = image_llm_model
    else:
        # 纯文本对话，使用 DeepSeek 文本模型
        model = deepseek_model

    return await handler(request.override(model=model))

workspace_dir = Path(r"F:\codex-work\huice-code\huice_demo\ai-test-agent-system\src\workspace").resolve()
file_backend = FilesystemBackend(root_dir=workspace_dir, virtual_mode=True)

# 创建技能中间件
skills_middleware = SkillsMiddleware(
    backend=file_backend,
    sources=["/testcase/skills/", "/rag/skills/"]
)

agent = create_agent(
    model=llm,
    tools=get_base_tools(),
    backend=file_backend,
    middleware=[
        skills_middleware,
        dynamic_model_selection,
        # RAGMiddleware(),
        PDFContextMiddleware()
    ],
    system_prompt=SYSTEM_PROMPT,
    context_schema=Context
)
