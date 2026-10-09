# 微信小程序从开发到上线的可复现实战手册

> 项目实例：“隐藏人格测试”Demo  
> 最后更新：2026-08-25  
> 适用范围：微信原生小程序、Django API、CloudBase MySQL、微信云托管、本地 Docker、真机测试

## 1. 文档目标与状态边界

本文档将本项目从需求文档、网页 Demo、小程序开发、数据库、云托管、权限申请、上传、真机调试到审核发布的经验合并为一份可执行手册。

阅读时必须区分四类信息：

- **已验证**：在本项目和当前设备上已经成功。
- **Demo 现状**：可用于体验和流程验收，不等于正式生产能力。
- **上线前必做**：提交正式审核前必须替换或确认。
- **平台动态规则**：套餐、类目、资质、隐私、广告和审核资格以提交当日的微信公众平台和 CloudBase 控制台为准。

本项目已验证的线上链路：

```text
微信开发者工具 / 真机
→ wx.cloud.callContainer
→ CloudBase 环境
→ personality-api 云托管容器
→ Django REST API
→ CloudBase MySQL
→ 生成人格结果与双人关系报告
```

---

## 2. 当前成功环境快照

### 2.1 本机和代码

```text
系统：macOS Apple Silicon
微信开发者工具：Stable 2.02.2608040
后端：Django + Django REST Framework + Gunicorn
本地数据库：PostgreSQL 16（Docker）
云端数据库：CloudBase MySQL
小程序：微信原生小程序 + TypeScript
```

源码根目录：

```text
/Users/cc/Documents/情感测试/personality-miniapp
```

微信开发者工具项目：

```text
项目名：miniprogram-3
路径：/Users/cc/WeChatProjects/miniprogram-3
AppID：wx5e14dc6e44274be6
```

### 2.2 CloudBase

```text
环境 ID：cloud1-d1gt8iwo343dfe428
云托管服务：personality-api
访问端口：80
服务端口：80
数据库名：cloud1-d1gt8iwo343dfe428
数据库账号：personality_app
```

当前免费体验环境无法为云托管开启私有网络，所以 Demo 使用 MySQL 外网直连：

```text
外网主机：sh-cynosdbmysql-grp-p49nrxzw.sql.tencentcdb.com
外网端口：22529
```

支持 VPC 后的正式切换值：

```text
内网主机：172.17.0.2
内网端口：3306
VPC：vpc-mokg9rnk
子网：subnet-1tgcdx9x
```

> 不在文档中记录数据库密码、`DJANGO_SECRET_KEY`、微信 AppSecret 或其他凭据。

---

## 3. 产品主链路和不做边界

开发前先把主链路压缩为一句话：

```text
A 完成测试
→ 生成结果快照
→ Mock 解锁完整报告
→ 邀请 B
→ B 完成测试
→ 生成双人关系报告
```

当前 Demo 明确不做：

- 正式人格算法。
- AI/LLM 生成报告。
- 支付、会员、积分、聊天和社区。
- 心理或医疗诊断。
- 复杂微服务、Redis、消息队列和 Kubernetes。

不要因为已能上云就把 Demo 表述为正式产品。当前评分和关系结论都是确定性 Mock，不具有科学或诊断效力。

---

## 4. 账号、身份和权限申请

### 4.1 需要的账号

| 账号/角色 | 用途 | 是否需要所有者人工操作 |
|---|---|---|
| 微信小程序管理员 | 创建小程序、认证、类目、隐私、审核和发布 | 是 |
| 小程序开发者 | 登录开发者工具、上传代码 | 需管理员添加 |
| 体验成员 | 扫码打开体验版 | 需管理员添加 |
| CloudBase 环境管理员 | 数据库、云托管、日志和费用 | 是 |

如果开发者工具登录的微信不是该 AppID 的管理员或开发者，就可能无法上传、预览或真机调试。

### 4.2 小程序基础信息

本项目可使用的 Demo 文案：

```text
名称：隐藏人格测试
简介：通过趣味选择题探索个人特点，并邀请好友生成娱乐化关系报告。内容仅供娱乐与自我探索，不用于心理或医疗诊断。
```

头像建议：

