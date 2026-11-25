# Spring Boot

## 适用范围与版本

用于已识别的 Spring Boot 项目或用户明确要求的相关规范。Boot 2/3/4 的 Java、Jakarta 和 Spring 基线不同，必须匹配项目版本。

## 工程规则

- **FRAMEWORKS-SPRING-BOOT-001** · RECOMMENDED / SHOULD：包结构按真实扫描范围组织，主配置不放 default package；不强制固定层数。
- **FRAMEWORKS-SPRING-BOOT-002** · RECOMMENDED / SHOULD：优先构造器注入表达必需依赖；Bean 生命周期交容器管理，避免手动 new 受管对象。
- **FRAMEWORKS-SPRING-BOOT-003** · RECOMMENDED / SHOULD：外部配置用项目现有 ConfigurationProperties 绑定及参数校验，不把秘密作为默认值。
- **FRAMEWORKS-SPRING-BOOT-004** · RECOMMENDED / SHOULD：Controller 处理传输校验，业务和访问层边界由项目决策；禁止未经授权重构。
- **FRAMEWORKS-SPRING-BOOT-005** · RECOMMENDED / SHOULD：事务边界核实代理、自调用、异常回滚和线程传播，不假定注解总生效。
- **FRAMEWORKS-SPRING-BOOT-006** · RECOMMENDED / SHOULD：全局异常映射保留可追踪标识，日志脱敏；不泄漏栈或 SQL。
- **FRAMEWORKS-SPRING-BOOT-007** · RECOMMENDED / SHOULD：变更自动配置先检查条件和现有 Bean；复用适用版本中的 StringUtils/ObjectUtils/CollectionUtils/NumberUtils 等已有工具。
- **FRAMEWORKS-SPRING-BOOT-008** · RECOMMENDED / SHOULD：测试选择 slice 或集成范围；Actuator 暴露端点与安全授权显式审查，禁止无鉴权暴露敏感端点。

## 验证方式

用项目 wrapper 测试绑定、事务回滚、异常边界和受保护端点。

## 最小示例

```java
@Service
class BillingService {
  BillingService(BillingRepository repository) { this.repository = repository; }
  private final BillingRepository repository;
}
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

包布局、事务策略和工具类采用。

## 官方或原始资料

- [Spring Boot 资料](https://docs.spring.io/spring-boot/reference/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
- [代码结构](https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html)（2026-11-24 核验无强制布局，不指定项目版本）。
