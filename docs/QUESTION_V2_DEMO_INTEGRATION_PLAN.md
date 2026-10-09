# 《月森关系地图》V2 题目与 24 张场景图接入 Demo 完整方案

> 文档状态：执行方案 / 2026-08-31  
> 项目源码：`/Users/cc/Documents/情感测试/personality-miniapp`  
> 微信开发者工具项目：`/Users/cc/WeChatProjects/miniprogram-3`  
> 云环境：`cloud1-d1gt8iwo343dfe428`  
> 云托管服务：`personality-api`

## 1. 目标与完成标准

把已经确认的 24 张绘本场景图和 `docs/QUESTION_COPY_V2.md` 中的 24 道题接入现有 Demo，同时保持以下边界：

1. A 用户完成 24 题、生成 Mock 结果、邀请 B、B 完成 24 题、生成双人 Mock 关系报告的主链路继续可用。
2. 答题页改为全屏绘本场景；题目和四个选项由 WXML/WXSS 渲染，不烘焙到图片里。
3. 四个选项使用不对称道路分枝式排版，不做四张封闭卡片，也不做蝴蝶翅膀式对称构图。
4. 图片、题目和题号由显式 manifest/metadata 关联，不依赖 `scene-v1/v2/v3` 猜测。
5. 新题库使用新的 `TestVersion`，不原地改写已有答题会话所引用的 V1。
6. 数据发布使用 Django Migration；Mock 评分和 Mock 关系报告仍集中在 Engine，不提前实现正式算法或 AI 报告。
7. 开发者工具能编译；真机能加载图片、连续快速答题、提交结果，并能继续完成双人链路。

## 2. 已确认事实与暂未验证事项

### 2.1 已确认

- 24 个题号目录均存在：`miniapp/assets/questions/q01` 至 `q24`。
- 已选定 24 张高清母图，文件均存在，总体积约 59.7 MB。
- `QUESTION_COPY_V2.md` 包含 Q01–Q24，每题均有 A/B/C/D 四个选项。
- Demo 源码会通过 `scripts/sync_miniprogram3.sh` 编译 TypeScript，再同步到 `miniprogram-3/miniprogram`。
- `miniprogram-3/project.config.json` 的 AppID 为 `wx5e14dc6e44274be6`。
- 小程序配置指向云环境 `cloud1-d1gt8iwo343dfe428` 和服务 `personality-api`，使用 `wx.cloud.callContainer`。
- 用户此前已在开发者工具控制台调用 `/api/v1/health` 得到 HTTP 200，并已跑通真机主链路。

### 2.2 本轮尚不能视为已确认

- 当前线上容器是否仍运行最新代码，本轮尚未重新部署和健康检查。
- 当前线上数据库是否已经存在用户答题数据，不能直接假设为空。
- 24 张图片叠加真实文字后的逐题真机可读性尚未验证。
- 微信上传包最终大小、不同机型裁切和弱网加载需要在接入后实测。

## 3. 正式母图清单

母图保留在原目录，不覆盖、不删除历史版本。发布版统一输出为 `scene.jpg`，由脚本生成。

| 题号 | 本轮选定母图 | 说明 |
|---|---|---|
| Q01 | `miniapp/assets/questions/q01/scene-v2.png` | 修正版，避免与 Q07 重复 |
| Q02 | `miniapp/assets/questions/q02/scene-v1.png` | 当前确认版 |
| Q03 | `miniapp/assets/questions/q03/scene-v4.png` | 修正版，海豚＋水獭 |
| Q04 | `miniapp/assets/questions/q04/scene-v1.png` | 当前确认版 |
| Q05 | `miniapp/assets/questions/q05/scene-v2.png` | 当前确认版 |
| Q06 | `miniapp/assets/questions/q06/scene-v1.png` | 当前确认版 |
| Q07 | `miniapp/assets/questions/q07/scene-v1.png` | 视觉基准版 |
| Q08 | `miniapp/assets/questions/q08/scene-v3.png` | 修正版，棕熊＋鹿 |
| Q09 | `miniapp/assets/questions/q09/scene-v1.png` | 当前确认版 |
| Q10 | `miniapp/assets/questions/q10/scene-v1.png` | 当前确认版 |
| Q11 | `miniapp/assets/questions/q11/scene-v1.png` | 当前确认版 |
| Q12 | `miniapp/assets/questions/q12/scene-v1.png` | 当前确认版 |
| Q13 | `miniapp/assets/questions/q13/scene-v1.png` | 当前确认版 |
| Q14 | `miniapp/assets/questions/q14/scene-v1.png` | 当前确认版 |
| Q15 | `miniapp/assets/questions/q15/scene-v1.png` | 当前确认版 |
| Q16 | `miniapp/assets/questions/q16/scene-v1.png` | 当前确认版 |
| Q17 | `miniapp/assets/questions/q17/scene-v1.png` | 当前确认版 |
| Q18 | `miniapp/assets/questions/q18/scene-v1.png` | 当前确认版 |
| Q19 | `miniapp/assets/questions/q19/scene-v1.png` | 当前确认版 |
| Q20 | `miniapp/assets/questions/q20/scene-v4.png` | 修正版，企鹅＋河狸 |
| Q21 | `miniapp/assets/questions/q21/scene-v2.png` | 当前确认版 |
| Q22 | `miniapp/assets/questions/q22/scene-v1.png` | 当前确认版 |
| Q23 | `miniapp/assets/questions/q23/scene-v1.png` | 当前确认版 |
| Q24 | `miniapp/assets/questions/q24/scene-v1.png` | 当前确认版 |

