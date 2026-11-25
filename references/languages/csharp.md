# C#

## 适用范围与版本

用于已识别的 C# 项目或用户明确要求的相关规范。匹配 TargetFramework、LangVersion 及 nullable。

## 工程规则

- **LANGUAGES-CSHARP-001** · RECOMMENDED / SHOULD：async API 传播 CancellationToken，避免同步阻塞异步调用。
- **LANGUAGES-CSHARP-002** · RECOMMENDED / SHOULD：using/await using 释放资源；DI 管理资源不手动重复 dispose。
- **LANGUAGES-CSHARP-003** · RECOMMENDED / SHOULD：可空引用标注与外部值校验同步维护，不用 ! 隐藏错误。

## 验证方式

运行现有 dotnet test 并检查 nullable 警告。

## 最小示例

```csharp
using var stream = File.OpenRead(path);
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

目标框架和异常契约。

## 官方或原始资料

- [C# 资料](https://learn.microsoft.com/dotnet/csharp/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
