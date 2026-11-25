# Changelog

## Unreleased — 2026-11-25

- Rewrite the default README in English and add complete Japanese and Simplified Chinese versions with language navigation.
- Document installation, working modes, CLI examples, scoring, safety, limitations, contribution guidelines, and both distribution layouts consistently across languages.
- Include every README language and the changelog in both package formats; validate their links after extraction. Keep README.en.md as a compatibility link to the default English README.

## 1.0.1 — 2026-11-24

- 根据用户实际上传错误修复 WorkBuddy 两级目录限制：ZIP 根直接包含 SKILL.md，资源只保留一层目录。
- 按类别前缀展平 references/assets，自动改写文档链接、锚点与资源路径；校验重名和目录深度。
- 运行工具同时支持源码分层和安装包展平布局；对解压后中英文生成、来源登记、schema 及摘要增加回归测试。
- 未重新提交 WorkBuddy，修复后的平台解析与审核仍待用户实际验证。

## 1.0.0 — 2026-11-24

- 新增七种工作模式、按需知识库、规则分类及语义审查输出契约。
- 新增标准库扫描、技术与版本证据、模块及规范发现、惯例抽样。
- 新增 Markdown 校验、结构冲突、部分评分、候选生成、保守去重、diff、profile 更新和规则迁移。
- 新增安全解压、原文摘要覆盖保护、允许清单打包与解压后校验。
- 新增中文/英文说明、WorkBuddy 专用元数据包与真实验证记录。
- 原创内容采用用户确认的 Apache-2.0，发布者 Safe Link；平台实机导入和市场审核未执行。
