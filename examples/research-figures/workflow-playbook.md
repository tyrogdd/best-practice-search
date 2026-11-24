# 科研绘图检索流程案例（Playbook）

> 本案例归档于 `examples/`，作为特定垂直领域的参考范例与用户示范沉淀示例，与通用 Skill 本体解耦。同案例的 10 平台社区覆盖与精选来源详见 [社区检索记录](community-search.md)。

示例任务是调研一张论文用的虚拟化系统架构图。输出包括参考图、Agent 协作流程和可交付格式。数据图、机制图和可直接复用的素材分别匹配检索入口。

## 用户指引的第一步

先到 GitHub 搜科研绘图 Skills。按数据图和架构图分别检索，打开仓库里的实际 `SKILL.md`、依赖与许可后筛选。将入选文件放到独立试跑目录，保存固定提交和静态审查记录，供后续 sub-agent 读取。

## 用户指引的第二步

按平台分配检索重点和投入权重。小红书先找同领域图例和半自动流程，LINUX DO 找科研绘图的实操与返工案例，V2EX 和 Hacker News 找技术取舍，Reddit 看期刊图件与后期组合。每个平台都记录实际查询、原帖证据和覆盖缺口。用户在小红书登录后续查，站内标题和笔记 ID 可用于复跑。

## 可复跑的搜索式

| 要解决的问题 | 搜索式和入口 | 筛选依据 |
| --- | --- | --- |
| 同类系统图怎么画 | Google 图片 `Firecracker microVM host integration architecture diagram` | 回查论文或维护者文档。观察运行边界、控制路径、图例和颗粒度 |
| 同一套图怎样在文章和演讲中讲清楚 | 网页或 YouTube `Firecracker Agache NSDI 2020 presentation slides` | 优先会议作者页。并列查论文、讲稿和演讲，记录实际查看的定位点 |
| 中文视频有没有完整操作 | B 站站内 `科研绘图 drawio 论文框架图` | 看是否演示改图、对齐、连线或导出，优先能拿到可编辑源文件的教程 |
| Agent 能交付什么 | `site:drawio.com AI agent diagram generation mxfile.xsd` | 查官方格式、渲染、验证和导出。软件能打开与图的语义正确分别验收 |
| 有没有附代码的统计图 | `scientific figure Python publication example source code heatmap` | 优先作者仓库和绘图库例程。匹配数据形状、统计含义与最终尺寸 |
| 实际使用哪里会失败 | `site:linux.do 技术路线 skill draw.io` 或 `site:reddit.com research paper figures inkscape workflow` | 看具体失败、修改成本、复现条件。访问受限则标记为线索 |

## 2026-11-24 Chrome 检索记录

- Google 图片返回 AWS 官方博客和多个二手解释。回到 Firecracker 维护者的 `docs/design.md`，确认有 **Firecracker Host Integration** 与 **Firecracker Threat Containment** 两张图。前者用于参考如何把宿主与 microVM 放在同一张图中，后者用于对照信任分区的表达。两张图在本例中用作视觉参考。 [Firecracker 设计文档](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md)
- NSDI 作者页可同时找到论文、演示文稿和演讲视频。本次核对到视频入口。选具体片段时，需要进一步查看演讲或字幕后再记时间戳。 [Firecracker 的 USENIX 作者页](https://www.usenix.org/conference/nsdi20/presentation/agache)
- B 站站内搜索找到可加载的 11 分 04 秒 draw.io 基础教程，页面说明覆盖流程图、泳道图和架构图。 [draw.io 基础教程](https://www.bilibili.com/video/BV1i24y1C7fU/)
- Figures4papers 的 README 给出带成图的 Python 项目和 `scientific-figure-making/` Skill 目录，按图型挑例子。Matplotlib Gallery 用于查绘图库原生做法。 [Figures4papers](https://github.com/ChenLiu-1996/figures4papers) · [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- LINUX DO 发帖者反馈，可编辑的 `.drawio` 有利于手调，直接生成图有时会漏边框。同一社区另有数据图风格、刻度和单位不一致的案例。这些是个案，适合转成验收项。 [技术路线图讨论](https://linux.do/t/topic/2886155) · [数据绘图讨论](https://linux.do/t/topic/2631735)
- 官方 draw.io 文档给出 XML 样式规范、XSD 与可选 MCP 入口。PLOS 的绘图文章适合明确图要传达的信息，提交格式以目标期刊或会议的要求为准。 [draw.io 生成与验证](https://www.drawio.com/docs/reference/diagram-generation/) · [PLOS 图表十条规则](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833) · [Nature 最终提交规范](https://www.nature.com/nature/for-authors/final-submission)
- 本次也筛查了知乎、V2EX、NodeSeek、贴吧和 Hacker News。小红书搜索需要重新登录，Reddit 原帖触发人机验证，两处只保留覆盖缺口。视频核对到原页、简介或播放入口，未逐段观看。

## Agent 交接

一张图先写一句结论、目标读者和尺寸。架构图列出节点、边、箭头方向、分组和每条关系的出处。让 Agent 从同一份关系表提供两个布局草案，定稿后生成可编辑 `.drawio` 和投稿所需的矢量文件。保留图注与关系表。检查图能打开、源格式与导出相符，并在成稿尺寸检查标注、留白、箭头方向和层级。

数据图交给 Agent 原始数据或已核验汇总、统计定义和版本。用 Python 或 R 出图，交付输入或其路径、脚本、图注和所需矢量文件。核对数据列、单位、比例尺、误差线含义、颜色和子图对应关系。需要修改时从源脚本重跑，保留新旧预览供比较。

参考图记录可抽取的设计原则，例如布局或标注方式。直接使用图标、照片或他人图件时，记录文件页、作者、许可和署名要求。图片搜索的许可筛选只提供线索，回原站确认。 [Google 图片使用权说明](https://support.google.com/websearch/answer/29508?hl=en&co=GENIE.Platform%3DDesktop)
