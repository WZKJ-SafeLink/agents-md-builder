# AGENTS.md

## 项目与适用范围

依据已授权项目的静态证据生成；仅约束此范围的研发行为。架构判断仍需结合业务语义确认。

模块范围：`backend`

## 技术栈证据

- fastapi · 0.115.0 · confirmed · high · 来源：`backend/pyproject.toml` (project/dependencies/fastapi)
- python · unknown · unknown · high · 来源：`backend/pyproject.toml` (project/runtime)

## 适用技术规则（推荐）

- **FRAMEWORKS-FASTAPI-001** · RECOMMENDED / SHOULD：路由定义输入输出模型，禁止无意返回内部敏感字段。
- **FRAMEWORKS-FASTAPI-002** · RECOMMENDED / SHOULD：依赖负责会话生命周期；async endpoint 不直接阻塞 I/O。
- **FRAMEWORKS-FASTAPI-003** · RECOMMENDED / SHOULD：错误统一映射，认证和授权分开；使用项目已有测试客户端版本。
- **LANGUAGES-PYTHON-001** · RECOMMENDED / SHOULD：PEP 8 是风格指导；保留项目 formatter 配置，不为风格大范围重排。
- **LANGUAGES-PYTHON-002** · RECOMMENDED / SHOULD：公共边界增加可维护类型注解；数据模型显式校验外部值，不把 typing 当运行时校验。
- **LANGUAGES-PYTHON-003** · RECOMMENDED / SHOULD：模块避免导入时执行外部操作；依赖与锁文件一致，不隐式安装包。
- **LANGUAGES-PYTHON-004** · RECOMMENDED / SHOULD：只捕获可处理异常并保留 cause；日志脱敏，不用 print 输出凭据。

## 构建、测试与交付验收

- 尚未确认构建和测试命令；不要编造脚本，待项目配置可用后补充并验证。
- 交付时说明改动范围、边界测试及结果；明确报告未执行或失败的检查，不宣称语义审查或命令已经完成。

## 未验证事项

- unknown 版本不得当作最新版本；扫描截断时仅以已有样本作证，版本相关 API 与关键安全配置须进一步核验。
