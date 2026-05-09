# DLNUDate 后端

## 技术栈
- Django 5.x + Django REST Framework
- PostgreSQL 16
- Redis 7
- Django Channels (WebSocket)
- Celery (定时匹配任务)

## 本地启动步骤

### 1. 准备数据库
在 pgAdmin 或 psql 中执行：
```sql
CREATE DATABASE dlnudate;
```

### 2. 配置环境变量
编辑 `.env` 文件，填入 PostgreSQL 密码：
```
DB_PASSWORD=你的postgres密码
```

### 3. 执行数据库迁移
```powershell
.\venv\Scripts\python manage.py migrate
```

### 4. 创建管理员账号
```powershell
.\venv\Scripts\python manage.py createsuperuser
```

### 5. 启动开发服务器
```powershell
.\venv\Scripts\python manage.py runserver
```
服务运行在 http://localhost:8000

如需 WebSocket 支持（聊天），改用 daphne：
```powershell
.\venv\Scripts\daphne -p 8000 config.asgi:application
```

## API 接口总览

| 模块 | 接口 |
|------|------|
| 发送验证码 | POST `/api/users/send-code/` |
| 注册 | POST `/api/users/register/` |
| 登录 | POST `/api/users/login/` |
| 刷新Token | POST `/api/users/token/refresh/` |
| 个人资料 | GET/PATCH `/api/users/profile/` |
| 问卷 | GET/PATCH `/api/questionnaire/` |
| 本周匹配 | GET `/api/match/current/` |
| 心动/再想想 | POST `/api/match/{id}/respond/` |
| 匹配历史 | GET `/api/match/history/` |
| 触发匹配(管理员) | POST `/api/match/trigger/` |
| 聊天室列表 | GET `/api/chat/rooms/` |
| 消息列表 | GET `/api/chat/rooms/{id}/messages/` |
| 上传图片 | POST `/api/chat/rooms/{id}/upload/` |
| 举报 | POST `/api/chat/report/` |
| 拉黑 | POST `/api/chat/block/{user_id}/` |
| 话题动态列表 | GET `/api/posts/` |
| 发布动态 | POST `/api/posts/create/` |
| 点赞/取消 | POST `/api/posts/{id}/like/` |
| 删除动态 | DELETE `/api/posts/{id}/delete/` |

## WebSocket
```
ws://localhost:8000/ws/chat/{room_id}/
```
发送格式：`{"type": "text", "content": "消息内容"}`

## 手动触发每周匹配（开发调试）
```powershell
.\venv\Scripts\python manage.py shell -c "from matching.tasks import run_weekly_match; run_weekly_match()"
```
