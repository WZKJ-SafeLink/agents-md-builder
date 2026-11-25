# Spring Data JPA

## 适用范围与版本

用于已识别的 Spring Data JPA 项目或用户明确要求的相关规范。javax/jakarta 与 Hibernate 主版本必须匹配；最新文档不可代替项目版。

## 工程规则

- **FRAMEWORKS-SPRING-DATA-JPA-001** · RECOMMENDED / SHOULD：Entity 明确 ID 与映射，关系 owning side 与级联、orphanRemoval 经领域语义确认。
- **FRAMEWORKS-SPRING-DATA-JPA-002** · RECOMMENDED / SHOULD：Repository 查询方法、JPQL 和 Specification 复用项目查询约定，参数绑定不拼接输入。
- **FRAMEWORKS-SPRING-DATA-JPA-003** · RECOMMENDED / SHOULD：分页必须稳定排序；大数据集评估 keyset，不无界 findAll。
- **FRAMEWORKS-SPRING-DATA-JPA-004** · RECOMMENDED / SHOULD：Lazy Loading 在明确事务范围内处理，不依赖序列化触发加载；不要用全局 EAGER 处理 N+1。
- **FRAMEWORKS-SPRING-DATA-JPA-005** · RECOMMENDED / SHOULD：N+1 用查询数量测试及实际执行计划验证，按场景选择 fetch join/entity graph；集合 fetch 与分页需单独核验。
- **FRAMEWORKS-SPRING-DATA-JPA-006** · RECOMMENDED / SHOULD：批处理考虑持久化上下文、flush/clear 与 bulk DML 失效缓存，不假定 saveAll 等于批量 SQL。
- **FRAMEWORKS-SPRING-DATA-JPA-007** · RECOMMENDED / SHOULD：事务入口明确，声明的查询方法和自定义实现需核验事务；readOnly 不是安全写入禁止。
- **FRAMEWORKS-SPRING-DATA-JPA-008** · RECOMMENDED / SHOULD：并发更新按需使用 @Version 并验证冲突；索引由查询计划和迁移管理。
- **FRAMEWORKS-SPRING-DATA-JPA-009** · RECOMMENDED / SHOULD：审计字段与软删除隔离跨租户查询；API DTO 与实体隔离由项目策略确定，避免泄漏懒加载关系。

## 验证方式

使用目标数据库集成测试验证回滚、分页、查询次数及乐观锁。

## 最小示例

```java
@Version
private Long version;
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

实体/API 隔离、ID 生成、审计、软删除及分页策略。

## 官方或原始资料

- [Spring Data JPA 资料](https://docs.spring.io/spring-data/jpa/reference/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
- [事务](https://docs.spring.io/spring-data/jpa/reference/jpa/transactions.html)（2026-11-24 核验继承 CRUD 与自定义查询事务区别，仍需匹配项目版）。
