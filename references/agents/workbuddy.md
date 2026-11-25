# WorkBuddy 适配

官方开放平台的 Skill 页面确认 YAML + Markdown、references 和 scripts 资源。市场字段包括 name、display_name、display_name_en、description、description_zh、description_en、version、author。通用 Skill 入口保持 name/description；package_skill.py --platform workbuddy 根据 release/publisher.json 生成市场字段。

- WORKBUDDY-FORMAT-001 · STANDARD/MUST：市场专用包补齐官方要求字段；不能编造作者。
- WORKBUDDY-CAPABILITY-001 · RECOMMENDED/SHOULD：脚本声明不保证本机 Python 已安装；运行时检测，缺失时由智能体降级静态读取。
- WORKBUDDY-LAYOUT-001 · PROJECT_REQUIRED/MUST：提交本产品的 WorkBuddy 包时，SKILL.md 直接置于 ZIP 根，资源只有一层目录。2026-11-24用户实际反馈1.0.0被平台以“两级目录结构”限制拒绝；此约束来源为实际错误，修复包上传尚待复核。

例：python scripts/package_skill.py --root . --platform workbuddy --output dist/agents-md-builder-workbuddy-v1.0.1.zip。验证：本地包校验后人工导入 WorkBuddy；未实测不得声称审核通过。

AGENTS.md 继承、override、上下文上限、ZIP 数值限制、审核时长在本次查阅的官方页面未确认，不能套用 Codex。默认 discover 仅列清单并标记 unknown；需实际产品验证。待确认：安装环境、平台约束与审核资料。

来源：[WorkBuddy 技能官方文档](https://open.workbuddy.cn/docs/skill)，2026-11-24 核验。
