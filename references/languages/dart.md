# Dart

## 适用范围与版本

用于已识别的 Dart 项目或用户明确要求的相关规范。匹配 pubspec SDK 约束。

## 工程规则

- **LANGUAGES-DART-001** · RECOMMENDED / SHOULD：保持空安全边界，外部 JSON 做类型和字段校验。
- **LANGUAGES-DART-002** · RECOMMENDED / SHOULD：Future 错误应进入状态或异常边界，关闭 stream/subscription。
- **LANGUAGES-DART-003** · RECOMMENDED / SHOULD：不为数据模型引入第二套并行风格，复用项目序列化。

## 验证方式

执行项目现有 dart analyze/test。

## 最小示例

```dart
final name = json["name"];
if (name is! String) throw FormatException("name");
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

序列化和并发 isolate 需求。

## 官方或原始资料

- [Dart 资料](https://dart.dev/guides)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
