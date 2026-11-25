# SQL Server

## 适用范围与版本

用于已识别的 SQL Server 项目或用户明确要求的相关规范。确认服务端与驱动版本；不假定兼容产品等同原产品。

## 工程规则

- **DATABASES-SQLSERVER-001** · RECOMMENDED / SHOULD：参数化与连接池复用，隔离级别及快照设置由项目决定。
- **DATABASES-SQLSERVER-002** · RECOMMENDED / SHOULD：索引和参数敏感计划需实际执行计划验证，避免无依据加提示。
- **DATABASES-SQLSERVER-003** · RECOMMENDED / SHOULD：连接生命周期、超时与迁移复用现有设施；输入使用参数化，日志不含连接凭据。
- **DATABASES-SQLSERVER-004** · RECOMMENDED / SHOULD：租户隔离、约束及索引在目标数据库集成测试，不用内存替身证明生产语义。

## 验证方式

在隔离测试库验证迁移回滚策略、约束、超时与查询计划。

## 最小示例

```sql
SELECT id FROM dbo.items WHERE id = @id;
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

隔离级别、迁移窗口与重试条件。

## 官方或原始资料

- [SQL Server 资料](https://learn.microsoft.com/sql/sql-server/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
