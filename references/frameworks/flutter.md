# Flutter

## 适用范围与版本

用于已识别的 Flutter 项目或用户明确要求的相关规范。依据 Flutter/Dart SDK 约束。

## 工程规则

- **FRAMEWORKS-FLUTTER-001** · RECOMMENDED / SHOULD：Widget 不承担长生命周期 I/O；状态及导航复用项目方案。
- **FRAMEWORKS-FLUTTER-002** · RECOMMENDED / SHOULD：dispose 控制器和订阅，异步回调检查生命周期。
- **FRAMEWORKS-FLUTTER-003** · RECOMMENDED / SHOULD：交互有 loading/error/empty、语义标签和国际化。

## 验证方式

运行现有 widget/integration 测试并检查屏幕阅读器语义。

## 最小示例

```dart
if (!mounted) return;
setState(() { loading = false; });
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

状态方案和目标平台。

## 官方或原始资料

- [Flutter 资料](https://docs.flutter.dev/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
