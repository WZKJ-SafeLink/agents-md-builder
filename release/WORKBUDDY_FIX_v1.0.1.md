# WorkBuddy 目录层级修复 1.0.1

日期：2026-11-24。用户实际反馈1.0.0上传失败：Skill 包仅支持两级目录结构。旧包使用外层技能目录及多级 references/assets，无法满足平台解析限制。

## 已修复

- WorkBuddy ZIP 根直接放 SKILL.md；其余资源至多一层子目录，所有137个成员最多两个路径部分。
- references/assets 按类别前缀展平，完整保留知识库、模板、schema 和脚本。
- 同步改写 Markdown 相对链接、锚点及内联路径，manifest记录资源原路径映射；重名拒绝打包。
- 运行工具兼容源工程与展平布局。解压后的中英文生成结果与源码一致；来源登记、规则迁移和 schema 真实 CLI 已测试。
- 通用 Agent Skills 包保留原有按主题分层布局；发布版本升级为1.0.1，评分规则未改变。

## 实际验证

完整命令 `python3 -m unittest discover -s tests -v`：147项全部通过，失败0、错误0、跳过0，用时5.888秒。原始日志见 [unit-test-output-v1.0.1.txt](unit-test-output-v1.0.1.txt)。

源码 Skill 校验通过；修复包已重新解压，目录深度、Markdown引用、资源完整性、CRC、137个成员的manifest摘要和Python 3.10语法检查通过。结构化结果见 [workbuddy-fix-v1.0.1.json](workbuddy-fix-v1.0.1.json)。

## 上传文件

请使用 [agents-md-builder-workbuddy-v1.0.1.zip](../dist/agents-md-builder-workbuddy-v1.0.1.zip)，大小197957字节。

SHA-256：`1e72b01a9d5442768c9504210c9a631902bb762191c6b16de757f368bfcc49d5`。

直接上传此 ZIP，不要重新添加外层文件夹，不要使用旧1.0.0或通用包。若手动解压安装，创建 agents-md-builder 文件夹后将 ZIP 内容解压到其中。

修复后的1.0.1尚未重新上传到平台，不能宣称平台解析、导入或审核已通过。Windows/Linux原生和完整宿主场景的未验证项仍按原报告保留。
