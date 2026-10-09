# 开发说明

业务调用层次：View → Service → Engine/Adapter → Model。事务、权限与幂等逻辑在 Service 和数据库约束中完成。

测试：

```bash
cd backend
USE_SQLITE_FOR_TESTS=1 ../.venv/bin/pytest
cd ../miniapp
npm run typecheck
```

真实环境验收：

```bash
docker compose -f deploy/docker-compose.yml up --build -d
docker compose -f deploy/docker-compose.yml exec backend python manage.py seed_demo
python3 scripts/demo_e2e.py
```

新增测试类型时创建 Test/TestVersion/Question，并注册对应 ScoringEngine；不要修改历史版本。正式算法上线时增加新的 engine key 和版本，不覆盖 Mock 快照。