## 4. 资源发布策略

### 4.1 为什么不能直接打包 PNG 母图

24 张选定 PNG 合计约 59.7 MB，不能作为普通小程序代码包资源直接发布。母图用于长期保存，运行时使用压缩后的 JPEG 发布版。此前 WebP 在开发者工具可显示，但真机只显示文字，因此运行格式改为兼容性更稳的 JPEG。

### 4.2 发布版输出

- 输入：第 3 节的 24 张 PNG 母图。
- 输出：`miniapp/assets/questions/q01/scene.jpg` 至 `q24/scene.jpg`。
- 所有发布图统一尺寸和编码参数。
- 建立 `miniapp/assets/questions/manifest.ts`，保存题目 sequence、场景 key、运行时路径、点缀和动效预设。
- 同步脚本只把运行需要的 `scene.jpg` 带入开发者工具项目，不同步 `scene-v*.png` 母图和旧 WebP。
- 目标是在清晰度可接受的前提下尽量控制整个小程序包体；若主包仍超限，再改为题目分包或云存储，不偷偷降低到明显糊图。

### 4.3 加载策略

- 当前题只绑定一张场景图。
- 当前题显示后预加载下一题；不在首屏同时创建 24 个 image 节点。
- 图片加载失败时显示低体积月森渐变占位，不阻断答题和保存。
- 使用本地资源时不依赖手机网络；API 仍通过云托管调用。

## 5. 题库 V2 数据策略

### 5.1 版本边界

- 保留现有 `hidden-personality` 测试与 V1，避免已有会话引用的题目被改写。
- 新建 V2，包含新的测试名称、说明、24 道题和 96 个选项。
- V2 的 `Question.metadata` 保存 `scene_key`、`scene_asset`、`motion_preset`、章节等展示信息。
- 发布 V2 后，新的测试会话使用 V2；已创建的 V1 会话仍能继续读取 V1。

### 5.2 数据写入方式

- 使用 Django Data Migration 创建并发布 V2，满足“所有数据库变化使用 Django Migration”的要求。
- `seed_demo` 改为可重复执行的开发初始化入口，但不能覆盖已发布历史版本。
- Migration 和 seed 共享经过测试的内容定义时，应确保 migration 的历史数据不会因以后修改常量而漂移。

### 5.3 评分边界

- 本轮不设计正式人格算法。
- 新选项的 `score_config` 继续为空或仅保存非正式内容键；MockScoringEngine 维持确定性 Demo 行为。
- 不根据单题直接给动物标签，不在前端写人格判断。

## 6. 答题页实现方案

### 6.1 页面层级

从后到前：

1. 全屏 `image` 场景层，使用 `aspectFill`。
2. 顶部轻量进度区：章节、`Qxx/24`、进度线。
3. 下半部暖象牙色半透明雾层，只用于提高文字可读性，不使用明显边框或重毛玻璃。
4. 题目区。
5. 四个道路分枝式选项。
6. 选中反馈：珊瑚色文字、小对勾、3–5 个脚印；约 320–420ms 后进入下一题。
7. 底部“上一题”和自动保存状态。

### 6.2 道路分枝排版

- 四项采用错位排列：左、右、略偏左、略偏右，不做严格镜像。
- 每个选项没有封闭卡片外框；使用细路径、短枝叶线稿或微弱底色保证点击范围。
- 选项点击区域仍需足够大，视觉无框不等于触控面积缩小。
- 长文本允许两行，但不能遮挡主要动物；极窄设备必要时缩小间距而不是裁掉文字。

