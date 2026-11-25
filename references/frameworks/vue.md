# Vue

## 适用范围与版本

用于已识别的 Vue 项目或用户明确要求的相关规范。Vue 2/3 API、响应性和工具链不同。

## 工程规则

- **FRAMEWORKS-VUE-001** · RECOMMENDED / SHOULD：组件按职责拆分，状态提升和路由遵守现有方案，不自动引入新状态库。
- **FRAMEWORKS-VUE-002** · RECOMMENDED / SHOULD：请求通过已有 API 层，提供 loading/error/empty 及取消；表单校验兼顾服务端错误。
- **FRAMEWORKS-VUE-003** · RECOMMENDED / SHOULD：TypeScript props/emits 明确类型；避免直接修改 props 和不可信 v-html。
- **FRAMEWORKS-VUE-004** · RECOMMENDED / SHOULD：交互提供键盘、标签、焦点及国际化；样式按既有 scoped/utility 方式，优化前测量。

## 验证方式

运行现有组件测试，验证表单错误、空状态和键盘交互。

## 最小示例

```vue
<button type="button" :disabled="loading" @click="submit">{{ label }}</button>
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

Options/Composition API、状态库及 SSR。

## 官方或原始资料

- [Vue 资料](https://vuejs.org/guide/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
