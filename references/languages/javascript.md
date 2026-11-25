# JavaScript

## 适用范围与版本

用于已识别的 JavaScript 项目或用户明确要求的相关规范。区分 Node/浏览器与 ESM/CommonJS。

## 工程规则

- **LANGUAGES-JAVASCRIPT-001** · RECOMMENDED / SHOULD：沿用现有模块系统，不无意混用 require 与 import。
- **LANGUAGES-JAVASCRIPT-002** · RECOMMENDED / SHOULD：Promise 拒绝必须可追踪；异步操作处理 loading/error/empty 状态。
- **LANGUAGES-JAVASCRIPT-003** · RECOMMENDED / SHOULD：不把外部字符串插入可执行 HTML；复用已有请求层和异常模型。

## 验证方式

执行 package.json 已有 lint/test；验证失败请求。

## 最小示例

```javascript
const data = await response.json();
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

运行时目标、模块与格式化策略。

## 官方或原始资料

- [JavaScript 资料](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
