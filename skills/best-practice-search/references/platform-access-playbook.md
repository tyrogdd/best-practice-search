# 信源访问手册（免登录与降级速查）

本手册只使用**官方公开 API、标准 CLI、公开网页结构与正常搜索引擎语法**。遇到登录墙、人机验证或付费墙时，**不得绕过访问控制或反爬校验**，应按登录交接规则处理或如实记录覆盖缺口。

## 公开 API 与 CLI 优先信源

这些信源对无头环境、CLI 或 HTTP 抓取最友好，应优先使用结构化接口而非仅看搜索摘要。除 `github`（推荐用 `gh` CLI）外，其余 6 个信源均已封装进零依赖脚本 [public_search.py](../scripts/public_search.py)，可直接运行获取带精确日期、链接和许可元数据的 Markdown 或 JSON 结果：

```sh
# 常用示例（--format json 可切换结构化输出，--limit 控制条数）
python3 scripts/public_search.py hn "mermaid draw.io diagram" --since 2025-11-01 --min-points 20 --limit 5
python3 scripts/public_search.py arxiv "agentic workflow evaluation" --sort submitted --limit 5
python3 scripts/public_search.py hf "qwen3" --kind models --sort downloads --limit 5
python3 scripts/public_search.py lobsters --tag practices --limit 5
python3 scripts/public_search.py se "matplotlib publication svg" --site stackoverflow --sort votes --limit 5
python3 scripts/public_search.py wikimedia "microkernel architecture" --svg-only --limit 5
```

| 信源标识 | 推荐免登录入口 | 关键用法与返回值 |
| --- | --- | --- |
| `github` | `gh` CLI 或 GitHub REST API (`api.github.com`) | `gh search repos` / `gh search issues` / `gh release list -R owner/repo` 直接取版本日期、源码路径与真实讨论；无 `gh` 时用 `https://api.github.com/repos/<owner>/<repo>/releases/latest` |
| `hacker-news` | HN Search by Algolia 公开 API | `https://hn.algolia.com/api/v1/search?query=<q>&tags=story`（按相关性）或 `search_by_date`（按时间），直接返回精确时间戳、分数、评论数与讨论 ID |
| `arxiv` | arXiv 公开 API + HTML 原文 | API：`https://export.arxiv.org/api/query?search_query=all:<q>&sortBy=submittedDate&sortOrder=descending`；读正文与图表优先访问 `https://arxiv.org/html/<id>` |
| `huggingface` | Hugging Face Hub 公开 API | `https://huggingface.co/api/models?search=<q>&sort=downloads`、`https://huggingface.co/api/daily_papers`；Model Card 原文可直读 `https://huggingface.co/<repo>/raw/main/README.md` |
| `lobsters` | 站内公开 JSON | `https://lobste.rs/t/<tag>.json` 或 `https://lobste.rs/s/<id>.json`，直接获得原链接、日期与评论树 |
| `stackoverflow` | Stack Exchange 公开 API | `https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q=<q>&site=stackoverflow`（可换 `tex`、`stats`、`unix` 等子站） |
| `wikimedia-commons` | MediaWiki 公开 API | `https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srsearch=<q>&format=json` 查 `File:` 条目，再用 `imageinfo&iiprop=url\|extmetadata` 核对许可与作者 |

## 搜索引擎限定与降级技巧

当站内搜索受限、或无浏览器会话时，按站点特点调整搜索算子：

| 信源标识 | 推荐搜索算子 / 降级方式 | 常见失效场景与处理 |
| --- | --- | --- |
| `reddit` | `site:reddit.com/r/<subreddit> <query>`；公开帖可尝试原 URL 后加 `.json` 读结构化文本 | 网页端频繁触发人机验证时，切回已登录浏览器或仅记索引线索并标明缺口 |
| `zhihu` | 问答用 `site:zhihu.com/question <query>`，长文用 `site:zhuanlan.zhihu.com <query>` | 遇登录弹窗遮挡正文时，改用已登录浏览器交接 |
| `wechat-mp` | 优先搜索引擎 `site:mp.weixin.qq.com <query>` 或搜狗微信发现链接，再直接抓取公开正文 | 注意过滤多个转载号，优先保留显示“原创”或官方主体的链接 |
| `juejin` / `sspai` | `site:juejin.cn <query>`、`site:sspai.com <query>` 后直接回读原页 | `sspai` 付费专栏只可读试读部分，遇到即标为 `访问受限（付费）` |
| `linux-do` / `v2ex` / `nodeseek` | `site:linux.do`、`site:v2ex.com/t/`、`site:nodeseek.com/post-` 精准限定帖子页 | 部分板块需登录才可见完整回复；已读主题但缺关键楼层时如实标注 |
| `alternativeto` | `site:alternativeto.net/software <name>` 快速取竞品名录 | 取到候选名后，立即转 `github` 或官网核对是否停更与最新定价 |
| `tieba` | `site:tieba.baidu.com/p/ <专业消歧词> <问题词>` | 务必带领域词排除同名游戏吧/水贴 |

## 强登录墙与富媒体信源策略

| 信源标识 | 核心瓶颈 | 推荐执行方式 |
| --- | --- | --- |
| `xiaohongshu` | 强登录态、会话参数时效短 | 有用户已登录浏览器时站内搜索并直读图文与评论，记录无参笔记 ID 与原题；无会话时仅用外部搜索引擎搜 `小红书 <关键词>` 获取公开线索，不伪造未读笔记细节 |
| `x` | 强登录态、单推文碎片化 | 有已登录浏览器或专用入口时查主贴与 thread，并沿外链回查 GitHub/官网；无会话时标记缺口，改由 `hacker-news`/`github`/`reddit` 交叉补位 |
| `youtube` | 仅看简介容易漏掉关键演示与参数 | 优先检查环境是否具备字幕/转写能力（如 `yt-dlp --skip-download --write-auto-sub` 或视频转写工具）读取逐字稿并定位时间戳；若未读字幕或未看画面，交付时必须标注 `仅核对原页与简介` |
| `bilibili` | 分 P、置顶评论与简介附件常藏关键信息 | 优先核对分 P 标题、简介链接与可用字幕；无法获取字幕或画面时标注 `仅核对原页与简介`，不臆测视频内操作步骤 |

## 读取层级标注标准

每条进入报告的外部资料，按实际拿到的证据深度标注其中一项：

- `原文已读`：已读取正文、源码、论文页、字幕/逐字稿或完整评论并核对有效日期。
- `部分已读`：仅读到正文摘要、视频简介/目录、试读段落或未展开的评论区。
- `仅索引可见`：仅在搜索引擎或列表页看到标题与片段，未成功打开原页。
- `访问受限`：因登录墙、人机验证、付费墙、地域限制或链接失效未能获取，归入覆盖缺口。
