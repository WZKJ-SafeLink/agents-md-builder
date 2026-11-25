> 此报告记录1.0.0历史交付。后续用户实际上传因目录层级超限失败，最新1.0.1修复包和验证记录见 [WorkBuddy修复报告](WORKBUDDY_FIX_v1.0.1.md)。WorkBuddy上传请使用新包。

# AGENTS.md Builder 1.0.0 最终交付报告

开发与验证日期：2026-11-24。发布者：Safe Link。原创内容许可证：Apache-2.0。工程位于 `/Users/jackjiang/Documents/WorkBuddy/Skill/agents-md-builder`。

## 完成情况

已在当前工作区实现可运行的本地 Agent Skill、按需知识库、Python 标准库辅助工具、模板/schema、自动化测试、用户文档、发布资料、图标和两个实际 ZIP。没有安装系统依赖、执行被扫描工程代码、上传项目内容或提交市场。

该产品采用“宿主智能体语义工作流 + 确定性工具”的任务书架构；自然语言理解、复杂语义分析、官方资料检索和版本适配由宿主完成，不能将脚本模式匹配描述为完整语义审查。

## 功能交付

| 编号 | 功能及实际实现 |
|---|---|
| F01 | CREATE：自然语言由 Skill 提取明示要求；requirements JSON 可生成未知项明确的候选 |
| F02 | 安全静态扫描、常用 gitignore、深度/文件数/字节预算和不完整范围报告 |
| F03 | 多语言配置和依赖识别、版本状态、证据与置信度；本地 POM 继承 |
| F04 | 模块、目录角色、锚点和依赖声明；架构语义由智能体核实 |
| F05 | 只读格式、安全、路径、版本、命令证据审查与问题定位 |
| F06 | 七维确定性指标评分、逐项解释、覆盖率和风险等级限制 |
| F07 | 智能体语义优化流程、保守精确去重、原文保护与候选 |
| F08 | 独立栈模块的根级/模块级候选，避免机械分层 |
| F09 | 结构化 key/value/scope/强度冲突；自由文本只列候选 |
| F10 | 宿主原生官方搜索核验流程、公开来源登记、离线降级 |
| F11 | 带来源、分类、作用域和验证的用户/企业明确规则 |
| F12 | 统一 diff、新增/修改/删除/保留及前后大小与同口径评分 |
| F13 | 上下文建议预算、同范围重复合并和语义精简工作流 |
| F14 | 中文/英文输出；CLI 英文为常见技术保守子集，宿主可按需翻译补齐 |
| F15 | 旧新 profile 的技术版本、模块、命令及架构候选变更分析 |
| F16 | 结构化规则按通用/技术/企业/项目/不适用分类迁移，过滤私有内容 |

所有 P0 均有实现入口；P1 提供可使用的基础实现。完整宿主语义效果尚未逐场景实机回放，不夸称已证明编码质量提升。

## 文件与知识库统计

- 源工程文件：208（排除 dist、Git 和编译缓存）；零字节文件：0。
- Python：19 个 CLI + common.py，全部仅依赖标准库。
- Markdown 参考：91份；技术与智能体主题79份，核心工作流10份，索引与来源各1份；另有资料访问 JSON。
- 模板7份、schema3份；虚构测试工程17个；宿主验收场景20个。
- 知识库分布：core=10; languages=13; frameworks=22; databases=5; middleware=6; architecture=9; engineering=15; security=6; agents=3; sources=1。
- 图标：release/icon.png，512×512 RGB，5913字节；另有可编辑 SVG 和设计说明。

未知或未专门建设参考的技术仅提供通用规则与官方核验流程，不宣称完整支持所有产品特性。

## 实际测试与安全检查

执行 `python3 -m unittest discover -s tests -v`：140项，成功140，失败0、错误0、跳过0，用时3.768秒。环境为 macOS / Python 3.11.5。详见 [测试报告](test-report.md)、[原始日志](unit-test-output.txt) 和 [结构化结果](test-results.json)。

