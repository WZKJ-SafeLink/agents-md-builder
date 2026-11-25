# MySQL

## 适用范围与版本

用于已识别的 MySQL 项目或用户明确要求的相关规范。确认服务端与驱动版本；不假定兼容产品等同原产品。

## 工程规则

- **DATABASES-MYSQL-001** · RECOMMENDED / SHOULD：存储引擎、字符集、排序规则和隔离级别显式核验；DDL 不能假定可事务回滚。
- **DATABASES-MYSQL-002** · RECOMMENDED / SHOULD：锁范围与索引相关；死锁重试完整事务，避免跨外部请求持锁。
- **DATABASES-MYSQL-003** · RECOMMENDED / SHOULD：连接生命周期、超时与迁移复用现有设施；输入使用参数化，日志不含连接凭据。
- **DATABASES-MYSQL-004** · RECOMMENDED / SHOULD：租户隔离、约束及索引在目标数据库集成测试，不用内存替身证明生产语义。

## 验证方式

在隔离测试库验证迁移回滚策略、约束、超时与查询计划。

## 最小示例

```sql
EXPLAIN SELECT id FROM items WHERE id = 1;
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

隔离级别、迁移窗口与重试条件。

## 官方或原始资料

- [MySQL 资料](https://dev.mysql.com/doc/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
