# PHP

## 适用范围与版本

用于已识别的 PHP 项目或用户明确要求的相关规范。遵循 composer PHP 约束。

## 工程规则

- **LANGUAGES-PHP-001** · RECOMMENDED / SHOULD：输入通过校验后进入领域层，SQL 使用参数绑定。
- **LANGUAGES-PHP-002** · RECOMMENDED / SHOULD：异常在统一边界映射，避免输出堆栈及配置秘密。
- **LANGUAGES-PHP-003** · RECOMMENDED / SHOULD：复用 Composer 自动加载和项目格式化规范。

## 验证方式

运行已有 composer test 或实际测试入口。

## 最小示例

```php
$statement = $pdo->prepare("SELECT id FROM items WHERE id = ?");
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

strict_types 和框架容器规则。

## 官方或原始资料

- [PHP 资料](https://www.php.net/manual/en/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
