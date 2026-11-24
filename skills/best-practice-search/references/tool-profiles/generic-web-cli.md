# 通用 Web / CLI 检索工具清单

适用于 **Claude Code、Antigravity、Cursor、Gemini CLI 及任意具备网页搜索、HTTP 抓取、Shell CLI 或独立浏览器子 Agent 的环境**。本清单不绑定特定客户端语法，按能力分层选入口。

## 能力映射总览

| 能力层级 | 典型可用工具 | 覆盖信源标识 | 使用原则 |
| --- | --- | --- | --- |
| **1. 公开 API / CLI（最快、字段最准）** | 内置 [public_search.py](../../scripts/public_search.py)、`gh` CLI、GitHub MCP | `github` · `hacker-news` · `arxiv` · `huggingface` · `lobsters` · `stackoverflow` · `wikimedia-commons` | 优先运行 `python3 scripts/public_search.py` 或 `gh`（见 [信源访问手册](../platform-access-playbook.md#公开-api-与-cli-优先信源)），直接取发布日期、版本、源码和许可元数据 |
| **2. 网页搜索 + 原文抓取** | `search_web` / `WebSearch`、`WebFetch` / HTTP fetch | `juejin` · `sspai` · `wechat-mp` · `v2ex` · `nodeseek` · `linux-do` · `zhihu` · `alternativeto` · `reddit` | 先用 `site:` 算子精准发现候选，再用 Fetch 读回正文；若仅拿到摘要或被弹窗/验证拦截，按实际层级标注 |
| **3. 浏览器子 Agent / 独立浏览器** | 内置 Browser Subagent、Playwright/Chrome DevTools MCP | `bilibili` · `youtube` · `tieba` · `zhihu` · `linux-do` · 公开动态页与图片检查 | 用于需要渲染 JS、查看图文布局、检查页面截图或用户指定打开网页的场景 |
| **4. 需用户登录会话的受限信源** | 带登录态的可见浏览器（需用户交接） | `xiaohongshu` · `x` · 部分 `zhihu` / `linux-do` / `reddit` 讨论 | 无登录态时**不强行绕过认证或人机验证**；先用外部搜索找公开线索，需要正文时交接用户登录，或直接记录覆盖缺口 |
| **5. 媒体字幕与转写（按环境可选）** | `yt-dlp`、字幕/转写 CLI 或视频 MCP | `youtube` · `bilibili` | 有工具时优先取字幕/逐字稿并定位时间戳；无工具时如实标注 `仅核对原页与简介` |

## 无头环境（无浏览器）默认降级策略

当运行环境**只有终端 + 网页搜索 + HTTP 抓取**时：
1. **主力信源自动向公开友好站倾斜**：优先组合 `github` + `hacker-news` / `lobsters` + `arxiv` / `huggingface` + `juejin` / `wechat-mp` / `v2ex`。
2. **强登录墙信源透明处理**：若任务要求查 `xiaohongshu` 或 `x`，先通过网页搜索收集可见标题与外链线索（标为 `仅索引可见`），同时向用户说明需要带登录态的浏览器才能回读原文与评论，或请用户提供导出材料继续核验。
3. **验证一次即复用**：进入新环境时，先检查 `gh`、`curl`、网页搜索与浏览器工具哪些实际可用，确认后再按 [检索路由](../source-routing.md) 拆题执行。
