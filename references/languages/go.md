# Go

## 适用范围与版本

用于已识别的 Go 项目或用户明确要求的相关规范。遵循 go.mod 的 go/toolchain 指令。

## 工程规则

- **LANGUAGES-GO-001** · RECOMMENDED / SHOULD：返回错误包含上下文，避免把预期失败 panic 化。
- **LANGUAGES-GO-002** · RECOMMENDED / SHOULD：请求 context 传至下游并释放 cancel；goroutine 必须有退出路径。
- **LANGUAGES-GO-003** · RECOMMENDED / SHOULD：共享状态用清楚的同步所有权，关闭 channel 由发送方协调。

## 验证方式

项目允许时运行 go test ./... 及 -race；均须记录是否实际执行。

## 最小示例

```go
ctx, cancel := context.WithTimeout(parent, timeout)
defer cancel()
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

错误包装策略和并发所有权。

## 官方或原始资料

- [Go 资料](https://go.dev/doc/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
