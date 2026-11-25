# 微信小程序

## 适用范围与版本

用于已识别的 微信小程序 项目或用户明确要求的相关规范。检查基础库版本与开发者工具配置。

## 工程规则

- **FRAMEWORKS-WECHAT-MINIPROGRAM-001** · RECOMMENDED / SHOULD：appsecret 留在可信服务端，不写入小程序包。
- **FRAMEWORKS-WECHAT-MINIPROGRAM-002** · RECOMMENDED / SHOULD：setData 控制更新量，生命周期内管理订阅和网络请求。
- **FRAMEWORKS-WECHAT-MINIPROGRAM-003** · RECOMMENDED / SHOULD：隐私权限按实际使用能力说明，登录态由服务端校验，不信任客户端身份。

## 验证方式

使用实际工具版本验证基础库兼容及登录过期。

## 最小示例

```javascript
Page({ data: { loading: false } });
```

示例是最小片段或交互契约，不是完整项目；先替换为项目实际类型、接口和版本。

## 常见错误与禁止事项

不得把此参考的建议自动升级为企业强制标准；不要复制不匹配版本的 API，不要忽略上述错误边界或泄漏配置秘密。无项目证据时不得声称验证已经通过。

## 待确认决策

基础库、分包与隐私能力。

## 官方或原始资料

- [微信小程序 资料](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- 适用版本：以项目声明为准；入口可访问性记录见 sources/official-sources.md；规则级资料未经逐项实时核验时保持未验证。
