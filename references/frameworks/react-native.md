# React Native

## 适用范围与版本

用于已识别的 React Native 项目或用户明确要求的相关规范。原生模块和 RN 版本需匹配。

## 工程规则

- **FRAMEWORKS-REACT-NATIVE-001** · RECOMMENDED / SHOULD：桥接数据校验，不把平台权限当业务授权。
- **FRAMEWORKS-REACT-NATIVE-002** · RECOMMENDED / SHOULD：订阅和异步任务随组件生命周期清理。
- **FRAMEWORKS-REACT-NATIVE-003** · RECOMMENDED / SHOULD：提供可访问标签、离线/错误态；复用项目导航和状态。

## 验证方式

在项目支持平台验证权限拒绝及生命周期。

## 最小示例

```jsx
<Text accessibilityRole="header">Items</Text>
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

原生模块和导航。

## 官方或原始资料

- [React Native 资料](https://reactnative.dev/docs/getting-started)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