- 使用简单、可辨识、无诊断暗示的原创图标。
- 不使用医院、医生、脑电图、治疗、证书等容易产生专业诊断误解的元素。

### 4.3 服务类目

不能仅根据产品名称猜类目。应在微信公众平台根据当前实际功能选择“工具/测试/娱乐”等当时可选且符合主体资质的类目。

禁止把娱乐测试包装成：

- 心理诊断。
- 精神疾病评估。
- 医疗建议。
- 具有专业效力的量表。

最终可选类目、是否需要资质，以提交时后台显示为准。

### 4.4 隐私和用户数据

正式提审前要在后台填写《小程序用户隐私保护指引》，且必须与代码真实行为一致。

当前 Demo：

- 不采集手机号、定位、通讯录和敏感健康信息。
- 保存测试进度、答案、结果快照、邀请和关系报告。
- 提供“删除我的测试数据”入口。
- 当前使用 Mock 身份，还不是正式微信 OpenID 身份。

---

## 5. 推荐项目结构

```text
personality-miniapp/
├── miniapp/                    # 微信原生小程序 TypeScript 源码
│   ├── pages/
│   ├── services/               # 统一 API 调用
│   ├── store/
│   ├── utils/
│   └── types/
├── web/                        # 浏览器人工验收端
├── backend/                    # Django API、Migration、Engine/Adapter
├── deploy/                     # 本地 Docker Compose / Nginx
├── cloudrun/                   # 云托管 Dockerfile 和启动脚本
├── scripts/
│   ├── demo_e2e.py
│   ├── build_cloudrun_package.sh
│   └── sync_miniprogram3.sh
├── dist/                       # 生成的云托管 ZIP
├── docs/
└── README.md
```

核心分层：

```text
View → Service → Engine / Adapter → Model
```

Mock 只能放在 Engine/Adapter，不能散落在页面和 API View 里。

---

## 6. Phase 1 → Phase 10 完整开发顺序

### Phase 1：骨架和 README

先创建目录、`.env.example`、README、测试命令和 Mock 替换说明，再写业务代码。

验收：

- Clone 后能明确知道如何启动。
- 机密只通过环境变量注入。
- “做什么/不做什么”已写清。

### Phase 2：数据模型与 Migration

关键不变式：

- `Test + version` 唯一。
- `Session + Question` 唯一，重复保存答案执行更新。
- Session 与 ResultSnapshot 一对一。
- Invite 与 Relationship 一对一。
- 历史结果保存快照，不因新算法上线而重算。

所有 Schema 变化必须创建 Django Migration，禁止只在控制台手工改表。

### Phase 3：身份、权限和幂等

- API 使用 JWT。
- 用户只能访问自己的 Session 和完整报告。
- 双人报告只允许双方查看。
- 重复提交返回已有结果。
- 重复接受邀请不创建第二段关系。

### Phase 4：Mock Engine/Adapter

```text
WechatAuthAdapter
ScoringEngine
RelationEngine
RewardedAdAdapter
```

正式能力上线时只替换对应实现和配置键，不重写主流程。

### Phase 5：API 和网页验收端

先在浏览器跑通 A/B 主链路，再适配微信端。网页只是验收壳，评分、邀请和关系报告仍由同一个后端生成。

### Phase 6：微信原生页面

API 调用集中在：

```text
services/http
services/auth
services/tests
services/results
services/relations
```

页面不应散落 `wx.request()` 或 `wx.cloud.callContainer()`。

### Phase 7：开发者工具导入与同步

保留真实 `project.config.json` 和 AppID，先编译 TypeScript，再同步产物。

### Phase 8：云数据库和云托管

创建 MySQL 账号、选择网络方式、构建 ZIP、部署容器、运行 Migration。

### Phase 9：开发者工具与真机端到端验收

依次验证：

```text
云托管健康接口
→ 开发者工具调用
→ A 完整答题
→ B 邀请链路
→ 真机
```

### Phase 10：上传、体验版、审核与发布准备

上传代码不等于已发布。还需要在微信公众平台设置体验版、完善信息、隐私与类目、提交审核，审核通过后才能发布。

---

## 7. 本地开发与 Web Demo

