# Nuxt

## 适用范围与版本

用于已识别的 Nuxt 项目或用户明确要求的相关规范。Nuxt 2/3/4 的路由、数据和配置 API 不同。

## 工程规则

- **FRAMEWORKS-NUXT-001** · RECOMMENDED / SHOULD：服务端私密 runtimeConfig 不放 public。
- **FRAMEWORKS-NUXT-002** · RECOMMENDED / SHOULD：SSR 请求通过版本对应数据工具处理，避免 hydration 不一致。
- **FRAMEWORKS-NUXT-003** · RECOMMENDED / SHOULD：插件标记客户端/服务端生命周期，复用已有 composable。

## 验证方式

验证 SSR、错误状态和客户端配置边界。

## 最小示例

```vue
<script setup>
const { data, error } = await useFetch("/api/items")
</script>
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

渲染模式和缓存策略。

## 官方或原始资料

- [Nuxt 资料](https://nuxt.com/docs)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
