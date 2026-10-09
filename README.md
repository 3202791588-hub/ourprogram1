# 微信人格测试与好友关系分析 Demo

这是一个严格按 `personality_miniapp_extensible_demo_spec.md` 实现的可扩展 Demo。它跑通：A 用户测试 → 结果快照 → Mock 解锁 → 邀请 B → B 测试 → 双人关系报告。

> 本项目只做娱乐化人格探索，不提供心理或医疗诊断。当前评分与关系结论均为确定性的 Mock 数据，不具有科学解释力。

## 最快启动（Docker）

1. 安装并启动 Docker Desktop（或兼容 Docker Compose 的容器运行时）。
2. 进入项目并复制配置：

   ```bash
   cp .env.example .env
   docker compose -f deploy/docker-compose.yml up --build -d
   docker compose -f deploy/docker-compose.yml exec backend python manage.py seed_demo
   curl http://localhost/api/v1/health
   ```

3. API 文档：<http://localhost/api/docs/>；Admin：<http://localhost/admin/>。
4. 创建管理员（可选）：

   ```bash
   docker compose -f deploy/docker-compose.yml exec backend python manage.py createsuperuser
   ```

验证完整 A/B 主链路：

```bash
python3 scripts/demo_e2e.py
```

## 浏览器 Web Demo

Docker 启动后直接访问：<http://localhost/>。

网页端复用同一套 Django API、数据库、权限、幂等和 Mock Engine。推荐人工验收：

1. 保持“用户 A”，点击“开始探索”并完成 24 题。
2. 解锁完整报告，点击“邀请好友测关系”。
3. 点击“切换到 B 并接受邀请”，完成 B 的 24 题。
4. 提交后自动进入双人关系报告。

网页端仅是微信小程序前的交互验收壳，不复制评分或关系算法。

## 不用 Docker 跑后端测试

Python 3.11+ 与 PostgreSQL 可用时：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL=postgresql://personality:personality@localhost:5432/personality
cd backend
python manage.py migrate
python manage.py seed_demo
pytest
```

测试默认可用内存 SQLite 作为隔离的测试数据库；实际开发与 Docker 运行均使用 PostgreSQL。

## 小程序

用微信开发者工具导入 `miniapp/`。当前默认通过 `wx.cloud.callContainer` 调用环境
`cloud1-d1gt8iwo343dfe428` 中的 `personality-api` 服务。需要只测试本机 Docker 时，
可在 `miniapp/utils/config.ts` 将 `USE_CLOUD_CONTAINER` 改为 `false`，此时 API 为
`http://localhost/api/v1`。点击首页顶部的 A/B 开关可模拟两位用户。

完整演示：

1. 以 A 登录，完成 24 题并提交。
2. 查看基础结果，Demo 解锁完整报告，创建邀请并复制邀请码。
3. 切换为 B，打开邀请页（开发工具可用编译参数 `pages/invite/index?code=...`），接受并完成测试。
4. 提交后自动生成并打开双人关系报告。

### 月森 V3 题目与场景资源

V3 使用 `docs/QUESTION_COPY_V3_HUMAN_RELATION.md` 的 24 道人际关系题：12 道记录
“我通常怎么做”的行为题，12 道记录“我希望怎样被回应”的需要题。动物和月森只作为
视觉隐喻，不把答题者代入动物角色。高清 PNG 母图保存在
`miniapp/assets/questions/q01` 至 `q24`，运行时不直接打包母图。生成 24 张压缩 JPEG：

```bash
./.venv/bin/pip install Pillow
./.venv/bin/python scripts/build_question_assets.py
./.venv/bin/python scripts/check_question_integration.py
npm --prefix miniapp run typecheck
```

正式映射位于 `miniapp/assets/questions/manifest.json`；同步脚本会排除
`scene-v*.png` 和旧的 `scene.webp`，只把 `scene.jpg` 带入开发者工具项目。JPEG 用于规避
模拟器可显示、部分真机却无法解析本地 WebP 的差异。完整实施与验收方案见
[`docs/QUESTION_V2_DEMO_INTEGRATION_PLAN.md`](docs/QUESTION_V2_DEMO_INTEGRATION_PLAN.md)。