### 7.1 Docker 启动

```bash
cd "/Users/cc/Documents/情感测试/personality-miniapp"
cp .env.example .env
docker compose -f deploy/docker-compose.yml up --build -d
docker compose -f deploy/docker-compose.yml exec backend python manage.py seed_demo
curl http://localhost/api/v1/health
```

预期：

```json
{"code":0,"message":"ok","data":{"status":"ok"}}
```

浏览器访问：

```text
http://localhost/
```

### 7.2 自动测试

```bash
cd "/Users/cc/Documents/情感测试/personality-miniapp/backend"
../.venv/bin/pytest -q

cd ../miniapp
./node_modules/.bin/tsc --noEmit
```

当前已验证：

```text
后端：15 passed
小程序：TypeScript 编译通过
```

端到端 API 脚本：

```bash
cd "/Users/cc/Documents/情感测试/personality-miniapp"
python3 scripts/demo_e2e.py
```

---

## 8. 微信开发者工具项目

### 8.1 创建或导入

可直接导入源码，也可先在开发者工具创建空项目，再同步业务文件。本项目采用后者。

重要文件：

```text
/Users/cc/WeChatProjects/miniprogram-3/project.config.json
```

不要用源码仓库里的模板配置覆盖它，否则可能丢失真实 AppID、云环境和开发者工具设置。

### 8.2 TypeScript 同步

项目已提供：

```bash
cd "/Users/cc/Documents/情感测试/personality-miniapp"
./scripts/sync_miniprogram3.sh /Users/cc/WeChatProjects/miniprogram-3
```

该脚本会：

1. 编译 TypeScript。
2. 同步 `.js/.json/.wxml/.wxss` 和业务文件。
3. 不删除微信项目自有文件。
4. 不覆盖 `project.config.json`。

### 8.3 开发者工具设置

- CLI 自动化需在“设置 → 安全设置 → 服务端口”开启服务端口。
- 本机 HTTP 联调可在本地设置中暂时关闭合法域名校验。
- `project.private.config.json` 可能覆盖公开配置，两者都要检查。
- 不建议为了解决正式网络问题而长期依赖“不校验合法域名”。

---

## 9. 创建 CloudBase 环境和 MySQL

### 9.1 创建云环境

1. 在微信开发者工具或腾讯云 CloudBase 控制台开通云开发。
2. 记录环境 ID。
3. 确认小程序 AppID 与该云环境完成关联。
4. 不要把“云环境名称”、“环境 ID”、“数据库名称”混为同一概念。

### 9.2 初始化 MySQL

进入：

```text
CloudBase → SQL 型数据库 / MySQL 数据库
```

首次使用时按控制台引导初始化。本项目使用 Django Migration 建表，不需要在可视化控制台手工创建业务表。

### 9.3 创建数据库账号

```text
账号名：personality_app
主机：%
```

`%` 表示允许来自不固定主机的连接。这是数据库账号授权范围，不是应用的 `DB_HOST`。

Django Migration 至少需要：

```text
SELECT
INSERT
UPDATE
DELETE
CREATE
ALTER
DROP
INDEX
REFERENCES（如控制台提供）
```

不需要为业务账号开放 `CREATE USER` 等账号管理权限。

密码由创建账号时自己设置。控制台通常不会再明文显示原密码，忘记时应重置。

### 9.4 开启直连服务

进入：

```text
数据库设置 → 直连服务
```

开启后会生成内网和外网连接地址。

两种方式不能混用：

| 场景 | DB_HOST | DB_PORT | 额外要求 |
|---|---|---:|---|
| 免费 Demo，不能开 VPC | 外网主机名 | 22529 | 直连服务开启 |
| 正式/支持 VPC | 172.17.0.2 | 3306 | 云托管开启私网并绑定数据库 VPC/子网 |

外网地址官方定位为开发调试用途。正式生产应升级到可用 VPC 的方案，切回内网地址。

---

## 10. 构建云托管代码包

构建：

```bash
cd "/Users/cc/Documents/情感测试/personality-miniapp"
./scripts/build_cloudrun_package.sh
```

产物：

```text
/Users/cc/Documents/情感测试/personality-miniapp/dist/personality-api-cloudrun.zip
```

