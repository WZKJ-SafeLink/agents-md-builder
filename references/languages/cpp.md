# C/C++

## 适用范围与版本

用于已识别的 C/C++ 项目或用户明确要求的相关规范。C 标准与 C++ 标准不可混同；查看 CMake 编译选项。

## 工程规则

- **LANGUAGES-CPP-001** · RECOMMENDED / SHOULD：C++ 资源使用 RAII；所有权优先唯一所有权，跨语言接口明确释放方。
- **LANGUAGES-CPP-002** · RECOMMENDED / SHOULD：缓冲区长度与整数转换必须检查；C 接口明确空指针和错误码。
- **LANGUAGES-CPP-003** · RECOMMENDED / SHOULD：禁止通过未定义行为进行性能优化；编译告警与 sanitizer 按现有工具链选择。

## 验证方式

使用项目 CMake/CTest 配置和可用 sanitizer 检查生命周期。

## 最小示例

```cpp
auto handle = std::make_unique<Resource>();
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

异常、RTTI 与 ABI 要求。

## 官方或原始资料

- [C/C++ 资料](https://isocpp.org/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
