# Swift

## 适用范围与版本

用于已识别的 Swift 项目或用户明确要求的相关规范。按 tools-version 与部署目标检查 API availability。

## 工程规则

- **LANGUAGES-SWIFT-001** · RECOMMENDED / SHOULD：用 optional 表达缺失，避免外部输入强制解包。
- **LANGUAGES-SWIFT-002** · RECOMMENDED / SHOULD：UI 更新保持主 actor；任务取消沿调用链处理。
- **LANGUAGES-SWIFT-003** · RECOMMENDED / SHOULD：闭包捕获确认生命周期，避免不必要 retain cycle。

## 验证方式

使用项目 SwiftPM/Xcode 测试并覆盖取消与空输入。

## 最小示例

```swift
guard let value = input else { return }
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

actor 隔离与部署目标。

## 官方或原始资料

- [Swift 资料](https://www.swift.org/documentation/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
