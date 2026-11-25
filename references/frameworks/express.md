# Express

## 适用范围与版本

用于已识别的 Express 项目或用户明确要求的相关规范。Express 4/5 异步异常行为不同。

## 工程规则

- **FRAMEWORKS-EXPRESS-001** · RECOMMENDED / SHOULD：中间件顺序及错误处理器参数必须符合版本契约。
- **FRAMEWORKS-EXPRESS-002** · RECOMMENDED / SHOULD：外部输入先校验，复用请求层；响应结束后不重复发送。
- **FRAMEWORKS-EXPRESS-003** · RECOMMENDED / SHOULD：超时、代理信任和 cookie 安全按部署确认，不无条件 trust proxy。

## 验证方式

验证错误传播、无效输入及反向代理边界。

## 最小示例

```javascript
app.get("/health", (req, res) => res.json({ status: "ok" }));
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

Express 主版本及代理拓扑。

## 官方或原始资料

- [Express 资料](https://expressjs.com/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
