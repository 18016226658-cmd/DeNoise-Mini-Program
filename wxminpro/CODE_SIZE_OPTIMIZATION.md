# 代码包大小优化说明

## 问题
代码包大小为 3628 KB，超过 2048 KB 的上限。

## 已完成的优化

### 1. 删除不必要的文件
- ✅ 删除了 `echarts - 副本.js`（重复文件）
- ✅ 删除了 `.map` 文件（源码映射文件，不需要上传）
- ✅ 删除了 `.LICENSE.txt` 文件
- ✅ 删除了 `效果.gif` 和 `效果.htm`（示例文件）
- ✅ 删除了 `echarts-wordcloud/demo` 文件夹（示例代码）

### 2. 配置优化
- ✅ 配置了 `project.config.json` 的 `packOptions.ignore`，忽略不必要的文件
- ✅ 关闭了 `uploadWithSourceMap`（不上传源码映射文件）

### 3. 忽略规则
在 `project.config.json` 中配置了以下忽略规则：
- `**/*.map` - 源码映射文件
- `**/*.LICENSE.txt` - 许可证文件
- `**/demo/**` - 示例代码
- `**/*.gif`, `**/*.htm`, `**/*.html` - 示例文件
- `**/node_modules/**` - 依赖包
- `**/.git/**` - Git 文件
- `**/README.md` - 文档文件

## 进一步优化建议

### 1. 使用 echarts 压缩版本
如果 `echarts.js` 文件仍然很大（>500KB），可以考虑：
- 使用 echarts 的按需引入
- 使用 echarts 的压缩版本（min.js）
- 考虑使用 CDN 加载（需要配置域名白名单）

### 2. 图片资源优化
- 检查 `static/icon/` 和 `static/image/` 中的图片大小
- 压缩图片资源
- 使用 WebP 格式（如果支持）

### 3. 代码压缩
- 确保 `minified: true`（已启用）
- 确保 `minifyWXSS: true`（已启用）
- 确保 `minifyWXML: true`（已启用）

### 4. 分包加载
如果主包仍然过大，可以考虑：
- 将非 tabBar 页面放入分包
- 使用独立分包（independent: true）

## 验证方法

1. 在微信开发者工具中：
   - 点击"上传"按钮
   - 查看代码包大小是否小于 2048 KB

2. 如果仍然超过限制：
   - 检查是否有其他大文件
   - 考虑进一步优化 echarts 库
   - 考虑使用分包

## 注意事项

- `echarts.js` 文件较大是正常的（>500KB），但不应超过 1MB
- 如果使用分包，tabBar 页面必须在主包中
- 确保删除的文件不影响功能

