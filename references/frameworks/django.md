# Django

## 适用范围与版本

用于已识别的 Django 项目或用户明确要求的相关规范。按锁定 Django 版本检查中间件和异步支持。

## 工程规则

- **FRAMEWORKS-DJANGO-001** · RECOMMENDED / SHOULD：模型变更伴迁移，不在导入时访问数据库。
- **FRAMEWORKS-DJANGO-002** · RECOMMENDED / SHOULD：查询列表用合适 select_related/prefetch_related 验证 N+1。
- **FRAMEWORKS-DJANGO-003** · RECOMMENDED / SHOULD：生产关闭 DEBUG，核实 CSRF、ALLOWED_HOSTS 和认证；不记录 settings 秘密。

## 验证方式

使用项目测试配置检查查询次数与迁移。

## 最小示例

```python
items = Item.objects.select_related("owner").all()
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

应用边界和部署设置来源。

## 官方或原始资料

- [Django 资料](https://docs.djangoproject.com/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
