# FastAPI

## 适用范围与版本

用于已识别的 FastAPI 项目或用户明确要求的相关规范。检查 FastAPI/Pydantic 主版本和 ASGI 运行时。

## 工程规则

- **FRAMEWORKS-FASTAPI-001** · RECOMMENDED / SHOULD：路由定义输入输出模型，禁止无意返回内部敏感字段。
- **FRAMEWORKS-FASTAPI-002** · RECOMMENDED / SHOULD：依赖负责会话生命周期；async endpoint 不直接阻塞 I/O。
- **FRAMEWORKS-FASTAPI-003** · RECOMMENDED / SHOULD：错误统一映射，认证和授权分开；使用项目已有测试客户端版本。

## 验证方式

验证模型校验、依赖释放、异常和未授权访问。

## 最小示例

```python
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

同步/异步 ORM 和响应模型。

## 官方或原始资料

- [FastAPI 资料](https://fastapi.tiangolo.com/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
