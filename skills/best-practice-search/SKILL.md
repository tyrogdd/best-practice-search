---
name: best-practice-search
description: 跨平台检索编排 Skill。用于需要多信源交叉验证的工具选型、最佳实践与踩坑调研、一手出处溯源，以及可复用图文/视频素材查找；覆盖中英文社区、技术论坛、论文库、模型库与媒体平台。不适用于单点简单事实查询或单一官方文档速查。Cross-platform research orchestrator for tool selection, real-world workflows, tradeoffs, primary-source verification, and reusable media across EN/ZH communities, papers, and repos (not for simple single-fact lookups).
license: MIT
---

# 跨平台检索编排

本 Skill 作为**检索编排层**，负责任务定级、按信源拆题、查询路由、动态时效判断、证据核验与缺口汇总。实际搜索、原文读回和媒体获取由当前环境已有工具（网页搜索、浏览器、CLI、API、MCP）、内置脚本 [public_search.py](scripts/public_search.py) 或专用的**信源执行 Skill** 完成。

**按需读取参考文件（节省上下文）**：`Quick` 模式无需通读全部参考文件，直接检索并在需要特定站点技巧时再查对应条目；`Standard` / `Deep` 模式再按需读取 [检索路由](references/source-routing.md)、[信源目录](references/sources.md)、[信源访问手册](references/platform-access-playbook.md) 与 [输出模板](references/output-template.md)。运行环境清单见 `references/tool-profiles/`（Codex 参考 [codex.md](references/tool-profiles/codex.md)，通用环境参考 [generic-web-cli.md](references/tool-profiles/generic-web-cli.md)，其他环境可复制 [template.md](references/tool-profiles/template.md)）。

## 1. 先定深度与检索预算

根据任务复杂度先选定模式，避免 20+ 信源盲目通扫：

- **Quick（快速核验 / 已知对象溯源）**：选 1–2 个最高匹配信源，最多 2–3 次检索；找到一手原页并确认对象、版本或出处即收束。
- **Standard（默认：工具选型 / 最佳实践 / 实操调研）**：按任务挑 3–4 个互补信源，每站 1–2 组精准查询；关键方案有实证、核心分歧已追查即收束。
- **Deep（深度调研 / 用户指定多平台）**：中英文双语交叉检索，按平台分配投入重点并记录完整覆盖矩阵、复跑搜索式与访问缺口。

## 2. 按信源拆题与执行

1. **明确约束与证据需求**。拆清要找的对象、约束条件（地区、版本、成本、兼容性、可编辑性、许可）及所需证据层级（原帖、评论、代码、论文图、视频片段或源文件）。用 `case study`、`workflow`、`migration`、`limitations`、`gotchas` 或 `实测`、`踩坑`、`平替` 替换宽泛的 `best practice`。
2. **按任务选信源并构造本地化查询**。用户指定站点、浏览器或账号范围时优先遵循；否则依据 [检索路由](references/source-routing.md#按任务选择首选信源) 挑选互补站点，中英文社区分别使用各自惯用词。
3. **优先用已有入口与免登录路径执行**。对 HN、arXiv、Hugging Face、Lobste.rs、Stack Exchange、Wikimedia Commons 可直接运行 `python3 scripts/public_search.py` 获取带日期与链接的结构化结果；其余平台优先使用当前会话已可用的搜索、CLI、连接器或浏览器（参考 [信源访问手册](references/platform-access-playbook.md)）。
   - **能力发现旁路（按需触发，非默认步骤）**：仅当用户明确要求寻找新工具，或某**核心必需信源**在所有已有入口均失败且用户同意投入额外步骤时，才去 GitHub / Skill 目录查找并静态审查专用信源执行 Skill。详见 [检索路由](references/source-routing.md#能力发现旁路按需触发)。
4. **原文核验与登录交接**。搜索摘要仅作检索线索，引用具体事实、日期、参数、图号或许可前须读回原页，并标注实际读取层级（`原文已读` / `部分已读` / `仅索引可见` / `访问受限`）。遇到登录墙挡住必需内容时，暂停并交接给用户登录或具备该会话的一方；用户放弃或不可达时保留覆盖缺口，不编造内容。

## 3. 动态时效与证据分级

- **动态滑动时间窗**：以执行当天的系统日期 `T` 为基准，而非固定年份：
  - **快迭代领域**（AI、Agent、MCP、模型评测、前端/云原生工具）：优先检索近 12 个月（`T - 12 个月` 至今）的现行资料；12–24 个月资料作补充并核对新版是否已变更；超过 24 个月仅作背景或历史演进。
  - **慢迭代领域**（经典架构、学术方法、基础协议、统计规范）：按是否仍为当前主流版本或被官方取代判断，不机械按年份降权。
  - 用户明确指定时间范围时按用户要求执行。
- **离散证据分级（用于排序与筛选）**：
  - **Tier 1（高可信一手）**：官方文档/源码/发行说明、论文原件、带可复现代码或源文件的实测。
  - **Tier 2（有效社区实证）**：含明确版本、场景、收益与失败条件的亲历帖、高价值评论或实操演示。
  - **Tier 3（仅作线索）**：二手转述、营销推广、仅索引摘要可见、或日期/版本未核验的材料。
  - 详细判断与去重规则见 [检索路由](references/source-routing.md#动态时效与证据分级)。

## 4. 交付与示范沉淀

- **结构化交付**：按 [输出模板](references/output-template.md) 交付。先给结论、选项对比与关键避坑/验收项，再附带定位点（原始链接、有效日期、版本/图号/时间戳、读取层级）的来源清单与覆盖缺口。
- **沉淀用户示范（显式触发）**：当用户要求按其示范路径执行或要求“记住这次搜法”时，记录实际使用的信源、查询式、换站时机与筛选标准。示范结束后，将可复跑路径写入用户工作区或指定路径（默认 `./.search-playbooks/<topic>.md`），**不要直接修改已安装的 Skill 目录本体**。