### 6.3 交互与稳定性

- 保留现有快速点击锁、旧题点击事件校验、等待最后一次保存后再提交等修复。
- 切题前先完成本地选中动画；接口失败时恢复之前答案并留在当前题。
- 允许返回上一题修改答案；修改后 `answeredCount` 不重复增加。
- 最后一题动画结束后，提交按钮进入可点击状态。

## 7. 代码改动范围

### 7.1 小程序源码

- `miniapp/assets/questions/manifest.ts`：新建正式资源清单。
- `miniapp/pages/test-run/index.ts`：绑定 metadata、图片加载状态、下一题预取与现有保存逻辑。
- `miniapp/pages/test-run/index.wxml`：改为场景式页面结构。
- `miniapp/pages/test-run/index.wxss`：实现全屏绘本、雾层、道路分枝和选中动效。
- `miniapp/pages/test-run/index.json`：按需要调整导航栏样式。
- `miniapp/types/index.ts`：补全 Question metadata 类型。
- `scripts/sync_miniprogram3.sh`：只同步发布图，排除高清母图。

### 7.2 后端

- 新增 V2 内容定义及数据校验。
- 新增 Django Data Migration 创建 V2。
- 调整 `seed_demo`，确保新安装和迁移后的环境一致且幂等。
- 增加题库 V2、场景 metadata、24×4 选项和旧会话兼容测试。

### 7.3 文档

- 更新 README：发布图生成、迁移、云托管重新部署、同步开发者工具和真机验收。
- 更新场景验收报告：标记 Q01/Q03/Q08/Q20 已修正，并记录工程接入状态。

## 8. 分阶段执行与每阶段测试

### Phase A：资源清单和发布图

1. 创建 manifest。
2. 生成 24 张统一规格 WebP。
3. 校验题号连续、每题唯一、尺寸一致、无缺图、总大小可接受。
4. 运行 TypeScript typecheck。

### Phase B：题库 V2 与 Migration

1. 把 V2 文案转成结构化数据。
2. 创建 Django Data Migration。
3. 验证空库迁移、重复 seed、V1/V2 共存和新会话使用 V2。
4. 运行后端 pytest。

### Phase C：答题页 UI

1. 接入场景和题目 metadata。
2. 实现道路分枝选项、选中脚印和题目完成动画。
3. 保留快速连点与提交竞态修复。
4. 运行 typecheck、静态资源检查和页面状态测试。

### Phase D：本地完整链路

1. 运行 migration 和 seed。
2. 运行后端测试。
3. 运行 `scripts/demo_e2e.py` 验证 A→B 完整链路。
4. 检查现有 Web Demo 是否因题库 V2 产生明显回归。

### Phase E：同步与云端部署

1. 编译并同步到 `/Users/cc/WeChatProjects/miniprogram-3/miniprogram`。
2. 在开发者工具中检查编译和包体积。
3. 重新构建并上传 `personality-api-cloudrun.zip`，让云数据库执行 Migration。
4. 再次调用 `/api/v1/health` 并请求测试详情，确认返回 V2。

### Phase F：人工真机验收

按 Q01、Q03、Q07、Q08、Q13、Q20、Q21、Q24 先做跨章节抽查，再跑完整 24 题和 A→B 链路。

## 9. 自动化验收清单

- [ ] 正式 manifest 恰好包含 Q01–Q24，无重复、无缺失。
- [ ] 24 张运行图均存在，尺寸一致，包体积未超开发者工具限制。
- [ ] V2 恰好有 24 道题、96 个选项，每题 A/B/C/D 各一次。
- [ ] API 返回每题 `metadata.scene_asset`。
- [ ] 快速连续点击不会把上一题 option 提交给下一题。
- [ ] 最后一题保存完成后可以立即提交，不再误报“请完成全部答题”。
- [ ] A/B 的旧主链路测试继续通过。
- [ ] `npm run typecheck` 通过。
- [ ] Django pytest 通过。
- [ ] Django Migration 没有未生成的模型变化。

## 10. 需要用户人工确认的检查点

### 检查点 1：开发者工具视觉样板

完成 Q01、Q03、Q07、Q20 的实际页面后，请确认：

- 文字雾层是否仍然过重；
- 道路分枝是否自然，是否再次出现“蝴蝶翅膀”感；
- 题目与选项字号是否适合真机；
- 图片裁切是否伤到动物或关键道具。

未通过时只调整 UI 层，不重新制作 24 张母图。

### 检查点 2：云托管重新部署

