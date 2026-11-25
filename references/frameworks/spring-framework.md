# Spring Framework

## 适用范围与版本

用于已识别的 Spring Framework 项目或用户明确要求的相关规范。Spring 5/6/7 基线及 Jakarta 迁移需匹配。

## 工程规则

- **FRAMEWORKS-SPRING-FRAMEWORK-001** · RECOMMENDED / SHOULD：容器依赖沿用现有配置，不重复创建基础设施 Bean。
- **FRAMEWORKS-SPRING-FRAMEWORK-002** · RECOMMENDED / SHOULD：代理能力检查可见性、自调用和线程边界。
- **FRAMEWORKS-SPRING-FRAMEWORK-003** · RECOMMENDED / SHOULD：请求校验、异常转换和资源生命周期采用已有项目机制。

## 验证方式

容器测试验证代理入口和资源关闭。

## 最小示例

```java
class Service { Service(Repository repository) {} }
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

Bean 配置和代理方式。

## 官方或原始资料

- [Spring Framework 资料](https://docs.spring.io/spring-framework/reference/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
