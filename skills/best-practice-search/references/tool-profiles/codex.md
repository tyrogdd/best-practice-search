# Codex 检索工具清单

配合 [跨平台检索编排 Skill](../../SKILL.md) 使用。下表逐项对应 [信源目录](../sources.md) 的 21 个信源标识，只记录**可复用的入口策略与切换条件**，不混入单次任务日志。每次运行以当前会话实际可调用的工具和用户指定入口为准。

## 中文社区与内容平台

| 信源标识 | 默认入口 | 备用入口与交接条件 |
| --- | --- | --- |
| `xiaohongshu` | `@Chrome`（用户已登录会话）站内搜笔记与评论 | 无登录会话时用网页搜索找标题线索并标 `仅索引可见`；遇登录页暂停交接 |
| `zhihu` | 网页搜索限定 `site:zhihu.com/question` 或 `site:zhuanlan.zhihu.com`，再读原文 | 遇登录弹窗遮挡完整回答或配图时，切换 `@Chrome` 回读 |
| `wechat-mp` | 网页搜索限定 `site:mp.weixin.qq.com` 发现链接，直接抓取公开正文 | 遇多篇转载时核对原创主体；仅能看摘要时转浏览器核对 |
| `juejin` | 网页搜索限定 `site:juejin.cn`，直接读正文与评论 | 页面需交互展开评论时用浏览器补读 |
| `sspai` | 网页搜索限定 `site:sspai.com` 或站内搜，直读免费文章 | 遇付费专栏标为 `访问受限（付费）`，不绕过付费墙 |
| `linux-do` | 网页搜索限定 `site:linux.do`，再读主题页 | 需读登录区或长串关键楼层时，切换 `@Chrome` 补读 |
| `v2ex` | 网页搜索限定 `site:v2ex.com/t/`，回读主题、附言与回复 | 限流或页面不完整时改用浏览器查看原节点与完整楼层 |
| `nodeseek` | 浏览器站内搜或网页搜索限定 `site:nodeseek.com/post-` | 回原帖核对时间、地区与完整回复 |
| `tieba` | `@Chrome` 站内搜目标贴吧与帖子 | 用 `site:tieba.baidu.com/p/` 加领域消歧词补查，再到原帖核对楼层 |

## 英文社区与实时动态

| 信源标识 | 默认入口 | 备用入口与交接条件 |
| --- | --- | --- |
| `x` | `@Chrome`（已登录会话）查主贴、thread 与作者动态 | 无会话时用网页搜索找公开线索并记录覆盖缺口，沿外链回查 GitHub/博客原文 |
| `hacker-news` | 内置 `scripts/public_search.py hn`（Algolia 公开 API） | 网页搜索限定 `site:news.ycombinator.com` 或浏览器查原讨论并追原始文章 |
| `reddit` | 网页搜索限定 `site:reddit.com/r/<sub>`，读正文与评论 | 触发人机验证或登录墙时切换已登录 `@Chrome` 或标 `访问受限` |
| `lobsters` | 内置 `scripts/public_search.py lobsters`（公开 `.json`） | 浏览器或抓取工具读讨论页及原始博文 |
| `stackoverflow` | 内置 `scripts/public_search.py se`（Stack Exchange API，含各 SE 子站） | 直读高赞与最新回答，重点核对评论区版本失效提示 |

## 项目、选型与学术模型

| 信源标识 | 默认入口 | 备用入口与交接条件 |
| --- | --- | --- |
| `github` | GitHub 连接器或 `gh` CLI 读 README、源码、Issues 与 Releases | 浏览器做仓库发现与 PR/Discussions 原页核对 |
| `alternativeto` | 网页搜索限定 `site:alternativeto.net/software` 发现候选 | 拿到竞品后立即切 `github` 或官网核实维护状态与定价 |
| `arxiv` | 内置 `scripts/public_search.py arxiv` + `arxiv.org/html/<id>` 读正文与图表 | 无 HTML 版时读摘要页及 PDF，并查官方代码链接 |
| `huggingface` | 内置 `scripts/public_search.py hf` 与 Model Card 原文直读 | 浏览器查看 Spaces Demo 与 Discussions；Gated 模型按授权范围处理 |

## 图片、视频与合规素材

| 信源标识或任务 | 默认入口 | 备用入口与交接条件 |
| --- | --- | --- |
| `bilibili` | 浏览器站内搜视频/专栏，核对分 P、简介与可用字幕 | 域名限定搜索补查；未读字幕或未看画面时标 `仅核对原页与简介` |
| `youtube` | 优先字幕/转写工具读逐字稿，结合浏览器查原页与章节 | 用作者官网/会议页补查讲稿；未读字幕时标 `仅核对原页与简介` |
| `wikimedia-commons` | 内置 `scripts/public_search.py wikimedia`（自动取许可与 SVG 源链） | 浏览器核对单图视觉内容、作者与 License 栏 |
| 公开文档与图片溯源 | 当前会话网页搜索与读取工具；视觉溯源用浏览器图片检索/Lens | 必须追回原始论文、维护者文档或素材许可页 |

## Codex 环境配置提示

- 项目专用 MCP 注册在受信任项目的 `.codex/config.toml`；跨项目共享配置放在 `~/.codex/config.toml`。 [Codex MCP 文档](https://learn.chatgpt.com/docs/extend/mcp?surface=cli#connect-codex-to-an-mcp-server)
- 委派 sub-agent 前，先在父会话用 `codex mcp list` 核对注册，并确认是否需要访问已有浏览器会话。 [Sub-agent 配置说明](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
- 切换到其他 Agent 时，优先查看 [通用 Web/CLI 清单](generic-web-cli.md) 或复制 [工具清单模板](template.md)。
