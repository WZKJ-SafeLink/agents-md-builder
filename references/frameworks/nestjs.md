# NestJS

## 适用范围与版本

用于已识别的 NestJS 项目或用户明确要求的相关规范。核实平台 adapter 与 Nest 主版本。

## 工程规则

- **FRAMEWORKS-NESTJS-001** · RECOMMENDED / SHOULD：模块通过显式 exports/imports 共享 provider，不跨模块绕过边界。
- **FRAMEWORKS-NESTJS-002** · RECOMMENDED / SHOULD：输入 DTO 校验、异常过滤器和 guard 按项目全局策略复用。
- **FRAMEWORKS-NESTJS-003** · RECOMMENDED / SHOULD：provider 生命周期和请求范围需评估，不对所有依赖用 request scope。

## 验证方式

用现有 unit/e2e 测试验证 guard 和校验失败。

## 最小示例

```typescript
@Injectable()
export class ItemsService {}
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

模块边界和传输 adapter。

## 官方或原始资料

- [NestJS 资料](https://docs.nestjs.com/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
