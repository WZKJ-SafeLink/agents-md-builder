# Angular

## 适用范围与版本

用于已识别的 Angular 项目或用户明确要求的相关规范。识别 standalone/NgModule 和版本适用性。

## 工程规则

- **FRAMEWORKS-ANGULAR-001** · RECOMMENDED / SHOULD：沿用现有 DI 与组件边界，不强行迁移所有模块。
- **FRAMEWORKS-ANGULAR-002** · RECOMMENDED / SHOULD：订阅绑定组件销毁生命周期，处理表单校验及错误态。
- **FRAMEWORKS-ANGULAR-003** · RECOMMENDED / SHOULD：模板保持可访问，外部 HTML 不绕过 sanitizer。

## 验证方式

运行项目定义的 Angular 测试与模板检查；signal 示例需版本支持。

## 最小示例

```typescript
readonly items = signal<string[]>([]);
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

响应式模型及路由组织。

## 官方或原始资料

- [Angular 资料](https://angular.dev/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
