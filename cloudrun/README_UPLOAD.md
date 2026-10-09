# CloudBase Run 上传说明

上传 `dist/personality-api-cloudrun.zip`，不要上传整个仓库。ZIP 根目录已包含
`Dockerfile`、`manage.py`、`requirements.txt`、`start.sh`、`config/` 和 `apps/`。

服务配置：

- 服务名：`personality-api`
- 访问端口：`80`
- 服务端口：`80`
- Dockerfile：`Dockerfile`
- 最小实例数：`0`
- 最大实例数：`1`（Demo）

必须在控制台配置的环境变量：

- `DJANGO_SECRET_KEY`：随机强密码
- `DEBUG`：`false`
- `DB_HOST`：数据库主机（不要包含协议或端口）
- `DB_PORT`：与所选数据库地址一致
- `DB_NAME`：控制台显示的数据库名
- `DB_USER`：`personality_app`
- `DB_PASSWORD`：数据库账号密码（原样填写，不需要 URL 编码）
- `WECHAT_AUTH_MODE`：`mock`
- `ADS_ENABLED`：`false`
- `SCORING_ENGINE`：`mock`
- `RELATION_ENGINE`：`mock`
- `JWT_ACCESS_TOKEN_MINUTES`：`10080`
- `PORT`：`80`（如果控制台没有自动注入）

也兼容完整的 `DATABASE_URL`，但不推荐在密码含特殊字符时使用。不要把数据库密码
或 Django Secret Key 写入 ZIP。容器启动时依次执行 Django
Migration、幂等 Demo 数据初始化和 Gunicorn。正式发布前应将 Mock 微信登录替换为
真实 `code2Session` Adapter，并将 Demo 数据初始化从启动命令中拆出。

## 数据库网络二选一

免费 Demo 无法开启云托管 VPC 时，使用数据库设置页显示的外网主机和外网端口。本环境当前为：

```env
DB_HOST=sh-cynosdbmysql-grp-p49nrxzw.sql.tencentcdb.com
DB_PORT=22529
```

外网直连只用于 Demo/开发调试。套餐支持 VPC 后，为云托管服务开启私有网络、选择数据库的 VPC/子网，再改为：

```env
DB_HOST=172.17.0.2
DB_PORT=3306
```

未开启 VPC 时不得使用 `172.17.0.2`，否则 Migration 会连接超时，Gunicorn 无法启动，最终表现为 liveness probe `connection refused`。
