<template>
  <section class="mine">
    <div class="avatar-ring"><User /></div>
    <h1>{{ store.user?.username || '游客' }}</h1>
    <p>管理个人收藏、反馈与历史问答记录</p>
    <el-button class="login-btn" type="primary" plain @click="logout">退出登录</el-button>
    <div class="menu-card">
      <router-link to="/tourist/favorites">
        <span class="menu-icon"><Star /></span>
        <span class="menu-text">我的收藏</span>
        <ArrowRight class="menu-arrow" />
      </router-link>
      <router-link to="/tourist/chat?history=1">
        <span class="menu-icon"><ChatDotRound /></span>
        <span class="menu-text">历史问答</span>
        <ArrowRight class="menu-arrow" />
      </router-link>
      <router-link to="/tourist/feedback">
        <span class="menu-icon"><EditPen /></span>
        <span class="menu-text">我的反馈</span>
        <ArrowRight class="menu-arrow" />
      </router-link>
      <router-link to="/tourist/faqs">
        <span class="menu-icon"><InfoFilled /></span>
        <span class="menu-text">常见问题</span>
        <ArrowRight class="menu-arrow" />
      </router-link>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
const store = useUserStore()
const router = useRouter()
const logout = () => {
  store.logout()
  router.push('/login')
}
</script>

<style scoped>
.mine {
  text-align: center;
}
.avatar-ring {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  border: 3px solid var(--primary);
  margin: 0 auto 16px;
  display: grid;
  place-items: center;
  color: var(--primary-dark);
}
.avatar-ring svg {
  width: 42px;
  height: 42px;
}
h1 {
  margin: 0;
}
p {
  color: var(--muted);
}
.login-btn {
  width: 100%;
  height: 54px;
  border-radius: 16px;
  margin: 18px 0;
}
.menu-card {
  background: #fff;
  border-radius: 18px;
  overflow: hidden;
}
.menu-card a {
  height: 66px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  border-bottom: 1px solid #edf2f5;
  font-size: 17px;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
}
.menu-card a:last-child {
  border-bottom: 0;
}
.menu-icon {
  width: 30px;
  height: 30px;
  flex: 0 0 30px;
  display: grid;
  place-items: center;
  color: #6f7f95;
}
.menu-icon :deep(svg) {
  width: 24px;
  height: 24px;
  display: block;
}
.menu-text {
  flex: 1;
  min-width: 0;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
}
.menu-arrow {
  margin-left: auto;
  color: #a8b5c5;
  width: 20px;
  height: 20px;
  flex: 0 0 20px;
}
</style>
