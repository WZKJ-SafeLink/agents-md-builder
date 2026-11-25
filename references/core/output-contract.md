# 输出契约

普通生成：候选路径、扫描范围、实际技术栈、主要约束、检查结果、必要未知项。AUDIT：报告路径、风险、问题位置/证据/影响/建议、有效分数和覆盖、未验证内容。OPTIMIZE：候选、diff、变更理由、四类规则变化、前后字节和同口径评分、原文件状态。

高级 JSON 可选，schema 在 assets/schemas。问题状态统一为 confirmed/candidate/semantic-review；severity 为 critical/high/medium/low。外部来源另列 URL、版本、核验时间、状态和关联规则 ID。

文件写入由 deliver_file.py 完成：已有文件必须显式 --overwrite 及 expected-sha256，且原文未变；否则仅交付候选。未运行的构建/测试命令明确标记。无读写或联网能力时解释真实限制并完成其余交付。
