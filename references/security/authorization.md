# 授权

## 适用范围与版本

用于已识别的 授权 项目或用户明确要求的相关规范。OWASP 为安全实践参考，实际合规义务需项目另行确认。

## 工程规则

- **SECURITY-AUTHORIZATION-001** · RECOMMENDED / SHOULD：每次操作检查资源归属和动作权限，默认拒绝。
- **SECURITY-AUTHORIZATION-002** · RECOMMENDED / SHOULD：前端按钮隐藏不能替代服务端授权，测试水平越权。

## 验证方式

在授权测试环境覆盖非法、缺失、过期与跨租户输入；不探测真实生产资源。

## 最小示例

```text
principal + action + resource -> policy decision
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

身份/权限模型、保留期限及密钥服务。

## 官方或原始资料

- [授权 资料](https://cheatsheetseries.owasp.org/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