本地后端与 Migration 通过后，需要用户在腾讯云控制台上传新的云托管包并触发部署。该操作会变更线上服务，应由用户在控制台确认。

### 检查点 3：真机完整验收

部署完成后由用户扫码验证：图片加载、快速答题、最后提交、退出恢复、A 邀请 B 和双人报告。

## 11. 回滚策略

- PNG 母图和历史 `scene-v*.png` 全部保留。
- V1 题库保留，不删除已有会话和答案。
- UI 改动集中在答题页与 manifest；若视觉样板不通过，可回退页面，不动数据库历史数据。
- 云托管部署失败时继续运行旧版本，不手工修改线上数据库；修复代码后重新部署 Migration。

## 12. 明确不做

- 不实现正式人格算法、正式动物主副型算法或心理测量效度声明。
- 不实现 AI/LLM 报告。
- 不新增支付、会员、聊天、社区、心理咨询等大型功能。
- 不把图片或测试结果解释成诊断、伴侣筛选或关系优劣结论。

## 13. 2026-08-31 执行记录

### 已完成

- [x] 核对并锁定 24 张正式母图。
- [x] 建立 `miniapp/assets/questions/manifest.json`。
- [x] 首轮生成 24 张 `600 × 1297` WebP；真机兼容修复后改为 JPEG，总计 `1,836,015` bytes。
- [x] 建立 V2 内容快照和 Django Data Migration。
- [x] 保留 V1，并修复旧邀请继续使用原题库版本的兼容逻辑。
- [x] 答题页接入全屏场景、渐变雾层、错位道路选项、脚印反馈、下一图预取和失败占位。
- [x] 首页文案更新为“月森关系地图”。
- [x] 配置 `miniprogram-3` 排除未使用的腾讯模板资源。
- [x] 同步到 `/Users/cc/WeChatProjects/miniprogram-3/miniprogram`。
- [x] 18 项 Django 测试通过。
- [x] TypeScript typecheck 通过。
- [x] Migration 模型检查通过，无遗漏 schema 变化。
- [x] 素材/题目/metadata 联合检查通过：24 题、96 选项、24 场景。
- [x] 使用临时 SQLite 实际跑通 A→邀请 B→B 完成→双人报告，状态 `ok`。
- [x] 云托管 `personality-api` 版本 `002` 部署为“正常”，V2 详情接口实际返回“月森关系地图 / 24 道题”。
- [x] 微信开发者工具实际进入 Q01，并检查 Q03/Q07/Q20 的场景、题目与分枝选项。
- [x] 修复微信运行时不能动态 `require` JSON manifest 导致的答题页空白，改用可编译的 TypeScript 场景模块。
- [x] 修复自定义导航在刘海屏上的章节标题遮挡，并增强浅色交界处题目小标题对比度。
- [x] 修复真机调试包遗漏动态场景图片：关闭未使用文件剔除，并将 `assets/questions` 明确加入打包清单。
- [x] 修复模拟器有图、真机无图：运行资源切换为 JPEG，客户端场景清单作为资源路径唯一来源，目标工程清除旧 WebP。
- [x] 最后一题保存成功后自动提交并进入结果页；提交失败时保留原页和手动重试，继续依赖后端幂等接口。
- [x] 修复旧会话可到达 Q24 但前面仍有漏题的死路：自动跳回第一道漏题；在任意位置补齐 24 题后立即生成结果。
- [x] 首页改为全屏月森绘本场景、低饱和纸张雾层和半透明入口面板，不再使用通用白色卡片。
- [x] 结果预览增加动物原型、标签、摘要和三维相处光谱；完整手记增加锁定态与分章节输出，仍使用 Mock Engine，不接入 AI 报告或正式人格算法。

### 环境性阻断

本机 Docker Desktop 可以启动，但 Docker Hub 拉取 `python:3.12-slim` 时发生
`DeadlineExceeded`。这不是项目测试失败；本轮改用隔离的临时 SQLite 和本机 Python
完成了相同 API 主链路验收。以后网络恢复后仍应补跑一次 Docker Compose。

### 当前人工检查点

1. 开发者工具重新登录后生成真机调试二维码，确认首页全屏场景与半透明入口面板。
2. 在真机从 Q01 连续完成 24 题，重点确认快速连续点击、最后一题动画、自动生成结果和结果页滚动。
3. 使用 A 邀请 B，真机完成双人关系报告的最终发布前验收。

> 本轮修复只涉及小程序端运行代码，后端版本 `002` 无需再次部署；正式体验版仍需在人工确认后重新“上传”小程序代码。
