# 科研绘图社区检索

2026-11-24（历史调研案例，采用早期固定年份分档；现行规则已升级为[动态时效与证据分级](../../skills/best-practice-search/references/source-routing.md#动态时效与证据分级)，同案例的搜索式与交接流程见 [流程案例](workflow-playbook.md)）。先筛 GitHub Skills，再逐个平台搜参考图、Agent 协作、工具实测和视频。证据优先用于系统架构图、机制图和实验数据图。下表百分比是十个社区与视频平台的**建议检索投入**，用于决定补查深度。GitHub、论文和官方文档按需要独立回查。

## 平台分工与本轮覆盖

| 平台 | 权重 | 重点与实际查询 | 本轮证据与限制 |
| --- | ---: | --- | --- |
| 小红书 | 17% | 同领域图例、配色和返工。站内搜 `科研绘图 论文框架图`、`科研绘图 Codex draw.io` | 在已登录的浏览器会话打开五篇笔记。TaskIR 笔记给出原始仓库。另两篇流程笔记展示先画可编辑骨架或先生成草图再重建，并说明了图标遗漏、反复修改和手工收尾。部分笔记的直达地址依赖会话，使用站内标题复查。 [站内搜索](https://www.xiaohongshu.com/search_result?keyword=%E7%A7%91%E7%A0%94%E7%BB%98%E5%9B%BE%20Codex%20draw.io) |
| 知乎 | 8% | 按图型选工具、操作解释。搜 `科研绘图 论文架构图 draw.io 矢量 实践` | 读了 draw.io 入门、论文插图选型和 NanaDraw 演示。入门适合看吸附网格、对齐和导出。产品稿主要提供候选功能线索。 [draw.io 入门](https://zhuanlan.zhihu.com/p/1967599807427240942) · [插图选型讨论](https://www.zhihu.com/question/21664179/answer/2164577371) · [NanaDraw 演示](https://zhuanlan.zhihu.com/p/2032080398369468946) |
| 百度贴吧 | 3% | 老工具、材料三维图和窄学科经验。站内搜 `科研绘图`、`Origin 绘图` | 找到科研绘图吧和材料方向 3ds Max 实例。另一个 Origin 答疑帖只有征集问题，所属板块介绍的是 EA 平台。查绘图软件时应加入 `OriginLab`、`曲线拟合` 等消歧词。 [材料三维图讨论](https://tieba.baidu.com/p/5266364955) · [Origin 同名结果](https://tieba.baidu.com/p/10674460868) |
| LINUX DO | 21% | 中文 Agent 实操、可编辑输出和失败。搜 `科研绘图 skill draw.io`，沿两条不同图型的主题读正文和回复 | 工科论文流程贴区分参考图到 `.drawio` 和图像草稿后重建，含实际成品。数据图讨论报告刻度、单位、多子图风格不一致，建议把要求固定到脚本和检查规则。 [论文框架图实操](https://linux.do/t/topic/1788555) · [实验数据图踩坑](https://linux.do/t/topic/2631735) · [前轮技术路线讨论](https://linux.do/t/topic/2886155) |
| V2EX | 10% | 架构图工具取舍、Agent 生成后的渲染验证。搜 `draw.io excalidraw AI 架构图 mermaid 画图` | 读了工程架构工具、绘图 Skill 和生成文本后的预览三个讨论。Agent 给了 Mermaid/PlantUML 源码却没有渲染，导致后续语法和布局返工。 [工具讨论](https://www.v2ex.com/t/1128213) · [Agent 绘图 Skill](https://hk.v2ex.com/t/1203166) · [渲染返工](https://www.v2ex.com/t/1218486) |
| NodeSeek | 4% | 本地、自托管和轻白板备选。先试站内 `draw.io`，再按域名补查 `draw.io OR excalidraw` | 回读了两篇 Drawnix 讨论。作者说明部分 Mermaid 语法可转成白板元素，不支持的语法会退为图片。适合作为检查导入后是否可编辑的案例。 [Mermaid 导入实操](https://www.nodeseek.com/post-299475-1) · [Drawnix 分享](https://www.nodeseek.com/post-431985-1) |
| Hacker News | 8% | 图即代码、自动布局和可控布局。用 HN 搜索查 `mermaid draw.io` 评论并追关联主题 | 读了 Reladraw 和 DrillFlow 作者帖及评论。前者讨论自动布局与位置控制，后者展示层级分解的用法。可启发设计选择，项目实际能力需回原站验证。 [Reladraw](https://news.ycombinator.com/item?id=49858513) · [DrillFlow](https://news.ycombinator.com/item?id=49740400) |
| Reddit | 13% | 论文绘图实践、工具边界与矢量组图。搜 `publication figures research paper architecture draw.io inkscape matplotlib how do you`，回查 r/AskAcademia 和 r/MachineLearning | 两条原帖正文和回复可读。讨论覆盖用 Matplotlib/R 输出矢量子图、在 Illustrator/Inkscape 合并，以及 TikZ、PowerPoint 和 draw.io 的实际取舍。 [AskAcademia 期刊图经验](https://www.reddit.com/r/AskAcademia/comments/19bs8q1/how_do_people_make_nice_figures_for_their_papers/) · [MachineLearning 论文图讨论](https://www.reddit.com/r/MachineLearning/comments/1p4t8l8/d_how_do_you_create_clean_graphics_that_youd_find/) |
| B 站 | 10% | 中文框架图实操、矢量导出、实验图排版。站内搜 `科研绘图 论文框架图 draw.io AI`、`Matplotlib 科研绘图 论文 多子图 导出` | 核验了作者框架图讲解、Gemini 到 draw.io、Codex 到 draw.io 和 Matplotlib 排版四个视频原页。含资料合集推广的内容作为线索。 [CCF-A 图件拆解](https://www.bilibili.com/video/BV16ZDWBbExg/) · [Gemini 到矢量导出](https://www.bilibili.com/video/BV1qfwNzNEZh/) · [Codex 到 draw.io](https://www.bilibili.com/video/BV1toe16hEts/) · [Matplotlib 排版](https://www.bilibili.com/video/BV1EL4y1s7RR/) |
| YouTube | 6% | 官方用法和英文长链路演示。站内搜 `draw.io diagrams AI agents editable architecture diagram tutorial` | 回查 draw.io 官方架构图教程和 Claude Code + MCP 的 AWS 示例原页。官方教程适合学架构表达，AWS 视频是英文 Agent 实操候选。 [draw.io 官方](https://www.youtube.com/watch?v=fH0ledaVHoQ) · [AWS MCP 演示](https://www.youtube.com/watch?v=nBai0mHVobs) |

视频核对的是原页、简介和可见播放入口，本轮未逐段观看。社区用户的用时、效果和返工属于各自场景。小红书复查时，先站内搜标题再进原帖，记录的笔记 ID 不附会话参数。

## 这轮最值得看的 10 个来源

日期从原帖、相关论文或视频页回查。同档按本题用途排序。8 条确认属于 2025 年起的高权重档，2024 年的组图讨论保留为方法补充，年份未确认的笔记单列在最后。

1. **LINUX DO 工科论文算法框图实操 · 2026-03-20 · 20 分**。看作者在哪类图直接出可编辑文件，在哪类图先试视觉草稿，以及重建耗时从哪里来。 [原帖](https://linux.do/t/topic/1788555)
2. **小红书 TaskIR 笔记 → 原始论文 · 2026-09 · 20 分**。笔记 ID `6ae06262000000000901c34e`。有效日期取原始论文的可查发布日期。作者仓库 *Method Overview* 给出主架构与各子模块的原始说明。 [TaskIR 原图](https://github.com/leoyjTu/TaskIR#-method-overview) · [原始论文](https://arxiv.org/abs/2609.31170)
3. **LINUX DO 实验数据图绘制踩坑 · 2026-07-22 · 20 分**。从计量单位、刻度、风格和子图串位这些失败，反推数据图的验收项。 [原帖](https://linux.do/t/topic/2631735)
4. **V2EX 的 Mermaid／PlantUML 渲染返工 · 2026-06-06 · 20 分**。把生成后实际预览、核对导出文件纳入交付流程。 [原帖](https://www.v2ex.com/t/1218486)
5. **Hacker News Reladraw 讨论 · 2026-09 · 20 分**。读作者与评论对自动布局、相对定位和手工位置控制的取舍。系统图带边界时，可以据此选择布局方式。 [原帖](https://news.ycombinator.com/item?id=49858513)
6. **B 站 CCF-A 框架图拆解 · 2026-04-09 · 20 分**。简介说明采用作者自己的 SIGIR 框架图，适合看多子图排版、格式和视觉层级。 [视频](https://www.bilibili.com/video/BV16ZDWBbExg/)
7. **B 站 Gemini + draw.io 技术路线图 · 2026-03-15 · 20 分**。按简介定位结构化框架、手动布局和 SVG/PDF 导出三个操作。 [视频](https://www.bilibili.com/video/BV1qfwNzNEZh/)
8. **YouTube draw.io 官方架构图教程 · 2026-09-16 · 20 分**。用于核对架构图的基础表达与 draw.io 操作。 [视频](https://www.youtube.com/watch?v=fH0ledaVHoQ)
9. **Reddit r/AskAcademia 的数据图组装讨论 · 2024-01-21 · 12 分**。按期刊成稿宽度生成子图，再用矢量文件组合，保持字号和线宽一致。用于组图方法参考。 [原帖](https://www.reddit.com/r/AskAcademia/comments/19bs8q1/how_do_people_make_nice_figures_for_their_papers/)
10. **小红书《GTP 半自动化流程出科研绘图》 · 年份待核 · 暂记 0 分**。笔记 ID `6a8977dd000000002202d937`。原页显示 `08-22`。看作者怎样从生成候选到可编辑重建，再补图标和手调。 [按原题站内检索](https://www.xiaohongshu.com/search_result?keyword=GTP%20%E5%8D%8A%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%81%E7%A8%8B%E5%87%BA%E7%A7%91%E7%A0%94%E7%BB%98%E5%9B%BE)

## 转成 sub-agent 的绘图分工

系统架构图走可编辑 `.drawio` 源文件路线。给 Agent 一份固定的节点、关系和边界表，再用两张同领域参考图说明想借鉴的布局。同一份关系表可以形成两个布局草案。先查节点、箭头和组间关系，再按成稿尺寸看对齐、留白及导出。参考图来源注明论文或项目。 [draw.io 官方 AI 绘图与验证文档](https://www.drawio.com/docs/reference/diagram-generation/)

实验数据图可以参考 Figures4papers 的 Matplotlib 示例。先明确列名、单位、误差线含义、坐标范围和统一样式，再让 Agent 生成可重跑脚本及矢量稿。组合多面板时按成稿宽度设定字号和线宽，核对子图标签与数据生成关系。 [Figures4papers 上游](https://github.com/ChenLiu-1996/figures4papers)

想试图像模型时，可让它给布局草案或单独图标。从设计草案重建的图应能逐个编辑节点、文字、图标和箭头。需要把截图当参考时，沿小红书笔记追作者文档或论文，再区分借鉴布局和直接复用图件。
