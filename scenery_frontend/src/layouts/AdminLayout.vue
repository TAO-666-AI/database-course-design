<template>
  <div class="admin-shell">
    <aside class="admin-side">
      <div class="admin-brand">
        <div class="brand-logo">景</div>
        <div>
          <strong>中山陵导览管理</strong>
          <span>后台管理系统</span>
        </div>
      </div>
      <router-link to="/admin/dashboard"><DataBoard />首页概览</router-link>
      <router-link to="/admin/users"><User />用户管理</router-link>
      <router-link to="/admin/spots"><Location />景点管理</router-link>
      <router-link to="/admin/routes"><Guide />路线管理</router-link>
      <router-link to="/admin/faqs"><Document />FAQ 管理</router-link>
      <router-link to="/admin/feedbacks"><ChatLineRound />反馈管理</router-link>
      <router-link to="/admin/chats"><ChatDotRound />聊天记录</router-link>
      <button class="back-btn" @click="logout">退出登录</button>
    </aside>
    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
const router = useRouter()
const userStore = useUserStore()

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.admin-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 280px 1fr;
  background: #f1f7fb;
}
.admin-side {
  background: rgba(255, 255, 255, 0.92);
  border-right: 1px solid #dfecef;
  padding: 22px 14px;
  position: sticky;
  top: 0;
  height: 100vh;
}
.admin-brand {
  display: flex;
  gap: 14px;
  align-items: center;
  padding: 0 8px 24px;
  border-bottom: 1px solid #e5eff2;
  margin-bottom: 20px;
}
.admin-brand strong {
  display: block;
  font-size: 19px;
}
.admin-brand span {
  color: var(--muted);
}
.admin-side a {
  height: 54px;
  border-radius: 14px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #536173;
  margin-bottom: 8px;
}
.admin-side a svg {
  width: 22px;
  height: 22px;
}
.admin-side a.router-link-active {
  background: #dcf3f1;
  color: var(--primary-dark);
  font-weight: 800;
}
.admin-main {
  padding: 32px;
  min-width: 0;
}
.back-btn {
  position: absolute;
  bottom: 24px;
  left: 22px;
  right: 22px;
  height: 44px;
  border: 0;
  border-radius: 12px;
  background: #eef7f7;
  color: var(--primary-dark);
  font-weight: 700;
  cursor: pointer;
}
@media (max-width: 900px) {
  .admin-shell {
    grid-template-columns: 1fr;
  }
  .admin-side {
    position: relative;
    height: auto;
  }
}
</style>