已验证敏感文件不读取、符号链接/硬链接/reparse point 保护、路径穿越与 ZIP 攻击、资源上限、多行凭据脱敏、官方公共引用保留、静态分析不执行恶意脚本、manifest/文件名提示注入防护、测试夹具不污染主栈、显式覆盖与摘要并发检查、发布资源凭据阻断。该结果不是安全认证或对未知攻击的绝对保证。

五个 CLI 生成调用在虚构 JPA、Vue、Python、英文 Next.js 和前后端工程中产出7个候选，见 [样例执行记录](smoke-results.json) 和 examples/。工程自身 AGENTS.md 的机械文档指标为97.0 /100，级别A，无检测到的高风险；这不是语义质量认证。

## Skill 与平台验证

本 Skill 的 validate_skill.py 已通过通用入口及解压后两个平台入口的元数据、链接、资源和 Python 语法检查。20个 Python 模块另通过3.10语法解析；原生运行实测为3.11.5。skill-creator 上游 quick_validate.py 未能启动，原因是当前 Python 缺少 PyYAML；没有自动安装系统依赖，不能把这项记为通过。

Agent Skills 基础格式与 WorkBuddy 市场必填字段已分别按官方文档核验；WorkBuddy 包补充展示字段与 Safe Link 作者，不污染通用入口。官方依据见 [来源登记](../references/sources/official-sources.md) 和 [WorkBuddy 发布说明](../docs/WORKBUDDY_PUBLISH.md)。78个公开资料入口中72个可访问，6个未验证；多数具体规则仍需按用户工程版本实时核验。

**未实际导入 WorkBuddy、未提交市场审核。** 上传数值限制、所有 ZIP 解析细节及 AGENTS.md 的 WorkBuddy 加载机制仍需实机确认，不能照搬 Codex。Windows/Linux 原生运行、无 Python/无联网等完整宿主降级、20个完整宿主场景和真实智能体三组对照实验未执行。

## 实际发布产物

- [agents-md-builder-v1.0.0.zip](../dist/agents-md-builder-v1.0.0.zip)：198700字节，137个文件；SHA-256 `c4856eaf1214af931935f7a980df08b205f2b3e23231200600979af7384363f3`。真实路径：`/Users/jackjiang/Documents/WorkBuddy/Skill/agents-md-builder/dist/agents-md-builder-v1.0.0.zip`。
- [agents-md-builder-workbuddy-v1.0.0.zip](../dist/agents-md-builder-workbuddy-v1.0.0.zip)：198803字节，137个文件；SHA-256 `1f6f7c55217e563a49bbf1a7e87bbffd56d81893e7cc6dde2a6716251b28998b`。真实路径：`/Users/jackjiang/Documents/WorkBuddy/Skill/agents-md-builder/dist/agents-md-builder-workbuddy-v1.0.0.zip`。

两个包均只有一层 agents-md-builder 目录，内有 SKILL.md；manifest、CRC、解压后的结构校验均通过。允许清单排除了开发期 AGENTS.md、测试/恶意夹具、缓存、内部测试报告和历史发布包。详细结果见 [build-results.json](build-results.json)。图标作为市场单独上传素材保留在 release。

## 安装与发布操作

1. WorkBuddy 用户选择 WorkBuddy 专用 ZIP；通用 Agent Skills/Codex 使用通用 ZIP 或解压后的技能目录。
2. 在 WorkBuddy 当前客户端技能添加/上传入口导入；若 ZIP 层级解析不接受，选择解压后的 agents-md-builder 文件夹。入口和字段限制以实际产品为准。
3. 在授权虚构项目中输入“帮我生成 AGENTS.md 候选”，检查不执行工程脚本、不覆盖旧文档；再验证 AUDIT 和无 Python 降级。
4. 到官方开放平台完成真实主体资料，使用 [市场介绍](marketplace-description.md)、[示例](example-prompts.md)、[图标](icon.png)、许可证及第三方声明；检查表单后自行提交审核。
5. 后续开发按 README 的 unittest、validate_skill 和 package_skill 命令复验；输出已存在时必须使用新文件名，不静默覆盖。

完整入口见 [README](../README.md)、[用户手册](../docs/USER_GUIDE.md) 和 [发布清单](release-checklist.md)。剩余事项均为真实平台或运行环境验证，没有伪造兼容性/审核结论。
