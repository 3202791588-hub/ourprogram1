# API

基础路径：`/api/v1/`；响应结构：`{"code":0,"message":"ok","data":{}}`。

主要端点：

- `POST /auth/wechat`
- `GET /tests`、`GET /tests/{slug}`
- `POST /test-sessions`、`GET /test-sessions/{id}`
- `PUT /test-sessions/{id}/answers`、`POST /test-sessions/{id}/submit`
- `GET /results/{id}/preview`、`GET /results/{id}/full`、`POST /results/{id}/unlock`
- `POST /relation-invites`、`GET /relation-invites/{code}`、`POST /relation-invites/{code}/accept`
- `GET /relationships/{id}`、`GET /me/results`、`GET /me/relationships`
- `POST /events`、`DELETE /me/data`

除登录、健康检查外均需 Bearer JWT。交互式 OpenAPI 位于 `/api/docs/`，Schema 位于 `/api/schema/`。
