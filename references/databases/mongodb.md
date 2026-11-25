# MongoDB

## 适用范围与版本

用于已识别的 MongoDB 项目或用户明确要求的相关规范。确认服务端与驱动版本；不假定兼容产品等同原产品。

## 工程规则

- **DATABASES-MONGODB-001** · RECOMMENDED / SHOULD：按访问模式建复合索引，分页保留稳定排序；无 schema 不代表无输入约束。
- **DATABASES-MONGODB-002** · RECOMMENDED / SHOULD：多文档事务与副本集/分片及驱动版本相匹配，明确 read/write concern。
- **DATABASES-MONGODB-003** · RECOMMENDED / SHOULD：连接生命周期、超时与迁移复用现有设施；输入使用参数化，日志不含连接凭据。
- **DATABASES-MONGODB-004** · RECOMMENDED / SHOULD：租户隔离、约束及索引在目标数据库集成测试，不用内存替身证明生产语义。

## 验证方式

在隔离测试库验证迁移回滚策略、约束、超时与查询计划。

## 最小示例

```sql
db.items.createIndex({ tenantId: 1, externalId: 1 }, { unique: true });
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

隔离级别、迁移窗口与重试条件。

## 官方或原始资料

- [MongoDB 资料](https://www.mongodb.com/docs/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
