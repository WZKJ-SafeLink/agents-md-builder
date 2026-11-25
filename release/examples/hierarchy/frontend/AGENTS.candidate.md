# AGENTS.md

## 项目与适用范围

依据已授权项目的静态证据生成；仅约束此范围的研发行为。架构判断仍需结合业务语义确认。

模块范围：`frontend`

## 技术栈证据

- vue · 3.5.0 · confirmed · high · 来源：`frontend/package.json` (dependencies/vue)
- javascript · unknown · unknown · high · 来源：`frontend/package.json` (package.json)
- typescript · 5.6.0 · confirmed · high · 来源：`frontend/package.json` (dependencies/typescript)

## 适用技术规则（推荐）

- **FRAMEWORKS-VUE-001** · RECOMMENDED / SHOULD：组件按职责拆分，状态提升和路由遵守现有方案，不自动引入新状态库。
- **FRAMEWORKS-VUE-002** · RECOMMENDED / SHOULD：请求通过已有 API 层，提供 loading/error/empty 及取消；表单校验兼顾服务端错误。
- **FRAMEWORKS-VUE-003** · RECOMMENDED / SHOULD：TypeScript props/emits 明确类型；避免直接修改 props 和不可信 v-html。
- **FRAMEWORKS-VUE-004** · RECOMMENDED / SHOULD：交互提供键盘、标签、焦点及国际化；样式按既有 scoped/utility 方式，优化前测量。
- **LANGUAGES-JAVASCRIPT-001** · RECOMMENDED / SHOULD：沿用现有模块系统，不无意混用 require 与 import。
- **LANGUAGES-JAVASCRIPT-002** · RECOMMENDED / SHOULD：Promise 拒绝必须可追踪；异步操作处理 loading/error/empty 状态。
- **LANGUAGES-JAVASCRIPT-003** · RECOMMENDED / SHOULD：不把外部字符串插入可执行 HTML；复用已有请求层和异常模型。
- **LANGUAGES-TYPESCRIPT-001** · RECOMMENDED / SHOULD：外部数据先校验再收窄 unknown，不用 any 掩盖边界。
- **LANGUAGES-TYPESCRIPT-002** · RECOMMENDED / SHOULD：保留 tsconfig strict 等既有开关；新增断言说明不变量。
- **LANGUAGES-TYPESCRIPT-003** · RECOMMENDED / SHOULD：类型与运行时校验分离；复用共享 DTO 而非在每个组件复制。

## 构建、测试与交付验收

- `npm run test` · 工作目录：`frontend` · all · 未执行，证据：`frontend/package.json`
- 交付时说明改动范围、边界测试及结果；明确报告未执行或失败的检查，不宣称语义审查或命令已经完成。

## 未验证事项

- unknown 版本不得当作最新版本；扫描截断时仅以已有样本作证，版本相关 API 与关键安全配置须进一步核验。
