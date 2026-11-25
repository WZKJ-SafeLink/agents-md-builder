# 测试报告

执行日期：2026-11-24；环境：Darwin，Python 3.11.5。

## 实际自动化结果

命令：`python3 -m unittest discover -s tests -v`

| 测试数 | 成功 | 失败 | 错误 | 跳过 | 用时 |
|---:|---:|---:|---:|---:|---:|
| 140 | 140 | 0 | 0 | 0 | 3.768 s |

完整真实日志见 [unit-test-output.txt](unit-test-output.txt)，结构化结果见 [test-results.json](test-results.json)。最终回归覆盖扫描与忽略、字节/数量预算、敏感与链接保护、manifest 版本和继承、测试夹具技术栈隔离、模块/override、代码惯例、Markdown、安全风险、结构冲突、部分评分、候选生成、中英输出、差异、迁移、更新、授权交付、ZIP 和两种发布包。

## 安全结果

通过：符号链接与硬链接拒绝、Windows reparse point 模拟、路径穿越、Zip Slip、ZIP 链接/碰撞/压缩比/预解析数量限制、超大文件、敏感 include 保护、多行与结构凭据脱敏、私有 URL 脱敏与公共官方引用保留、恶意指令不执行、候选风险拒绝、伪造版本不变成事实、原文覆盖授权与摘要、并发写入拒绝和发布资源凭据候选阻断。

## CLI 与结构

19 个 CLI 均通过 --help；五个实际生成调用在虚构 JPA、Vue、Python、英文 Next.js 和前后端工程中产生7个候选，结果见 [smoke-results.json](smoke-results.json) 与 examples/。19个 CLI 加1个公共模块全部通过 Python 3.10 语法解析，不能据此声称已做3.10原生运行测试。

Skill 自带 validate_skill.py 校验通过，详情见 [skill-validation.json](skill-validation.json)。skill-creator 上游 quick_validate.py 因当前 Python 未安装 PyYAML 无法启动（ModuleNotFoundError: yaml），未安装系统依赖；此项不计作通过，本 Skill 的运行与校验工具均仅用标准库。

单元测试内已真实构建、解压并校验通用与 WorkBuddy 包，检查 manifest 摘要、重复构建一致性及开发文件排除。最终独立构建结果记录在 build-results.json。

## 明确未执行

- 20个宿主场景已写验收契约，并覆盖可自动化的工具断言；没有逐一回放真实宿主对话，不等于20个宿主场景全部通过。
- 未实际导入 WorkBuddy，未提交市场审核，未确认其全部数值限制和 AGENTS.md 加载机制。
- 未做 Windows/Linux 或 Python 3.10 原生运行；Windows junction 只有边界模拟。
- 未做同模型、任务、权限下“无规范 / 通用模板 / 项目定制”的真实智能体对照实验，不提供提升比例。
- 无 Python、无目录访问、无联网等完整宿主降级依照手工场景，未实机回放。

资料入口核验：78个公开地址，72个可访问、6个未验证；入口可访问不代表全部规则逐项核验。详见 references/sources 的登记。
