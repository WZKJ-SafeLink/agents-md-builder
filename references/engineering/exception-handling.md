# 异常

## 适用范围与版本

用于已识别的 异常 项目或用户明确要求的相关规范。推荐实践随项目工具版本与既有策略适配，不要求安装未存在的工具。

## 工程规则

- **ENGINEERING-EXCEPTION-HANDLING-001** · RECOMMENDED / SHOULD：在可恢复边界处理异常；保留 cause，避免 catch 后返回伪成功。
- **ENGINEERING-EXCEPTION-HANDLING-002** · RECOMMENDED / SHOULD：面向用户错误与内部日志分开，错误码和关联 ID 复用现有机制。

## 验证方式

以现有项目命令或差异检查验证上述行为；无法执行时标记未验证。

## 最小示例

```python
raise DomainError("invalid state") from error
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

团队已有约定、工具和变更权限。

## 官方或原始资料

- [异常 资料](https://docs.python.org/3/tutorial/errors.html)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
