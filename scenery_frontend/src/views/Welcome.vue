<template>
  <div class="welcome-page">
    <div class="welcome-card">
      <div class="brand-logo big-logo">景</div>
      <h1>南京中山陵景区导览管理系统</h1>
      <p class="subtitle">请选择登录身份，进入对应的系统页面</p>

      <div class="role-grid">
        <div class="role-card tourist" @click="goLogin('tourist')">
          <div class="role-icon"><User /></div>
          <h2>游客登录</h2>
          <p>浏览中山陵景点、收藏景点、提交反馈、使用文本问答</p>
          <el-button type="primary" round>进入游客端</el-button>
        </div>

        <div class="role-card admin" @click="goLogin('admin')">
          <div class="role-icon"><Setting /></div>
          <h2>管理员登录</h2>
          <p>维护中山陵景点、路线、FAQ、反馈和聊天记录</p>
          <el-button type="primary" plain round>进入管理端</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goLogin = (role) => {
  router.push({ path: '/login', query: { role } })
}
</script>

<style scoped>
.welcome-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 36px;
}
.welcome-card {
  width: 860px;
  max-width: 94vw;
  padding: 44px;
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 24px 80px rgba(27, 74, 91, 0.14);
  text-align: center;
}
.big-logo {
  width: 72px;
  height: 72px;
  border-radius: 24px;
  font-size: 30px;
  margin: 0 auto 18px;
}
h1 {
  margin: 0;
  font-size: 34px;
  font-weight: 900;
}
.subtitle {
  margin: 12px 0 34px;
  color: var(--muted);
  font-size: 17px;
}
.role-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 22px;
}
.role-card {
  min-height: 260px;
  border-radius: 24px;
  padding: 30px 24px;
  border: 1px solid #d4e9ed;
  cursor: pointer;
  transition: 0.2s ease;
}
.role-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 40px rgba(18, 164, 147, 0.13);
}
.role-card.tourist {
  background: linear-gradient(135deg, #e8fbf8, #f7fffe);
}
.role-card.admin {
  background: linear-gradient(135deg, #eef5ff, #fbfdff);
}
.role-icon {
  width: 68px;
  height: 68px;
  border-radius: 22px;
  display: grid;
  place-items: center;
  margin: 0 auto 18px;
  color: var(--primary-dark);
  background: #fff;
}
.role-icon :deep(svg) {
  width: 34px;
  height: 34px;
}
.role-card h2 {
  margin: 0;
  font-size: 24px;
}
.role-card p {
  min-height: 48px;
  margin: 12px 0 24px;
  color: var(--muted);
  line-height: 1.7;
}
@media (max-width: 720px) {
  .welcome-card {
    padding: 30px 22px;
  }
  .role-grid {
    grid-template-columns: 1fr;
  }
}
</style>
