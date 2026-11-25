# 规则编写

重要规则使用稳定大写 ID，例如 JAVA-NAMING-001。修改文案不更换 ID；改变语义需评估新 ID 和迁移。字段按 assets/schemas/rule.schema.json。STANDARD 必须有官方准确来源，推荐实践不是标准；OBSERVED/PROPOSED 不得强制。分类和强度属于不同轴。

规则包含：新增或变更的条件、明确动作、禁止事项、例外和验证；scope 是技术标签或相对目录，路径范围与技术范围须由智能体解释，避免混用。自动冲突比较只在相同 key、有交叠路径范围且具明确 value/exclusive 时确认；复杂技术标签交集另行语义审查。

```json
{"id":"JAVA-NAMING-001","title":"Class naming","category":"naming","classification":"RECOMMENDED","severity":"SHOULD","scope":["java"],"condition":"Adding a Java class","requirement":"Follow the existing peer class naming convention","prohibition":[],"exceptions":[],"verification":{"type":"review","description":"Inspect the new class name and peer examples"},"sources":[],"confidence":"high"}
```

知识库每篇写清版本边界、工程约束、验证、最小例子、错误、禁止事项、来源和待确认决策。Maven/Gradle 等动态值无法解析时保留 unknown。添加 STANDARD 前查官方对应版本，不拿社区博客作为唯一依据；URL 可访问和规则已核验分别登记。

参考规范迁移需标记 migration_class 为 general、technology、enterprise、project、inapplicable，并在 technologies 标记适用栈。默认不迁移企业/项目专属内容；迁移前移除私有地址及秘密，公共来源只保留已确认官方域名。
