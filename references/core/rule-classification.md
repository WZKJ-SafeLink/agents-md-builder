# 规则数据模型

分类：STANDARD（官方明确约束，必须有准确来源）、RECOMMENDED（可选推荐）、PROJECT_REQUIRED（已确认项目要求）、USER_REQUIRED（本次明示要求）、OBSERVED（观察）、PROPOSED（待确认建议）。强度为 MUST/MUST_NOT/SHOULD/MAY；OBSERVED 和 PROPOSED 不可自动赋 MUST。

结构见 assets/schemas/rule.schema.json。核心字段是稳定 id、title、category、classification、severity、scope（相对路径或技术标签）、condition、requirement、prohibition、exceptions、verification、sources、confidence。对于自动冲突比较，额外使用 key、value、exclusive 和独立边界 independent；只有相同语义 key 才能确定性比较。

例如 key=data-access、value=jpa、scope=[backend]、exclusive=true 表示该作用域独占 JPA。不要仅凭一句话含有 JPA 和 MyBatis 判定冲突。规则 evidence 使用 path 与 locator，不复制源码或秘密。
