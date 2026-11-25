# UniApp

## 适用范围与版本

用于已识别的 UniApp 项目或用户明确要求的相关规范。核实 Vue 版本与编译平台。

## 工程规则

- **FRAMEWORKS-UNIAPP-001** · RECOMMENDED / SHOULD：平台差异通过现有条件编译隔离，不假定所有 API 跨端一致。
- **FRAMEWORKS-UNIAPP-002** · RECOMMENDED / SHOULD：请求层统一错误、登录过期及取消。
- **FRAMEWORKS-UNIAPP-003** · RECOMMENDED / SHOULD：秘密留服务端，页面订阅随生命周期释放。

## 验证方式

在实际目标端验证权限和失败状态。

## 最小示例

```javascript
uni.request({ url, success: handle, fail: report });
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

目标端与分包策略。

## 官方或原始资料

- [UniApp 资料](https://uniapp.dcloud.net.cn/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
