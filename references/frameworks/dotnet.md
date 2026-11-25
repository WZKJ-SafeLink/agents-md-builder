# ASP.NET Core

## 适用范围与版本

用于已识别的 ASP.NET Core 项目或用户明确要求的相关规范。匹配 SDK 与 TargetFramework。

## 工程规则

- **FRAMEWORKS-DOTNET-001** · RECOMMENDED / SHOULD：DI lifetime 不把 scoped 服务捕获进 singleton。
- **FRAMEWORKS-DOTNET-002** · RECOMMENDED / SHOULD：认证中间件与授权策略显式排序，端点检查资源权限。
- **FRAMEWORKS-DOTNET-003** · RECOMMENDED / SHOULD：EF/连接生命周期沿用请求 scope，异步 I/O 传播取消。

## 验证方式

现有集成测试验证权限、中间件和取消。

## 最小示例

```csharp
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

minimal API/Controller 与数据访问方式。

## 官方或原始资料

- [ASP.NET Core 资料](https://learn.microsoft.com/aspnet/core/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