ZIP 根目录必须直接包含：

```text
Dockerfile
manage.py
requirements.txt
start.sh
config/
apps/
```

不要上传整个仓库，不要把 `.env`、数据库密码和 Secret 打入 ZIP。

容器启动顺序：

```text
python manage.py migrate --noinput
→ python manage.py seed_demo
→ gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

`seed_demo` 是幂等 Demo 初始化。正式上线前应将它从每次启动流程拆出，改为一次性管理命令或发布任务。

---

## 11. 创建并部署云托管服务

### 11.1 不必须使用 Git 仓库

CloudBase 支持 Git、容器镜像、CLI 和本地代码上传。本项目已验证“使用本地代码上传部署”，不需要先创建 GitHub 仓库。

### 11.2 服务参数

```text
服务名：personality-api
部署方式：本地代码包
文件：personality-api-cloudrun.zip
Dockerfile：Dockerfile
访问端口：80
服务端口：80
最小实例：0（Demo）
最大实例：1（Demo）
```

服务名创建后通常不建议随意改变，因为小程序 `callContainer` 会使用它。

### 11.3 环境变量

免费 Demo 当前可用清单：

```env
DB_HOST=sh-cynosdbmysql-grp-p49nrxzw.sql.tencentcdb.com
DB_PORT=22529
DB_NAME=cloud1-d1gt8iwo343dfe428
DB_USER=personality_app
DB_PASSWORD=<数据库账号密码>
DJANGO_SECRET_KEY=<独立随机强密钥>
DEBUG=false
WECHAT_AUTH_MODE=mock
ADS_ENABLED=false
SCORING_ENGINE=mock
RELATION_ENGINE=mock
JWT_ACCESS_TOKEN_MINUTES=10080
PORT=80
```

`DJANGO_SECRET_KEY` 不是在微信或腾讯云查找的密码，而是由项目自己生成的 Django 签名密钥：

```bash
openssl rand -base64 48
```

规则：

- 必须与 `DB_PASSWORD` 不同。
- 可包含 `/`，因为它作为独立环境变量传入，不是 URL。
- 不写入代码、ZIP、截图或公开日志。
- 不要随意更换，更换可能使旧签名和登录状态失效。

### 11.4 内网正式配置

套餐支持私有网络后，更改：

```env
DB_HOST=172.17.0.2
DB_PORT=3306
```

并在云托管“服务设置 → 网络设置”中开启私有网络，选择数据库所在 VPC 和子网。只改为内网 IP 却不开 VPC，一定会连接超时。

---

## 12. 云托管部署验证

不能只看“镜像构建成功”。完整成功需要：

```text
ZIP 解压成功
→ Docker 构建成功
→ 镜像推送成功
→ Migration 成功
→ Gunicorn 监听 0.0.0.0:80
→ 健康检查通过
→ 版本状态正常
```

正常启动日志应出现类似：

```text
Applying migrations...
Running migrations...
Demo data ready
Listening at: http://0.0.0.0:80
```

本项目首次失败的关键日志：

```text
Liveness probe failed: connection refused
django.db.utils.OperationalError:
Can't connect to MySQL server on '172.17.0.2' (timed out)
```

真正根因不是 80 端口，而是：

```text
容器启动
→ Migration 连内网 MySQL 超时
→ start.sh 终止
→ Gunicorn 没有监听 80
→ 健康检查只看到 connection refused
```

免费环境无法开 VPC 时，使用外网主机和 22529 端口后成功。

---

## 13. 小程序调用云托管

### 13.1 配置

`miniapp/utils/config.ts`：

```ts
export const CLOUD_ENV_ID = "cloud1-d1gt8iwo343dfe428"
export const CLOUD_SERVICE_NAME = "personality-api"
export const API_PREFIX = "/api/v1"
export const USE_CLOUD_CONTAINER = true
```

`app.ts`：

```ts
wx.cloud.init({
  env: CLOUD_ENV_ID,
  traceUser: true,
})
```

统一请求层使用：

```ts
wx.cloud.callContainer({
  config: {env: CLOUD_ENV_ID},
  service: CLOUD_SERVICE_NAME,
  path: API_PREFIX + path,
  method,
  data,
  header: {
    "X-WX-SERVICE": CLOUD_SERVICE_NAME,
  },
})
```

`callContainer` 使用微信与云托管的专用调用链路。小程序主链路不依赖自定义 request 域名，云托管公网入口开关也不影响 `callContainer`。

### 13.2 健康检查

在开发者工具 Console 运行：

```js
wx.cloud.callContainer({
  config: {env: 'cloud1-d1gt8iwo343dfe428'},
  service: 'personality-api',
  path: '/api/v1/health',
  method: 'GET',
  header: {'X-WX-SERVICE': 'personality-api'},
}).then(console.log).catch(console.error)
```

成功判定：

```text
statusCode: 200
```

以及：

```json
{"code":0,"message":"ok","data":{"status":"ok"}}
```

`Promise {<pending>}` 只是异步请求尚未返回时的正常状态，不是错误。

---

## 14. 开发者工具和真机验收

### 14.1 建议顺序

```text
1. 模拟器编译成功
2. Console 健康检查 200
3. A 用户完成 24 题
4. 生成个人结果
5. 生成邀请码
6. 切换 B
7. B 接受邀请并完成测试
8. 生成双人关系报告
9. 真机重复主链路
```

### 14.2 Demo 中的 A/B 邀请

当前是 Mock 用户。开发者工具中：

1. A 完成测试并复制邀请码。
2. 返回首页切换 B。
3. Console 运行：

```js
wx.navigateTo({
  url: '/pages/invite/index?code=<邀请码>'
})
```

4. B 接受并完成测试。

这不是正式微信好友分享。正式上线前要把分享卡片 path 改为邀请页、接入真实微信身份，并用两个真实微信账号测试。

### 14.3 快速点击答案的竞态修复

真机暴露出的问题：逻辑层已经切到下一题，原生视图还短暂显示上一题；此时快速点击会把旧选项 ID 与新问题 ID 组合发送。

修复原则：

- 点击节点同时携带 `questionId` 和 `optionId`。
- 忽略与当前题不匹配的旧视图事件。
- 保存和过渡期立即加锁。
- 最后一题提交前从服务器重新读取答题数。
- 客户端“完成 24 题”只用于交互，服务端仍是最终真值。
- 选中后显示对勾、进度和“当前题目已完成”过渡动画。

---

## 15. 真机调试 Timeout 排查

真机调试与小程序访问云托管是两条不同链路。健康接口已返回 200 时，“生成真机调试二维码 Timeout”不应继续归因于 Django 或 MySQL。

本次本机日志的确定证据：

```text
代码包上传成功
远程调试 login/join/heartbeat 成功
/remote-debug/appservice 返回 500
initWithProxyFunc 等待 30005ms 后超时
```

恢复顺序：

1. 取消当前真机调试。
2. “工具 → 清除缓存 → 清除全部”。
3. `Command + Q` 完全退出开发者工具。
4. 重开后只打开 `miniprogram-3`，不同时打开旧项目。
5. 先编译，再选择与手机一致的 Android/鸿蒙或 iOS。
6. 优先尝试二维码真机调试。
7. 仍失败时，从项目列表“仅移除”项目，再重新导入原路径，禁止删除本地文件。

该方法已恢复真机调试。

---

## 16. 上传、体验版、审核和发布

### 16.1 上传代码

开发者工具：

```text
右上角“上传”
→ 版本号，例如 0.0.2
→ 版本备注，例如“云托管联调版”
```

每次修改小程序源码后，真机体验版都需要重新上传。仅修改云托管环境变量或后端版本时，如果 API 兼容，则不需要重新上传小程序。

### 16.2 设置体验版

```text
微信公众平台
→ 版本管理
→ 开发版本
→ 选中刚上传的版本
→ 设为体验版
```

再在成员管理中添加体验成员，使用体验版二维码进行真实微信环境验收。

### 16.3 正式提审前资料

- 名称、头像、简介。
- 服务类目和可能的资质。
- 隐私保护指引。
- 用户协议和隐私政策页（如适用）。
- 测试账号或审核路径说明。
- 所有核心页面可访问，无空白、无死链接。
- 不夸大人格测试的科学效力。
- 如接入广告、支付或其他特殊能力，已获得对应资格。

### 16.4 提审和发布

```text
上传代码
→ 设为体验版
→ 内部验收
→ 提交审核
→ 处理审核反馈
→ 审核通过
→ 管理员确认发布
```

只有最后一步成功后才能表述为“已上线”。

---

## 17. 当前 Demo 不能直接当正式版发布的原因

当前已跑通技术主链路，但以下项目仍是正式上线阻断项：

1. `WECHAT_AUTH_MODE=mock`，还没有真实 `code2Session` 和 OpenID 身份。
2. A/B 通过首页开关模拟，不是两个真实微信用户。
3. 分享卡片尚未完成正式邀请 path 的真实好友验证。
4. `SCORING_ENGINE=mock` 和 `RELATION_ENGINE=mock`。
5. 当前数据库使用外网直连，官方建议只用于开发调试。
6. `seed_demo` 仍在每次容器启动时执行。
7. 隐私、服务类目和审核文案仍需所有者在后台确认。

开发版、体验版可继续用于内部人工验收，但不应跳过上述替换就宣称为完整正式产品。

---

## 18. Mock 到正式能力替换表

| 能力 | 当前配置 | 正式替换 |
|---|---|---|
| 微信登录 | `WECHAT_AUTH_MODE=mock` | 实现 `WechatAuthAdapter` 的 `code2Session`，Secret 只存服务端 |
| 人格评分 | `SCORING_ENGINE=mock` | 新增有版本号的 `ScoringEngine.calculate()`，不改历史快照 |
| 关系算法 | `RELATION_ENGINE=mock` | 新增有版本号的 `RelationEngine.calculate()` |
| 激励广告 | `ADS_ENABLED=false` | 小程序接 `wx.createRewardedVideoAd`，服务端验证解锁 |
| 数据库网络 | 外网直连 | 升级套餐、开 VPC、改用内网地址 |
| Demo 初始化 | 启动时 `seed_demo` | 独立发布任务或后台内容管理 |
| 好友邀请 | Mock 切换 A/B | 分享卡片携带邀请码，两个真实 OpenID 完成 |

---

## 19. 安全、权限和幂等检查

- [ ] 所有秘密只存环境变量。
- [ ] 数据库账号不具有账号管理权限。
- [ ] `DEBUG=false`。
- [ ] 用户不能获取他人完整报告。
- [ ] 双人报告只允许参与者查看。
- [ ] 答案重复保存执行更新。
- [ ] 重复提交不生成第二份结果。
- [ ] 重复接受邀请不生成重复关系。
- [ ] 广告解锁在正式模式不接受 Mock 完成事件。
- [ ] 所有数据库变化都有 Migration。
- [ ] 重置过数据库密码后同步更新云托管环境变量并重新部署。

---

## 20. 常见错误速查

| 现象 | 优先查看 | 常见根因 |
|---|---|---|
| 小程序提示网络不可用 | `wx.cloud.callContainer` 健康检查 | 仍在请求 localhost，或环境/服务名错误 |
| `statusCode: 200` | 展开 `data` | 链路已通，`Promise pending` 不是错误 |
| 部署时 liveness connection refused | 往前看启动 Traceback | Migration 先失败，Gunicorn 没启动 |
| MySQL `timed out` | `DB_HOST/DB_PORT` 和 VPC | 内网 IP 与未开 VPC 混用 |
| MySQL `Access denied` | 账号、密码、主机 `%`、权限 | 身份或授权错误 |
| Migration permission denied | CREATE/ALTER/DROP/INDEX | 数据库账号权限不足 |
| 真机调试二维码 Timeout | 本机 WeappRemote/IDE 日志 | 本地调试进程或旧上下文，不是业务 API |
| 快速点答案提示题目/选项不匹配 | 点击事件的题目 ID | 原生视图与逻辑层切题瞬间竞态 |
| 最后一题后提示未完成 | 服务端 Session 答案数 | 提交抢在最后一题保存前 |
| 开发者工具配置不生效 | `project.private.config.json` | 私有配置覆盖公开配置 |
| CLI 无法连开发者工具 | 安全设置 | IDE 服务端口未开启 |

---

## 21. 从零复现的最短执行清单

### 代码和本地环境

- [ ] Clone 项目。
- [ ] 阅读 README 和本文档。
- [ ] 安装并启动 Docker Desktop。
- [ ] 运行 Docker Compose。
- [ ] 验证 localhost 健康接口和 Web Demo。
- [ ] 运行后端测试、TypeScript 编译和 E2E。

### 微信项目和权限

- [ ] 创建小程序 AppID。
- [ ] 填写名称、头像、简介和类目。
- [ ] 添加开发者和体验成员。
- [ ] 在开发者工具创建或导入项目。
- [ ] 确认 AppID 和本地项目路径。
- [ ] 编译并同步 TypeScript 产物。

### CloudBase 和数据库

- [ ] 开通云开发并记录环境 ID。
- [ ] 初始化 MySQL。
- [ ] 创建应用数据库账号和密码。
- [ ] 分配 Django Migration 所需权限。
- [ ] 开启直连服务。
- [ ] 根据套餐选外网调试或 VPC 内网。

### 云托管

- [ ] 构建 `personality-api-cloudrun.zip`。
- [ ] 创建 `personality-api`。
- [ ] 服务和访问端口设为 80。
- [ ] 在控制台设置环境变量，不将秘密写入 ZIP。
- [ ] 确认 Migration、Gunicorn 和健康检查成功。

### 联调和真机

- [ ] `wx.cloud.init` 使用正确环境 ID。
- [ ] `callContainer` 使用正确服务名。
- [ ] Console 健康接口返回 200。
- [ ] A/B Demo 主链路完整通过。
- [ ] 快速点击、最后一题和重复提交通过。
- [ ] 真机调试通过。

### 体验版和上线

- [ ] 上传新版本。
- [ ] 设为体验版并完成体验成员验收。
- [ ] 替换真实微信登录和好友邀请。
- [ ] 数据库切换为 VPC 内网方案。
- [ ] 隐私、类目、资质和文案与实际功能一致。
- [ ] 提交审核。
- [ ] 审核通过后由管理员确认发布。
- [ ] 用普通用户身份再次验证线上版。

---

## 22. 复制到新小程序或小游戏

可直接复用：

- Phase 顺序。
- README 驱动的交付。
- Web 快速验收。
- Engine/Adapter Mock 边界。
- Docker 后端和云托管容器。
- Migration、权限、幂等和快照。
- 本地、模拟器、真机、体验版和正式版的分层验证。

小游戏不能直接复用：

- `pages/*.wxml` 页面结构。
- 小程序页面导航。
- 对 Canvas/WebGL、帧循环、音频和资源包的性能假设。

小游戏的第一条主链路建议写成：

```text
进入游戏
→ 新手引导
→ 完成第一局
→ 服务端幂等结算
→ 获得奖励
→ 再来一局/分享
```

第一版不要默认加入实时多人、公会、聊天、UGC、大型商城和复杂赛季，除非它们就是必须验证的核心玩法。

---

## 23. 官方参考

- [CloudBase 从源代码部署](https://docs.cloudbase.net/run/deploy/deploy/deploying-source-code)
- [CloudBase 云托管部署方式](https://docs.cloudbase.net/run/deploy/deploy/introduce)
- [CloudBase 服务设置与 callContainer 链路](https://docs.cloudbase.net/run/deploy/service-setting)
- [CloudBase MySQL 数据库集成](https://docs.cloudbase.net/run/develop/resource-integration/mysql)
- [CloudBase MySQL 直连服务](https://docs.cloudbase.net/database/configuration/db/tdsql/direct-connection)
- [CloudBase VPC 内网互联](https://docs.cloudbase.net/run/deploy/networking/internal-link)

---

## 24. 最终结论

本次真正可复制的不是一套页面，而是一条有证据的交付路径：

> 先写清主链路和不做边界，用可替换 Mock 跑通业务，用 Web 完成快速人工验收，再适配微信和 CloudBase；本地、云端、开发者工具和真机每一层都用健康接口、测试和日志独立验证，最后再进入体验版、审核和发布。
