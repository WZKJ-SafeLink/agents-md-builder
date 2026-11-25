# AGENTS.md Builder 开发约束

## 职责与边界

本仓库维护可本地安装的 `agents-md-builder` Skill 1.0.0。入口编排智能体的语义工作，Python 工具只负责静态、确定性分析。不得把模式匹配称为完整语义审查。

## Python 开发、编码与文件安全

- 使用 Python 3.10+ 标准库、类型注解及 pathlib；命令行提供 `--help`、UTF-8 JSON 和非零错误状态。
- 必须只读扫描用户指定根目录；不得执行目标项目代码、构建钩子或脚本。不得读取敏感文件，不跟随符号链接或 Windows reparse point。
- 所有读取必须受文件数量、深度、单文件和累计字节预算约束。新增扫描入口复用 `scripts/common.py`。
- 报告仅保留必要的证据路径与定位；对凭据、内网地址及私人信息脱敏。不要添加遥测和项目上传逻辑。
- 写入已有规范前须有显式覆盖授权、原文 SHA-256 校验和原子替换；新建文件须避免竞争覆盖。
- ZIP 先完整验证成员、大小、压缩比和路径，再解压；禁止链接、设备及路径越界。

## Skill 与知识库

- 通用 SKILL.md 仅使用可移植元数据；WorkBuddy 专用元数据由打包配置生成。不要编造发布者。
- 必须按技术栈加载知识库；区分 STANDARD、RECOMMENDED、PROJECT_REQUIRED、USER_REQUIRED、OBSERVED、PROPOSED。观察和建议不能自动变成强制要求。
- 每份技术参考必须包含版本边界、适用条件、稳定规则 ID、验证、最小例子、常见错误、官方来源及待确认决策。
- 官方技术事实必须有来源。联网访问成功只证明入口可访问，不证明所有规则已核实；分别记录两者。
- 不得复制第三方手册；新增内容独立总结。必须维护 THIRD_PARTY_NOTICES.md。

## 验证与发布

- 修改安全、识别、评分或写入逻辑时，为真实边界或回归添加 unittest；测试使用虚构项目和临时目录。
- 运行 `python -m unittest discover -s tests -v`、`python scripts/validate_skill.py --root .` 和打包命令。报告真实通过、失败、跳过数。
- 发布包必须采用允许清单，不包含本开发指令、测试项目、缓存、历史包、环境文件。解压后必须再次校验。
- 修改已发布评分规则时必须更新 scoring_version；修改用户可见行为时必须更新 CHANGELOG.md。发布版本由 VERSION 读取。
- WorkBuddy 实机导入、Windows/Linux 原生运行和真实智能体对照实验未执行时必须如实报告。
