# Ruby

## 适用范围与版本

用于已识别的 Ruby 项目或用户明确要求的相关规范。以 Gemfile 和 .ruby-version 为准。

## 工程规则

- **LANGUAGES-RUBY-001** · RECOMMENDED / SHOULD：不要将不可信字符串传给 eval 或系统命令。
- **LANGUAGES-RUBY-002** · RECOMMENDED / SHOULD：资源使用 block 生命周期；异常不无条件 rescue Exception。
- **LANGUAGES-RUBY-003** · RECOMMENDED / SHOULD：沿用 Bundler 锁定依赖与项目 RuboCop 规则。

## 验证方式

执行已有 test/spec 入口并验证错误路径。

## 最小示例

```ruby
File.open(path, "r:utf-8") { |file| file.read(4096) }
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

Ruby 版本与测试框架。

## 官方或原始资料

- [Ruby 资料](https://docs.ruby-lang.org/en/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
