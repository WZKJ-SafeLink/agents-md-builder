# 多租户

## 适用范围与版本

用于已识别的 多租户 项目或用户明确要求的相关规范。OWASP 为安全实践参考，实际合规义务需项目另行确认。

## 工程规则

- **SECURITY-MULTI-TENANCY-001** · RECOMMENDED / SHOULD：租户身份来自可信认证上下文，不信任请求中任意 tenantId。
- **SECURITY-MULTI-TENANCY-002** · RECOMMENDED / SHOULD：数据库、缓存、消息和导出均验证租户隔离，覆盖管理端例外授权。

## 验证方式

在授权测试环境覆盖非法、缺失、过期与跨租户输入；不探测真实生产资源。

## 最小示例

```sql
SELECT id FROM items WHERE tenant_id = ? AND id = ?
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

身份/权限模型、保留期限及密钥服务。

## 官方或原始资料

- [多租户 资料](https://cheatsheetseries.owasp.org/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
