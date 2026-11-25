# Kotlin

## 适用范围与版本

用于已识别的 Kotlin 项目或用户明确要求的相关规范。按 Gradle Kotlin plugin 与 JVM target 匹配。

## 工程规则

- **LANGUAGES-KOTLIN-001** · RECOMMENDED / SHOULD：优先非空类型；!! 必须有可证实不变量，外部输入通过校验转为领域类型。
- **LANGUAGES-KOTLIN-002** · RECOMMENDED / SHOULD：协程作用域跟随生命周期；取消应传播，不把 CancellationException 当普通失败吞掉。
- **LANGUAGES-KOTLIN-003** · RECOMMENDED / SHOULD：data class 是否用于持久化实体需核验 equals/hashCode 及代理兼容。

## 验证方式

运行现有 Kotlin 测试并验证协程取消和空输入。

## 最小示例

```kotlin
val name: String = input?.trim() ?: return
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

协程调度器与错误模型。

## 官方或原始资料

- [Kotlin 资料](https://kotlinlang.org/docs/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
