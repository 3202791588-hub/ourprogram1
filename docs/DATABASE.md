# 数据库

本地 Docker 开发环境使用 PostgreSQL 16；CloudBase 云托管环境使用 CloudBase MySQL。Django 通过环境变量选择连接，业务模型和 Migration 保持同一套。模型按 `users`、`tests`、`results`、`relations`、`ads`、`analytics` app 划分。

关键不变量：

- `Test + version` 唯一，历史 Session 固定引用 TestVersion。
- `Session + Question` 唯一，重复保存答案为更新。
- Session 与 ResultSnapshot 一对一，结果是不可变快照。
- `User + Result` 解锁唯一。
- Invite Code 为 `secrets.token_urlsafe(32)`，不含用户 ID。
- Invite 与 Relationship 一对一，Relationship 与 Report 一对一。

任何 Schema 变化必须提交 Django Migration；禁止手工改库。

云端数据库网络：

- 免费 Demo 不支持云托管 VPC 时，使用直连服务的外网地址和外网端口。
- 正式环境应开启云托管私有网络，使用 MySQL 内网地址。
- 数据库账号主机范围 `%` 与应用 `DB_HOST` 不是同一个配置。
- 密码和 `DJANGO_SECRET_KEY` 只存云托管环境变量，不写入代码包。
