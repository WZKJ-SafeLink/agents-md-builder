# TypeScript

## 适用范围与版本

用于已识别的 TypeScript 项目或用户明确要求的相关规范。以 tsconfig 与 TypeScript 版本为准。

## 工程规则

- **LANGUAGES-TYPESCRIPT-001** · RECOMMENDED / SHOULD：外部数据先校验再收窄 unknown，不用 any 掩盖边界。
- **LANGUAGES-TYPESCRIPT-002** · RECOMMENDED / SHOULD：保留 tsconfig strict 等既有开关；新增断言说明不变量。
- **LANGUAGES-TYPESCRIPT-003** · RECOMMENDED / SHOULD：类型与运行时校验分离；复用共享 DTO 而非在每个组件复制。

## 验证方式

运行现有类型检查与边界测试，不臆造 tsc 脚本。

## 最小示例

```typescript
function isText(value: unknown): value is string {
  return typeof value === "string";
}
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

严格程度及共享类型归属。

## 官方或原始资料

- [TypeScript 资料](https://www.typescriptlang.org/docs/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
