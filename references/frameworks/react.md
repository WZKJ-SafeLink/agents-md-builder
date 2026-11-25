# React

## 适用范围与版本

用于已识别的 React 项目或用户明确要求的相关规范。以项目 React 与渲染框架版本为准。

## 工程规则

- **FRAMEWORKS-REACT-001** · RECOMMENDED / SHOULD：组件和 hook 职责清晰；共享状态用现有策略，不新增平行 store。
- **FRAMEWORKS-REACT-002** · RECOMMENDED / SHOULD：Effect 处理外部同步及清理，异步取消或忽略过期响应；不直接修改 state。
- **FRAMEWORKS-REACT-003** · RECOMMENDED / SHOULD：API 与 TypeScript 模型复用，表单同时处理校验、错误、空与加载态。
- **FRAMEWORKS-REACT-004** · RECOMMENDED / SHOULD：使用语义 HTML 和可访问标签、国际化；不向 dangerouslySetInnerHTML 注入外部值，性能优化先测量。

## 验证方式

组件测试验证重渲染、失败请求、空结果和键盘操作。

## 最小示例

```jsx
<button type="button" disabled={loading} onClick={submit}>{label}</button>
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

客户端/服务端边界和状态管理。

## 官方或原始资料

- [React 资料](https://react.dev/learn)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
