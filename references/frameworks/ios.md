# iOS

## 适用范围与版本

用于已识别的 iOS 项目或用户明确要求的相关规范。按 deployment target 和 Swift 版本适配。

## 工程规则

- **FRAMEWORKS-IOS-001** · RECOMMENDED / SHOULD：UI 操作位于主 actor，任务随界面取消。
- **FRAMEWORKS-IOS-002** · RECOMMENDED / SHOULD：凭据使用系统安全存储，避免明文 UserDefaults。
- **FRAMEWORKS-IOS-003** · RECOMMENDED / SHOULD：权限说明与实际能力相符，测试拒绝路径。

## 验证方式

使用项目模拟器测试生命周期与权限。

## 最小示例

```swift
@MainActor func updateView() {}
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

UIKit/SwiftUI 和最低系统版本。

## 官方或原始资料

- [iOS 资料](https://developer.apple.com/documentation/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
