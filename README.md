<div align="center">

<img src="https://img.shields.io/badge/version-v1.0--alpha-FF6B8A?style=for-the-badge" alt="version"/>
<img src="https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="django"/>
<img src="https://img.shields.io/badge/Vue-3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="vue"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="postgresql"/>
<img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="redis"/>

<br/><br/>

# 💝 TryDate · 校园心动匹配平台

### *"在最好的年纪，遇见刚刚好的你"*

一款专为高校在校生设计的心动匹配与交友平台。  
不靠颜值滤镜，通过趣味问卷、价值观匹配和温暖的互动设计，  
帮你遇见那个「感觉刚刚好」的人。

</div>

---

## ✨ 产品特色

| 特色 | 说明 |
|------|------|
| 🧠 **灵魂先行** | 五维问卷（价值观 / 性格 / 兴趣 / 生活习惯 / 约会偏好）先了解再心动 |
| 💌 **每周心动** | 每周日 20:00 精准推送一位契合度最高的人，附五维雷达图报告 |
| 🤝 **双向确认** | 心动❤️ / 再想想，双方均选心动才解锁聊天，无尬匹配 |
| 💬 **实时聊天** | WebSocket 驱动，支持文字 & 图片消息 |
| 📝 **话题动态** | 匿名发布校园日常，点赞互动，保护隐私 |
| 🔒 **安全可靠** | JWT 鉴权、举报拉黑、敏感词过滤、邮箱/手机双验证 |

---

## 🏗 技术栈

```
后端          Django 5.x + Django REST Framework
实时通信      Django Channels + Redis Channel Layer (WebSocket)
数据库        PostgreSQL 16
缓存 & 队列   Redis 7
定时任务      Celery
身份认证      JWT (djangorestframework-simplejwt)
前端 (规划中) Vue 3 + Vite + TailwindCSS
```

---

## 📁 项目结构

```
TryDate/
├── backend/
│   ├── config/          # Django 项目配置 (settings, urls, asgi)
│   ├── users/           # 用户注册 / 登录 / 资料 / 黑名单
│   ├── questionnaire/   # 灵魂问卷（五维度 JSON 存储）
│   ├── matching/        # Gale-Shapley 双向稳定匹配算法
│   ├── chat/            # WebSocket 实时聊天 + 举报
│   ├── posts/           # 话题动态（发布 / 点赞）
│   ├── requirements.txt
│   └── README.md        # 后端启动指南
└── PRD-校园恋爱匹配平台.md   # 完整产品需求文档
```

---

## 🚀 快速启动（后端）

### 环境要求
- Python 3.11+
- PostgreSQL 16
- Redis 7

### 步骤

```bash
# 1. 克隆项目
git clone https://github.com/a2722034443/TryDate.git
cd TryDate/backend

# 2. 创建并激活虚拟环境
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DB_PASSWORD 等配置

# 5. 在 PostgreSQL 中创建数据库
# psql -U postgres -c "CREATE DATABASE trydate;"

# 6. 执行迁移
python manage.py migrate

# 7. 创建管理员账号
python manage.py createsuperuser

# 8. 启动服务
python manage.py runserver
# 或使用 daphne 启用 WebSocket：
# daphne -p 8000 config.asgi:application
```

服务启动后：
- **API**：http://localhost:8000/api/
- **管理后台**：http://localhost:8000/admin/
- **WebSocket**：`ws://localhost:8000/ws/chat/{room_id}/`

---

## 📡 API 概览

<details>
<summary><b>👤 用户 /api/users/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/send-code/` | 发送邮箱或短信验证码 |
| POST | `/register/` | 注册（验证码 + 基础信息） |
| POST | `/login/` | 登录（验证码）|
| POST | `/token/refresh/` | 刷新 JWT Token |
| GET/PATCH | `/profile/` | 获取 / 更新个人资料 |

</details>

<details>
<summary><b>📋 问卷 /api/questionnaire/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 获取问卷答案与完成度 |
| PATCH | `/` | 提交 / 更新问卷答案（增量合并） |

</details>

<details>
<summary><b>💘 匹配 /api/match/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/current/` | 查看本周匹配 + 契合度报告 |
| POST | `/{id}/respond/` | 心动❤️ 或 再想想 |
| GET | `/history/` | 历史匹配记录 |
| POST | `/trigger/` | 手动触发匹配（管理员） |

</details>

<details>
<summary><b>💬 聊天 /api/chat/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/rooms/` | 聊天室列表 |
| GET | `/rooms/{id}/messages/` | 消息历史 |
| POST | `/rooms/{id}/upload/` | 上传图片 |
| POST | `/report/` | 举报用户 |
| POST | `/block/{user_id}/` | 拉黑用户 |

</details>

<details>
<summary><b>📝 动态 /api/posts/</b></summary>

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 话题动态列表 |
| POST | `/create/` | 发布动态 |
| POST | `/{id}/like/` | 点赞 / 取消点赞 |
| DELETE | `/{id}/delete/` | 删除自己的动态 |

</details>

---

## 🧮 匹配算法

采用**两阶段方案**：

1. **契合度计算**：基于五维问卷，使用 Jaccard 相似度、Spearman 秩相关、量表差值等方法，加权计算总契合度（满分 100 分）
2. **Gale-Shapley 双向稳定匹配**：保证不存在"双方都更希望与对方匹配"的情况，消除不稳定匹配对

```
总契合度 = 基础偏好 × 15%
         + 爱情观 & 价值观 × 40%
         + 性格 & 生活习惯 × 25%
         + 兴趣 & 个性 × 15%
         + 约会偏好 × 5%
```

---

## 🗺 开发路线图

- [x] 后端框架搭建
- [x] 用户注册 / 登录（验证码）
- [x] 灵魂问卷系统
- [x] Gale-Shapley 匹配算法
- [x] WebSocket 实时聊天
- [x] 话题动态
- [ ] Vue 3 前端开发
- [ ] Celery 定时匹配任务配置
- [ ] 图片上传云存储（MinIO / OSS）
- [ ] 生产环境部署

---

## 📄 License

MIT © 2026 TryDate Team

---

<div align="center">
  <sub>Made with 💝 for campus love</sub>
</div>
