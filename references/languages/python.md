# Python

## 适用范围与版本

用于已识别的 Python 项目或用户明确要求的相关规范。以 requires-python 和运行环境为准；3.10 无 tomllib 时使用静态降级。

## 工程规则

- **LANGUAGES-PYTHON-001** · RECOMMENDED / SHOULD：PEP 8 是风格指导；保留项目 formatter 配置，不为风格大范围重排。
- **LANGUAGES-PYTHON-002** · RECOMMENDED / SHOULD：公共边界增加可维护类型注解；数据模型显式校验外部值，不把 typing 当运行时校验。
- **LANGUAGES-PYTHON-003** · RECOMMENDED / SHOULD：模块避免导入时执行外部操作；依赖与锁文件一致，不隐式安装包。
- **LANGUAGES-PYTHON-004** · RECOMMENDED / SHOULD：只捕获可处理异常并保留 cause；日志脱敏，不用 print 输出凭据。
- **LANGUAGES-PYTHON-005** · RECOMMENDED / SHOULD：用 pathlib 与 with 管理路径和资源；读取有大小上限。
- **LANGUAGES-PYTHON-006** · RECOMMENDED / SHOULD：async 路径中不直接执行长时间阻塞 I/O；取消和超时传播。
- **LANGUAGES-PYTHON-007** · RECOMMENDED / SHOULD：使用既有 unittest/pytest 组织边界测试；优化前测量，禁止 eval 解析不可信配置。

## 验证方式

在项目支持的 Python 版本执行现有测试，验证异步取消和资源关闭。

## 最小示例

```python
with path.open(encoding="utf-8") as stream:
    text = stream.read(4096)
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

是否采用 dataclass、Pydantic 或其他模型库。

## 官方或原始资料

- [Python 资料](https://docs.python.org/3/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
- [PEP 8](https://peps.python.org/pep-0008/)（2026-11-24 核验风格指导性质）。
