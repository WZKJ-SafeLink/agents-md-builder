# Kafka

## 适用范围与版本

用于已识别的 Kafka 项目或用户明确要求的相关规范。确认客户端与服务端版本、集群模式及托管差异。

## 工程规则

- **MIDDLEWARE-KAFKA-001** · RECOMMENDED / SHOULD：分区决定局部顺序，consumer group 与 rebalance 生命周期明确。
- **MIDDLEWARE-KAFKA-002** · RECOMMENDED / SHOULD：提交 offset 与外部副作用不能自动原子；幂等 producer 或事务不等于任意外部系统端到端恰好一次。
- **MIDDLEWARE-KAFKA-003** · RECOMMENDED / SHOULD：客户端初始化、连接生命周期和超时沿用项目单一设施；重试设置上限、退避与总截止时间，不重试不安全副作用。
- **MIDDLEWARE-KAFKA-004** · RECOMMENDED / SHOULD：日志只写脱敏事件 ID，监控延迟、失败、重试及积压；认证/TLS/ACL 明确；测试断线、重复投递和关闭流程。

## 验证方式

使用该产品匹配版本的隔离集成环境验证失败、重试、幂等和监控；文本流程是验证契约而非可运行 SDK。

## 最小示例

```text
process(record) -> commit offsets after durable success
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

投递语义、超时、幂等存储、重试/死信和连接归属。

## 官方或原始资料

- [Kafka 资料](https://kafka.apache.org/documentation/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
