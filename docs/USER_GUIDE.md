# 用户手册

## 安装和输入

安装包含 SKILL.md 的 agents-md-builder 文件夹后，用自然语言请求生成或审查。可输入自然语言需求、授权目录、单份 AGENTS.md、构建配置、项目 ZIP、企业规范、架构说明或代码片段。宿主只拥有附件时仅分析附件，不声称全仓扫描。WorkBuddy 的包与市场操作见 [发布说明](WORKBUDDY_PUBLISH.md)。

## 七种模式

CREATE：描述语言、框架、数据库及已确认约束，智能体提取事实；未知的重要架构决策才询问。DISCOVER：分析现有配置、模块与源码抽样后生成。AUDIT：默认只读，报告位置、风险、影响与建议。OPTIMIZE：保留强制规则，给候选、diff、变更原因和前后同口径评分。HIERARCHY：仅实际技术规则不同的模块生成独立候选。UPDATE：比较历史与当前 profile，再定位旧规范。MIGRATE：分类和过滤参考项目规则，企业要求需目标授权，项目专属规则默认不移植。

## 工具速查

所有工具支持 --help，结构化报告输出到标准输出；--output 只创建新 JSON 文件。退出状态：0 成功；1 校验/确定冲突不通过；2 输入、权限、安全、预算或 I/O 错误。评分成功返回 0 不代表文档优秀。

| 工具 | 主要输入和作用 |
|---|---|
| scan_project.py | --root；受限清单、类型、配置和扫描覆盖 |
| detect_stack.py | --root；技术、版本状态、模块、命令证据 |
| discover_agents.py | --root --target codex --cwd api；项目内有效链，WorkBuddy 加载状态保留 unknown |
| analyze_structure.py | --root；模块与目录角色候选，不保证语义调用图 |
| extract_conventions.py | --root --sample-limit 80；代码习惯观察与多实现候选 |
| validate_agents.py | --file，可加 --root；格式、安全及证据候选 |
| detect_conflicts.py | --rules JSON；明确结构冲突，或 --file 仅文本候选 |
| evaluate_agents.py | --file，可加 --root、--depth、--rules；确定性指标评分与显式冲突风险 |
| generate_agents.py | --root 或 --requirements；--output-dir --language zh/en --hierarchy |
| optimize_agents.py | --file --candidate；同章节精确重复保守合并 |
| generate_diff.py | --before --after；四类规则变化、diff 和前后评分 |
| compare_profiles.py | --before --after；技术版本、模块、架构候选和命令变化 |
| migrate_rules.py | --rules --profile；可选 --authorize-enterprise |
| deliver_file.py | --candidate --target；显式授权后交付 |
| safe_extract.py | --archive --target；向新目录安全解压 |
| check_schema.py | --file --schema；校验内置 schema 使用的子集 |

静态版本识别不解析远程父 POM 或执行动态 Gradle；Python 3.10 使用受限 TOML 静态降级，复杂内容必须人工复核。范围版本、继承版本与 unknown 保持区分。嵌套 fixtures、__fixtures__、testdata、__mocks__ 默认不计入项目技术栈；detect_stack.py 的 --include-fixtures 可显式纳入，或把某个夹具工程直接指定为根。清单扫描仍会计数这些文件。扫描达到上限会标记 truncated，不能把样本当完整项目。

## 创建新项目候选

智能体可把你的自然语言转成如下 JSON，随后调用 generate_agents.py --requirements 生成骨架，并结合知识库完成语义适配。不要把没有证据的命令放入需求 JSON。

```json
{"technologies":[{"name":"java","category":"language","version":"21"},{"name":"spring-boot","category":"framework","version":"unknown"}],"rules":[]}
```

企业规则使用 [规则 schema](../assets/schemas/rule.schema.json)，指定分类、强度、范围、条件、动作和验证。英文本地 CLI 对常见栈提供保守规则子集，宿主按实际需求翻译和补全其他已选知识库。

## 优化与交付

1. 读取原文件，计算原始字节 SHA-256。
2. 在新目录生成候选并进行确定性与语义审查，生成 diff。
3. 用户已明确授权覆盖时执行：

```text
python scripts/deliver_file.py --candidate /reviewed/AGENTS.candidate.md --target /authorized/project/AGENTS.md --overwrite --expected-sha256 原文件的SHA256
```

没有覆盖授权时只交付候选。文件在审查后变更会拒绝替换。默认备份是 AGENTS.md.bak-摘要前12位，也不静默覆盖。新文件可不带 overwrite 创建。工具不会自动替换业务代码。

## 评分与联网

只有 AGENTS.md、没有项目时，项目适配20分为未验证，总评分显示有效得分/80、覆盖率80%和明确标识的参考归一化分。脚本分数是文档特征指标，复杂语义与技术准确性由智能体另审。严重风险不能评为优秀。

联网由宿主使用通用技术词核验官方文档，不发送项目内容。离线继续使用本地参考并注明未经实时核验。不会自动运行发现的脚本、构建钩子或安装依赖。

## 故障处理

输出已存在：使用新文件名，或走显式候选覆盖流程。链接路径被拒绝：改用用户授权范围内的规范化真实路径。扫描截断：按授权调整上限或缩小模块。无 Python：宿主按 SKILL.md 安全采样生成；无写入：直接返回完整 Markdown；无本地目录访问：只使用附件。不要为缺失能力虚构扫描或测试结果。