题库 V3 由 Django Migration `tests.0004_publish_human_relationship_v3` 发布，不原地
覆盖 V1/V2。部署新后端包后，容器启动时会自动运行 Migration；历史会话及邀请仍读取
各自创建时绑定的版本。V3 的 `response_mode` 仅为未来双人匹配保留结构；当前个人结果
和关系报告仍由 Mock Engine 生成，不代表正式契合度算法。

### 首页主视觉

首页使用独立的“树心入口”主 KV，不复用任何一道题目的场景。无字 PNG 母图位于
`docs/assets/home/home-tree-gateway-v1.png`，真机运行使用压缩后的
`miniapp/assets/home/tree-gateway.jpg`。标题、说明和按钮均由小程序原生组件渲染，便于
适配屏幕、修改文案和保证点击区域准确。同步脚本会明确把 `assets/home` 加入开发者工具
项目的上传包。

需重新生成运行图时，使用工作区依赖中的 Pillow 运行
`python scripts/build_home_asset.py` 和 `python scripts/build_question_assets.py`。这两个脚本均从 PNG 原图生成 JPG，避免反复压缩已压缩的图片。

## 微信云托管部署

生成可上传的云托管代码包：

```bash
./scripts/build_cloudrun_package.sh
```

将 `dist/personality-api-cloudrun.zip` 上传到“云函数/托管 → 服务管理 → 使用本地代码
上传部署”。服务名填 `personality-api`，访问端口和服务端口均填 `80`，Dockerfile
名称填 `Dockerfile`，Demo 最大实例数设为 `1`。完整环境变量清单见
`cloudrun/README_UPLOAD.md`。

数据库连接推荐分别使用 `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USER` 和
`DB_PASSWORD`，密码无需进行 URL 编码。数据库密码与 `DJANGO_SECRET_KEY` 只配置
在云托管环境变量，不写入代码包。容器启动
时依次执行 Django Migration、幂等 `seed_demo` 和 Gunicorn。正式发布前应将 Mock
微信登录替换为真实 `code2Session` Adapter，并将 Demo 初始化从启动流程中拆出。

接入月森 V3 后必须重新构建并上传云托管包，否则小程序虽然能显示场景图，API 仍会
返回旧题目。部署完成后先验证 `/api/v1/health`，再打开测试详情确认名称为
“月森关系地图”、版本为 V3。

当前免费体验套餐无法为云托管开启 VPC，Demo 使用 MySQL 外网直连。该方式只适用开发调试；正式上线应升级到支持 VPC 的方案并切换为内网地址。

## Mock 与正式能力替换

| 当前 Mock | 配置 | 正式替换方式 |
|---|---|---|
| 微信登录 | `WECHAT_AUTH_MODE=mock` | 实现 `WechatAuthAdapter` 的 code2Session 调用，配置 AppID/Secret，再设为 `wechat` |
| 人格评分 | `SCORING_ENGINE=mock` | 实现 `ScoringEngine.calculate()` 并在 engine factory 注册版本；已有结果快照不会重算 |
| 关系算法 | `RELATION_ENGINE=mock` | 实现 `RelationEngine.calculate()` 并注册版本；已有关系报告不会重算 |
| 激励广告 | `ADS_ENABLED=false` | 小程序 Adapter 接 `wx.createRewardedVideoAd`，后端仅在广告完成后写入 `AD` 解锁 |

所有 Mock 计算集中在 `backend/apps/results/engines.py`、`backend/apps/relations/engines.py` 和小程序 `services/ad.ts`，未散落在页面或 View 中。

## 常用命令

```bash
docker compose -f deploy/docker-compose.yml logs -f backend
docker compose -f deploy/docker-compose.yml exec backend python manage.py migrate
docker compose -f deploy/docker-compose.yml exec backend pytest
docker compose -f deploy/docker-compose.yml down
```

数据库结构只通过 Django Migration 变更。API 使用 JWT、对象级权限、事务与唯一约束保证关键操作的权限和幂等性。

## 范围边界

未实现：正式人格算法、AI/LLM 报告、支付、会员、积分、聊天、社区、心理咨询/诊断、Redis、消息队列、微服务、独立 Admin、Kubernetes。

## 可复制开发经验

从需求、Web 验收、Docker 后端到微信开发者工具同步的完整经验见：

[`docs/WECHAT_MINIPROGRAM_REUSABLE_PLAYBOOK.md`](docs/WECHAT_MINIPROGRAM_REUSABLE_PLAYBOOK.md)
