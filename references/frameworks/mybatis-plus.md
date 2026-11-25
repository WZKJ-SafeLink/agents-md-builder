# MyBatis-Plus

## 适用范围与版本

用于已识别的 MyBatis-Plus 项目或用户明确要求的相关规范。根据实际版本核验拦截器顺序及模块拆分。

## 工程规则

- **FRAMEWORKS-MYBATIS-PLUS-001** · RECOMMENDED / SHOULD：复用已有 BaseMapper/Service 扩展，避免重复 CRUD 封装。
- **FRAMEWORKS-MYBATIS-PLUS-002** · RECOMMENDED / SHOULD：Wrapper 来自可信服务逻辑，不接收客户端 SQL 片段。
- **FRAMEWORKS-MYBATIS-PLUS-003** · RECOMMENDED / SHOULD：租户、逻辑删除及乐观锁覆盖自定义 SQL；全表更新保护以实际插件配置为证据。

## 验证方式

测试租户隔离、逻辑删除和无条件写保护。

## 最小示例

```java
mapper.selectById(id);
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

Service 边界与插件启用范围。

## 官方或原始资料

- [MyBatis-Plus 资料](https://baomidou.com/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
