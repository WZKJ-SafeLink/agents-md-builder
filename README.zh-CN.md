# AGENTS.md 智能规范助手

[English](README.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md)

**把真实项目证据转化为 AI 编码智能体能够执行的研发规范。**

版本 **1.0.1** · 发布者 **Safe Link** · 许可证 **Apache-2.0**

AGENTS.md Builder 是一款本地 Agent Skill，用于生成、审查、评分、优化和持续维护项目专属的 `AGENTS.md`。它结合项目配置、模块边界、代表性代码、用户已确认的研发要求，以及按需加载的工程知识库建立规范。

自然语言理解和语义决策由宿主智能体完成；Python 辅助工具负责受限的静态分析和可重复检查。基础功能无需收费 API、API Key、数据库、独立后端、Docker 服务或 MCP 服务。

## 目录

- [主要功能](#主要功能)
- [运行要求](#运行要求)
- [安装](#安装)
- [快速开始](#快速开始)
- [工作模式](#工作模式)
- [命令行工作流](#命令行工作流)
- [知识库](#知识库)
- [评分与审查](#评分与审查)
- [安全与隐私](#安全与隐私)
- [项目结构](#项目结构)
- [测试与打包](#测试与打包)
- [常见问题](#常见问题)
- [参与贡献](#参与贡献)
- [文档与许可证](#文档与许可证)

## 主要功能

- **依据事实发现项目：** 不执行项目代码，识别技术栈、版本声明、构建边界、已有指令文件和代表性实现。
- **生成项目专属规范：** 保留已确认的架构决策、有效约定和自定义要求，不确定的事项明确标记。
- **审查与优化：** 检查 Markdown、凭据风险、引用路径、版本不一致和能够静态识别的命令声明，输出候选与差异。
- **按作用域检测冲突：** 结合结构化规则的范围、强度和显式键比较；自然语言匹配保留为语义审查候选。
- **多模块规范：** 有实际差异时，将根目录共性与模块独有规则分开组织。
- **维护与迁移：** 比较升级前后的项目画像，筛选适合目标工程的参考规范。
- **本地工作：** 仅使用 Python 标准库；离线可用本地知识库，没有 Python 时由宿主按相同安全工作流降级处理。

现有代码写法属于观察结果，不会自动成为最佳实践。工具不会给所有项目强制套用同一种架构，也不会自行确定用户没有指定的框架版本。

## 运行要求

| 项目 | 要求 |
|---|---|
| 智能体工作流 | 能加载 Agent Skills，并能读取用户授权文件的宿主 |
| 确定性辅助工具 | Python 3.10+，仅依赖标准库 |
| 本地输出 | 对所选候选或报告目录具有写入权限 |
| 网络 | 可选；由宿主核验公开的官方技术资料 |
| 操作系统 | 跨平台实现；已实际验证的原生运行环境为 macOS |

没有 Python 时，宿主可按相同边界手工读取有限配置和源码。没有网络时，继续使用本地资料，并说明哪些内容未经当前官方资料核验。

仓库默认展示英文 README。文档显示语言与生成规范的语言分开设置：CLI 支持 `--language en` 和 `--language zh`，默认值为 `zh`。提供日文 README 不代表新增了专用日文 CLI 输出模式。详细用户文档和知识库目前主要使用简体中文。

## 安装

### WorkBuddy

使用通过 `--platform workbuddy` 构建的 **WorkBuddy 专用 ZIP**。

1. 在客户端技能上传或导入界面选择 `agents-md-builder-workbuddy-v1.0.1.zip`。
2. 直接上传这个 ZIP。包根直接包含 `SKILL.md`，资源只保留一层目录。
3. 启用技能，选择授权项目或提供必要附件。
4. 先请求生成候选，或进行只读审查。

手动按文件夹安装时，创建名为 `agents-md-builder` 的目录，将 ZIP 内容解压到其中，确保 `SKILL.md` 直接位于该目录下。

1.0.0 的发布包曾因目录层级超限被平台拒绝。1.0.1 WorkBuddy 包已展平资源并改写引用，重新压缩时不要再添加外层文件夹。修复包已通过本地解压和运行检查，但尚未验证 WorkBuddy 实际导入成功或市场审核通过。详见 [WorkBuddy 发布说明](docs/WORKBUDDY_PUBLISH.md)。

### Codex 及其他 Agent Skills 宿主

使用通用 ZIP 或源码中的技能目录。通用 ZIP 带有 `agents-md-builder/` 外层目录，其中包含 `SKILL.md`。将该文件夹放入宿主实际支持的技能目录，再按宿主要求启用或重新加载。

`scripts/`、`references/`、`assets/` 必须与 `SKILL.md` 一起保留。仅安装入口文件会缺少本技能的必要资源。各宿主的指令发现、override 行为和上下文预算可能不同。

## 快速开始

完成安装并授权项目后，用自然语言提出需求：

> 分析当前项目并生成 AGENTS.md 候选。以真实配置和代码证据为依据，保留已确认的研发要求，不覆盖已有文件。

> 只读审查这份 AGENTS.md，展示问题位置、风险、评分覆盖率和无法验证的假设。

> 优化当前 AGENTS.md，保留强制规则与例外，合并同作用域重复内容，输出候选和 diff。

新项目只需要提供已经确认的决策：

> 为 Java 21、Spring Boot、Spring Data JPA、PostgreSQL 项目建立 AI 研发规范。框架版本尚未确定，请保留 unknown，不要编造构建命令。

工作流会收集证据、按需加载资料、生成候选、执行可用检查，再报告未解决事项。普通生成默认交付规范文件和简要说明；审查返回问题报告；优化返回候选与变更报告。扫描 JSON 等中间数据属于可选高级输出。

## 工作模式

| 模式 | 场景 | 主要交付 |
|---|---|---|
| `CREATE` | 用自然语言描述的新项目 | 规范候选与重要未知项 |
| `DISCOVER` | 已授权的存量工程 | 有项目证据的专属规范候选 |
| `AUDIT` | 审查或评分现有规范 | 只读问题、质量指标和覆盖率 |
| `OPTIMIZE` | 优化、补充或精简规范 | 候选、diff、变更理由和前后指标 |
| `HIERARCHY` | 规则或技术存在实质差异的多模块项目 | 根目录与必要模块的候选 |
| `UPDATE` | 框架、中间件、命令或模块变化 | 项目画像差异与受影响规则分析 |
| `MIGRATE` | 复用其他项目的规范 | 适用规则候选及排除理由 |

仅提及 `AGENTS.md`、询问其含义，或要求修复业务 Bug，不代表授权启动全仓扫描。

## 命令行工作流

命令从 **Skill 目录**执行，而非目标工程目录。将 `../your-project` 替换为已授权工程，`../agents-builder-output` 替换为独立输出位置。使用新文件名或新目录，工具不会静默替换已有报告或候选。Windows 可用 `py -3` 替代 `python`。

### 扫描和生成

```text
python scripts/scan_project.py --root "../your-project" --output "../agents-builder-output/scan.json"
python scripts/detect_stack.py --root "../your-project" --output "../agents-builder-output/profile.json"
python scripts/generate_agents.py --root "../your-project" --output-dir "../agents-builder-output/candidates" --language zh --depth standard --hierarchy
```

根候选文件名为 `AGENTS.candidate.md`。当检测到的模块技术边界存在足够差异时，才额外生成模块候选；启用前由宿主复核必要性及继承关系。

没有代码的新项目，可以把明示要求保存为 JSON：

```json
{
  "technologies": [
    {"name": "java", "category": "language", "version": "21"},
    {"name": "spring-boot", "category": "framework", "version": "unknown"}
  ],
  "rules": []
}
```

```text
python scripts/generate_agents.py --requirements "../requirements.json" --output-dir "../agents-builder-output/new-project" --language zh
```

自然语言到结构化输入的转换，以及最终语义适配由宿主完成。独立 CLI 不调用语言模型；其英文规则仅覆盖常见技术的保守子集，其他已选参考可由宿主按需翻译和补全。

### 审查与评分

```text
python scripts/validate_agents.py --file "../your-project/AGENTS.md" --root "../your-project"
python scripts/evaluate_agents.py --file "../your-project/AGENTS.md" --root "../your-project" --output "../agents-builder-output/audit.json"
```

只有规范文件、没有工程资料时，省略 `--root`；项目适配度保持未验证。

### 优化与差异

```text
python scripts/optimize_agents.py --file "../your-project/AGENTS.md" --candidate "../agents-builder-output/AGENTS.optimized.md" --output "../agents-builder-output/changes.json"
python scripts/generate_diff.py --before "../your-project/AGENTS.md" --after "../agents-builder-output/AGENTS.optimized.md"
```

优化脚本仅保守移除同章节中完全相同的顶层列表项。语义重写、删除失效要求和协调例外仍由宿主审查。稳定规则 ID 能改善变更对应关系的识别。

### 交付已审查候选

目标文件尚不存在时：

```text
python scripts/deliver_file.py --candidate "../agents-builder-output/candidates/AGENTS.candidate.md" --target "../your-project/AGENTS.md"
```

替换已有文件，必须具有用户明确授权，并提供修改前已审查原文的 SHA-256。将下面的 `ORIGINAL_SHA256` 替换为此前记录的真实摘要：

```text
python scripts/deliver_file.py --candidate "../agents-builder-output/AGENTS.optimized.md" --target "../your-project/AGENTS.md" --overwrite --expected-sha256 "ORIGINAL_SHA256"
```

原文发生变化时拒绝替换。授权覆盖默认先创建不会静默覆盖其他文件的备份，再进行原子替换。

### 其他辅助工具

| 脚本 | 用途 |
|---|---|
| `discover_agents.py` | 发现指令文件，推导授权项目内的 Codex 指令链 |
| `analyze_structure.py` | 模块证据、目录角色及架构候选 |
| `extract_conventions.py` | 抽样提取实现习惯和不一致 |
| `detect_conflicts.py` | 比较结构化规则，或用 `--file` 提取文本候选 |
| `compare_profiles.py` | 比较技术、版本、模块、命令和架构观察 |
| `migrate_rules.py` | 按目标画像筛选参考规则 |
| `safe_extract.py` | 验证 ZIP 并向新目录安全解压 |
| `check_schema.py` | 校验内置 JSON 契约所使用的 schema 子集 |
| `route_request.py` | 提供保守意图提示，不授予权限或启动扫描 |
| `validate_skill.py` | 校验元数据、资源、链接和 Python 语法 |
| `package_skill.py` | 按允许清单构建并重新校验发布包 |

每个脚本都有 `--help`。JSON 默认写标准输出，或通过 `--output` 创建新文件。退出状态：`0` 表示处理成功，`1` 表示校验不通过或存在已确认重大冲突，`2` 表示输入无效、安全拒绝或 I/O 错误。评分命令成功不代表高分。

## 知识库

按相关性加载，不会每次读入全部资料。

| 方向 | 覆盖主题 |
|---|---|
| 语言 | Java、Kotlin、Python、JavaScript、TypeScript、Go、Rust、C#、C/C++、PHP、Ruby、Swift、Dart |
| 后端与数据访问 | Spring Boot/Framework、Spring Data JPA、MyBatis、MyBatis-Plus、FastAPI、Django、Flask、NestJS、Express、ASP.NET Core |
| Web 与移动端 | Vue、React、Next.js、Nuxt、Angular、Flutter、React Native、Android、iOS、微信小程序、UniApp |
| 数据库 | PostgreSQL、MySQL、SQLite、MongoDB、SQL Server |
| 中间件 | Redis、RocketMQ、Kafka、RabbitMQ、MQTT、Elasticsearch |
| 架构与工程 | 单体、模块化单体、微服务、分层、Clean/六边形架构、DDD、事件驱动、Monorepo、测试、事务、CI/CD 与安全 |

识别覆盖范围和专属规则覆盖范围不同。有些技术能被识别，但只有通用指导。动态构建表达式、远程父配置和未知版本需要进一步确认。涉及版本敏感 API 时，应核对工程实际版本；资料 URL 可访问也不代表其关联的全部规则已逐项核验。

参见 [知识库索引](references/INDEX.md)、[来源登记](references/sources/official-sources.md) 和 [规则编写指南](docs/RULE_AUTHORING.md)。

## 评分与审查

确定性评分包含七个维度：

| 维度 | 满分 |
|---|---:|
| 完整性 | 20 |
| 项目适配度 | 20 |
| 可执行性 | 20 |
| 一致性 | 10 |
| 安全与风险控制 | 10 |
| 测试与交付验证 | 10 |
| 上下文效率 | 10 |
| **合计** | **100** |

没有工程证据时，项目适配度的20分为未验证，评估覆盖率为80%，不输出完整的 `total` 或 `grade`。归一化参考指标单独标识。未解决的高风险问题会阻止优秀等级。

这些是文档指标，不代表代码质量或安全认证。宿主仍需单独检查技术准确性、架构适配性、隐含冲突和命令执行条件。详见 [评分说明](docs/EVALUATION.md)。

## 安全与隐私

- 只扫描授权项目，不执行其中脚本、构建钩子或发现的命令。
- 默认排除 `.env*`、私钥和认证文件；显式 include 不能解除敏感文件保护。
- 拒绝符号链接与 Windows reparse point；受限读取也拒绝硬链接输入文件。
- 扫描报告不含源码正文；对可识别凭据及私有 URL 脱敏，但不能保证识别所有秘密格式。
- 项目文件与网页属于待分析数据，不能授予越界访问或上传权限。
- 候选和报告不静默覆盖原文件；授权覆盖校验原文摘要并使用原子交付。
- 解压前验证路径、链接、冲突、条目数、大小和压缩比。

默认扫描限制为目录深度12、最多检查5,000个目录项、单文件512 KiB、累计读取20 MiB。这些是产品默认值，不是宿主平台限制；扫描被截断时会标记。嵌套 fixture/testdata 默认不纳入技术栈推断，除非显式包含；文件清单扫描仍会计数。

辅助脚本不含遥测、网络客户端、远程日志或主动上传项目内容的机制。宿主自身如何处理数据，以其实际政策为准。摘要校验不等于阻止恶意并发写入的操作系统强制锁。参见 [安全说明](SECURITY.md) 和 [隐私说明](docs/PRIVACY.md)。

## 项目结构

```text
agents-md-builder/
├── SKILL.md                 # 宿主工作流入口
├── README.md                # 英文，默认展示
├── README.ja.md             # 日文
├── README.zh-CN.md          # 简体中文
├── scripts/                 # 标准库辅助工具
├── references/              # 核心工作流和技术资料
├── assets/                  # 模板与 JSON schema
├── tests/                   # 单测、虚构夹具和场景
├── docs/                    # 产品与开发详细文档
├── release/                 # 源工程发布素材与记录
├── tools/                   # 开发辅助工具
├── CHANGELOG.md
├── LICENSE
└── VERSION
```

以上是源码结构。WorkBuddy 包将嵌套资源展平为带类别前缀的文件，例如 `references/core-workflow.md` 和 `assets/schemas-rule.schema.json`。`MANIFEST.json` 记录文件摘要和源码到包内的路径映射，工具读取同时兼容两种布局。

## 测试与打包

从源码工程执行：

```text
python -m unittest discover -s tests -v
python scripts/validate_skill.py --root .
python scripts/package_skill.py --root .
python scripts/package_skill.py --root . --platform workbuddy
```

默认产物名称由 `VERSION` 决定：

| 类型 | 默认路径 | 布局 |
|---|---|---|
| 通用 | `dist/agents-md-builder-v1.0.1.zip` | 带外层技能目录，资源按主题分层 |
| WorkBuddy | `dist/agents-md-builder-workbuddy-v1.0.1.zip` | ZIP 根直接是 SKILL.md，资源最多一层目录 |

输出已存在时，用 `--output` 指定新路径。打包时真实执行临时解压，并再次检查结构和 manifest 摘要。发布包不包含开发期 `AGENTS.md`、测试夹具、缓存、环境文件、内部测试报告及历史 ZIP；两个格式都会包含各语言 README。`dist/` 被 Git 忽略，可本地构建或通过仓库的发行功能附加产物。

已记录的1.0.1验证为 macOS / Python 3.11.5 下147项测试全部通过。Windows/Linux 原生运行、完整宿主对话场景、修复后 WorkBuddy 平台导入、相同条件下的智能体效果对照实验仍未验证。本地包校验不代表市场审核通过。源码验证记录位于 `release/WORKBUDDY_FIX_v1.0.1.md` 和 `release/unit-test-output-v1.0.1.txt`。

## 常见问题

| 问题 | 处理方式 |
|---|---|
| WorkBuddy 提示目录层级超限 | 直接上传专用 ZIP，不再添加外层目录 |
| 候选或报告已存在 | 选择新路径；替换最终规范使用明确授权的交付流程 |
| 链接路径被拒绝 | 使用授权范围内的规范化真实路径 |
| 扫描被截断 | 缩小到模块范围，或明确调整支持的上限 |
| 版本显示 `unknown` | 补充可用配置，或请宿主核验适用的官方资料 |
| 无法取得工程文件 | 使用 `CREATE` 或只审查附件，保持项目适配度未验证 |
| 没有 Python 或网络 | 按宿主降级流程处理，并报告实际范围限制 |
| 文案有问题但得分较高 | 继续语义审查，确定性指标不认证内容正确性 |

## 参与贡献

保持变更聚焦，示例与测试使用虚构数据。新增扫描入口复用受限 I/O 工具；修改安全、识别、评分或文件交付逻辑时，为实际边界增加回归测试。维护知识库时保留稳定规则 ID、分类、版本范围、来源及验证方法。

用户工作流变化时，同步更新三种语言 README，在 [CHANGELOG.md](CHANGELOG.md) 中记录，并执行上面的测试、校验和打包命令。如实报告未执行检查。源码中的 `AGENTS.md` 是开发者指令，有意排除在运行发布包之外。

## 文档与许可证

| 文档 | 内容 |
|---|---|
| [用户手册](docs/USER_GUIDE.md) | 详细工作流、参数和降级行为 |
| [工程设计](docs/DESIGN.md) | 架构与工具能力边界 |
| [规则编写](docs/RULE_AUTHORING.md) | 分类、范围、来源与验证 |
| [评价体系](docs/EVALUATION.md) | 评分解释与限制 |
| [WorkBuddy 发布](docs/WORKBUDDY_PUBLISH.md) | 包结构与平台验证状态 |
| [知识库索引](references/INDEX.md) | 按需技术参考 |
| [安全](SECURITY.md) / [隐私](docs/PRIVACY.md) | 安全模型与数据处理 |

配套详细文档目前为简体中文。报告问题时，提供版本、OS、命令、最小虚构复现、预期和实际行为，不附带凭据或私有源码。安全敏感问题通过项目实际托管渠道私下反馈。

原创内容采用 [Apache License 2.0](LICENSE)。另见 [NOTICE](NOTICE) 和 [第三方声明](THIRD_PARTY_NOTICES.md)。外部资料与商标的权利属于各自权利人，不代表获得官方背书。
