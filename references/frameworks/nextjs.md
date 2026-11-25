# Next.js

## 适用范围与版本

用于已识别的 Next.js 项目或用户明确要求的相关规范。先识别 App Router/Pages Router；缓存默认值随版本变化。

## 工程规则

- **FRAMEWORKS-NEXTJS-001** · RECOMMENDED / SHOULD：服务器端密钥不能进入客户端 bundle；use client 边界最小化。
- **FRAMEWORKS-NEXTJS-002** · RECOMMENDED / SHOULD：请求缓存、动态渲染和失效策略按目标版本显式核验。
- **FRAMEWORKS-NEXTJS-003** · RECOMMENDED / SHOULD：路由错误、loading、not-found 与表单验证保持既有约定。

## 验证方式

运行已有构建和路由测试，检查客户端产物无服务端秘密。

## 最小示例

```tsx
export default function Page() { return <main>Ready</main>; }
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

Router、缓存与部署运行时。

## 官方或原始资料

- [Next.js 资料](https://nextjs.org/docs)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
