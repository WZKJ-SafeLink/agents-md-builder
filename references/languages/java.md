# Java

## 适用范围与版本

用于已识别的 Java 项目或用户明确要求的相关规范。以项目 compiler release/toolchain 为准；不把新 JDK API 引入旧目标。

## 工程规则

- **LANGUAGES-JAVA-001** · RECOMMENDED / SHOULD：新增类型沿用 UpperCamelCase、成员 lowerCamelCase、常量 UPPER_SNAKE_CASE；这是推荐命名，项目既定规范优先。
- **LANGUAGES-JAVA-002** · RECOMMENDED / SHOULD：常量应体现单位和业务语义；禁止用魔法值掩盖边界条件。
- **LANGUAGES-JAVA-003** · RECOMMENDED / SHOULD：集合面向接口声明，明确可变性；并发写用匹配语义的并发集合，不能把普通 HashMap 当线程安全。
- **LANGUAGES-JAVA-004** · RECOMMENDED / SHOULD：使用泛型消除不必要的 raw type；边界与通配符按读写方向设计，不以 unchecked 强转替代类型建模。
- **LANGUAGES-JAVA-005** · RECOMMENDED / SHOULD：Optional 用于表达可缺失返回值；检查空值后再取值，是否用于字段/参数由项目约定，不自动强制。
- **LANGUAGES-JAVA-006** · RECOMMENDED / SHOULD：Stream 管道避免外部共享状态及阻塞副作用；parallelStream 必须先验证线程上下文、执行器和负载。
- **LANGUAGES-JAVA-007** · RECOMMENDED / SHOULD：异常保留原因及业务上下文，不捕获后静默吞掉；受检与运行时异常按接口契约选择。
- **LANGUAGES-JAVA-008** · RECOMMENDED / SHOULD：共享状态必须有可说明的同步策略；线程池容量、队列、拒绝策略及关闭流程应可验证。
- **LANGUAGES-JAVA-009** · RECOMMENDED / SHOULD：日期时间用与业务相符的 Instant/LocalDate/ZonedDateTime，外部边界显式时区。
- **LANGUAGES-JAVA-010** · RECOMMENDED / SHOULD：十进制金额从字符串或精确整数构建 BigDecimal；除法指定舍入策略，compareTo 与 equals 语义不可混用。
- **LANGUAGES-JAVA-011** · RECOMMENDED / SHOULD：资源实现 AutoCloseable 时优先 try-with-resources；I/O 操作有超时，禁止泄漏流和连接。
- **LANGUAGES-JAVA-012** · RECOMMENDED / SHOULD：日志只传脱敏业务标识，不记录凭据；复用已有工具类前先确认语义和依赖版本。
- **LANGUAGES-JAVA-013** · RECOMMENDED / SHOULD：新增逻辑用项目既有单测验证空集合、精度、时间边界和异常；性能优化先保留测量依据。
- **LANGUAGES-JAVA-014** · RECOMMENDED / SHOULD：参考阿里巴巴 Java 手册时按团队选择采用，不能将其全部偏好称为 Java 语言强制标准。

## 验证方式

使用项目 wrapper 编译与单测，检查泛型警告、资源关闭和金额边界。

## 最小示例

```java
BigDecimal amount = new BigDecimal("0.10");
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

是否采用阿里手册、空值策略、包组织和金额精度。

## 官方或原始资料

- [Java 资料](https://docs.oracle.com/javase/specs/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
- [阿里巴巴 Java 开发手册官方仓库](https://github.com/alibaba/p3c)（实践参考，非 Java 语言标准）。
- [BigDecimal Java 21 API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigDecimal.html)（2026-11-24 核验精度及数值构造语义，仅 Java 21）。
