# Codex 指令加载

2026-11-24 核验官方说明：项目从根到工作目录逐级取文件，每目录优先非空 AGENTS.override.md，再 AGENTS.md，再配置的 fallback；最多选一个。深层指令在组合顺序中靠后。全局配置不在项目扫描授权范围内，不自动读取。

- CODEX-CHAIN-001 · STANDARD/MUST：分析同目录 override 与普通文件时按上述选择，不把两者都计入有效链。
- CODEX-BUDGET-001 · RECOMMENDED/SHOULD：默认 project_doc_max_bytes 为 32 KiB，可配置；它不是本 Skill 的扫描预算。最终以用户实际版本和配置为准。

例：根 AGENTS.md + api/AGENTS.override.md → api 工作目录有效链。验证：discover_agents.py --target codex --cwd api；只能推导授权项目内链，宿主全局及真实加载需实机验证。常见错误：漏记全局未扫描，或对兄弟目录全量累计。待确认：fallback 名称和预算是否被用户改写。

来源：[Codex 官方文档](https://developers.openai.com/codex/guides/agents-md/)，重定向入口正常，核验日期 2026-11-24。
