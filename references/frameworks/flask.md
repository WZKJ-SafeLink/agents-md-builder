# Flask

## 适用范围与版本

用于已识别的 Flask 项目或用户明确要求的相关规范。按 Flask 与扩展版本核验应用上下文。

## 工程规则

- **FRAMEWORKS-FLASK-001** · RECOMMENDED / SHOULD：复用 app factory/blueprint，避免导入时创建并启动服务。
- **FRAMEWORKS-FLASK-002** · RECOMMENDED / SHOULD：请求资源绑定 teardown；异步支持不能等同 ASGI 原生并发。
- **FRAMEWORKS-FLASK-003** · RECOMMENDED / SHOULD：生产配置不使用开发服务器，模板保持默认转义。

## 验证方式

测试请求上下文、资源关闭和错误处理。

## 最小示例

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

工厂模式与扩展管理。

## 官方或原始资料

- [Flask 资料](https://flask.palletsprojects.com/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
