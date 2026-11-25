# Rust

## 适用范围与版本

用于已识别的 Rust 项目或用户明确要求的相关规范。遵循 Cargo edition、rust-version 和锁文件。

## 工程规则

- **LANGUAGES-RUST-001** · RECOMMENDED / SHOULD：外部失败返回 Result；生产路径 unwrap 需要不变量依据。
- **LANGUAGES-RUST-002** · RECOMMENDED / SHOULD：unsafe 必须说明安全前提，提供相应边界测试。
- **LANGUAGES-RUST-003** · RECOMMENDED / SHOULD：避免为逃避借用检查无差别 clone；明确资源与并发所有权。

## 验证方式

使用已有 cargo test/fmt/clippy 配置；验证错误分支。

## 最小示例

```rust
fn parse(value: &str) -> Result<u64, std::num::ParseIntError> { value.parse() }
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

MSRV 和异步运行时。

## 官方或原始资料

- [Rust 资料](https://doc.rust-lang.org/book/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
