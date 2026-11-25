# Android

## 适用范围与版本

用于已识别的 Android 项目或用户明确要求的相关规范。检查 minSdk/targetSdk 与 Gradle plugin。

## 工程规则

- **FRAMEWORKS-ANDROID-001** · RECOMMENDED / SHOULD：界面状态绑定 lifecycle，不持有失效 Activity。
- **FRAMEWORKS-ANDROID-002** · RECOMMENDED / SHOULD：运行时权限按最小需要请求，服务端校验身份。
- **FRAMEWORKS-ANDROID-003** · RECOMMENDED / SHOULD：阻塞 I/O 离开主线程，取消可传播。

## 验证方式

使用现有单测/仪器测试验证旋转和权限拒绝。

## 最小示例

```kotlin
viewModelScope.launch { repository.refresh() }
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

UI 工具包及后台任务。

## 官方或原始资料

- [Android 资料](https://developer.android.com/guide)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
