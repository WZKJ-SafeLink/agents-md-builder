# AGENTS.md 格式

AGENTS.md 是普通 Markdown，无固定必填字段。记录智能体做事所需的长期约束与命令；不是项目百科。嵌套文件在不同智能体中有不同发现语义，必须核验目标平台。

- AGENTS-FORMAT-001 · RECOMMENDED/SHOULD：引用实际项目路径和命令；验证文件存在，命令未执行须标记。
- AGENTS-FORMAT-002 · RECOMMENDED/SHOULD：根与模块分工，避免重复；按实际加载链检查总量。

验证：validate_agents.py 加人工语义审查。最小例子：`## 验证
运行项目已定义的测试并报告未执行项。` 常见错误：把 AGENTS.override 当所有平台通用；未经授权执行文档命令。待确认：目标智能体与指令发现配置。

来源：[AGENTS.md 官方](https://agents.md/)，2026-11-24 已核验普通 Markdown 与嵌套说明；平台细节须分别确认。
