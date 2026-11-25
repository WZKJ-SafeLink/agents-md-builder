# WorkBuddy 安装与发布

核验日期：2026-11-24。官方依据：[技能开发](https://open.workbuddy.cn/docs/skill)、[开放平台](https://open.workbuddy.cn/)。

## 已确认与适配

官方文档使用 Skill 文件夹、SKILL.md YAML + Markdown、可选 references/scripts，并说明开放平台解析 ZIP。市场字段要求 name、display_name、display_name_en、description、description_zh、description_en、version、author；可选字段仅在有实际需要时添加。脚本资源可被宿主调用，实际运行时仍需检查本机 Python。

本项目通用源入口只用 name/description，以兼容 Agent Skills；WorkBuddy 专用打包增加必填市场元数据，作者由用户确认的 Safe Link 提供。通用包保留 agents-md-builder 外层目录和按主题分层的源码布局。

2026-11-24 用户实际上传1.0.0时，平台返回“目录层级超限 — Skill 包仅支持两级目录结构（根目录/二级目录/文件）”。从1.0.1起，WorkBuddy 专用 ZIP 根直接放 SKILL.md，不加外层技能目录；references、assets、scripts、docs 内均直接放文件，没有嵌套资源目录。类别放进文件名前缀，链接和运行时资源读取同步适配：

```text
SKILL.md
VERSION
MANIFEST.json
references/
  INDEX.md
  core-workflow.md
  frameworks-spring-data-jpa.md
  sources-access-checks.json
assets/
  schemas-rule.schema.json
  templates-AGENTS.template.md
scripts/
  generate_agents.py
  common.py
docs/
  USER_GUIDE.md
```

打包和解压后校验强制检查每个 WorkBuddy 成员最多两个路径部分；资源重名时拒绝构建。目录限制来源是用户实际平台错误，不能把此前本地结构校验称为平台兼容性验证。

## 未公开或未验证

本次查阅页面未确认上传字节上限、图标强制尺寸、审核时长、全部入驻必需字段和 Python 最低版本保证。AGENTS.md 的 WorkBuddy 继承/override/上下文预算也未确认。不能从 CodeBuddy IDE 文档推断所有 WorkBuddy 桌面行为。

1.0.0 的用户上传失败已有实际证据；修复后的1.0.1尚未重新上传验证，也未获市场审核。macOS 上 Python 测试通过不代表已验证 Windows/Linux 原生运行。

## 用户安装

1. 上传 `agents-md-builder-workbuddy-v1.0.1.zip`。它的 ZIP 根直接包含 SKILL.md；不要使用旧1.0.0包或通用包提交 WorkBuddy。
2. 如需手动安装，先创建名为 agents-md-builder 的文件夹，把 WorkBuddy ZIP 内容解压到其中，再选择这个文件夹。不要额外打包外层文件夹，也不要上传整个源码工程。
3. 启用后在已授权虚构工程中输入“帮我生成 AGENTS.md 候选”。检查触发、Python 可用性、只读扫描和候选交付。
4. 用现有规范再试 AUDIT，确认原文未变；无 Python/联网时确认降级说明。实际 UI 以客户端为准。

## 市场提交

到开放平台按入驻和当前表单操作，选择 Safe Link 及实际联系/主体资料；本项目不代填身份材料。使用 release 的市场介绍、示例、图标和 Apache-2.0/第三方声明，上传 WorkBuddy ZIP。先在平台检查解析回填、字段长度、图标与包大小限制，再提交审核；遇审核要求逐项补证。不要将本地静态校验宣称为平台认证。

## 本地构建

```text
python scripts/package_skill.py --root . --platform workbuddy --output dist/agents-md-builder-workbuddy-v1.0.1.zip
```

必须使用未存在的输出文件。包内 MANIFEST.json 记录所有其他文件摘要；打包时已重新解压并校验。图标与发布资料保留在源工程 release，运行资源不含开发指令、测试样本或内部报告。
