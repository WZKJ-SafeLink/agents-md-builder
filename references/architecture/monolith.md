# 单体

## 适用范围与版本

用于已识别的 单体 项目或用户明确要求的相关规范。架构模式是设计参考，不是正式强制标准；需项目边界证据。

## 工程规则

- **ARCHITECTURE-MONOLITH-001** · RECOMMENDED / SHOULD：部署与进程边界必须有配置证据，目录数量不等于服务数量。
- **ARCHITECTURE-MONOLITH-002** · RECOMMENDED / SHOULD：模块交互遵守已有接口，不为生成规范引入网络拆分。
- **ARCHITECTURE-MONOLITH-003** · RECOMMENDED / SHOULD：新增跨边界依赖前查现有调用锚点；迁移架构须用户明确决策，观察不自动强制。

## 验证方式

用现有依赖图、架构测试和集成测试验证调用方向；无工具时做静态抽样并注明范围。

## 最小示例

```text
feature -> application interface -> persistence
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

模块职责、依赖方向和一致性边界。

## 官方或原始资料

- [单体 资料](https://martinfowler.com/architecture/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
