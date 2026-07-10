# 南京中山陵景区导览管理系统 - Vue 前端

技术栈：

- Vue 3
- Vite
- Element Plus
- Vue Router
- Pinia
- Axios

## 启动前提

请先启动后端：

```bash
cd ../scenery_backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端默认地址：

```text
http://127.0.0.1:8000
```

## 启动前端

```bash
cd scenery_frontend
npm install
npm run dev
```

浏览器访问：

```text
http://127.0.0.1:5173
```

## 默认管理员账号

```text
账号：admin
密码：Admin123456
```

## 目录说明

```text
src/
├── api/             # Axios 请求封装，按游客端和管理端区分
├── router/          # Vue Router 路由配置和登录守卫
├── stores/          # Pinia 登录状态
├── layouts/         # 游客端移动风布局、管理端后台布局
├── views/
│   ├── tourist/     # 游客端页面
│   └── admin/       # 管理端页面
└── styles/          # 全局样式
```

## 前后端联通方式

开发环境使用 Vite 代理：

```js
proxy: {
  '/api': {
    target: 'http://127.0.0.1:8000',
    changeOrigin: true
  }
}
```

因此前端直接请求 `/api/...` 即可访问 FastAPI 后端。
