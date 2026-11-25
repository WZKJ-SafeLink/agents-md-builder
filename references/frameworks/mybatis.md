# MyBatis

## 适用范围与版本

用于已识别的 MyBatis 项目或用户明确要求的相关规范。核实 MyBatis 与 Spring 集成版本。

## 工程规则

- **FRAMEWORKS-MYBATIS-001** · RECOMMENDED / SHOULD：外部值用 #{...} 绑定，${...} 标识符仅允许白名单。
- **FRAMEWORKS-MYBATIS-002** · RECOMMENDED / SHOULD：Mapper/resultMap 与列别名一致；动态 SQL 空条件不得变成全表写。
- **FRAMEWORKS-MYBATIS-003** · RECOMMENDED / SHOULD：事务由现有会话/框架管理，关闭手工会话；批处理显式处理失败。

## 验证方式

验证空集合、分页、映射和回滚。

## 最小示例

```xml
<select id="find" resultType="long">SELECT id FROM items WHERE id = #{id}</select>
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

XML/注解风格及分页插件。

## 官方或原始资料

- [MyBatis 资料](https://mybatis.org/mybatis-3/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
