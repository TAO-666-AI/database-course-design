<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="brand-logo auth-logo">景</div>
      <h1>{{ roleTitle }}</h1>
      <p>{{ roleTip }}</p>
      <el-form label-position="top" @submit.prevent>
        <el-form-item label="手机号/账号">
          <el-input v-model="form.account" size="large" placeholder="请输入手机号或账号" clearable />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" size="large" placeholder="请输入登录密码" show-password />
        </el-form-item>
        <el-button class="full-btn" type="primary" size="large" :loading="loading" @click="handleLogin">登录</el-button>
      </el-form>
      <div class="auth-links" v-if="loginRole === 'tourist'">
        <span>还没有账号？</span>
        <router-link to="/register">去注册</router-link>
      </div>
      <div class="auth-links" v-else>
        <span>管理员账号由系统初始化或后台分配</span>
      </div>
      <div class="mode-links">
        <router-link to="/">返回身份选择</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/auth'
import { useUserStore } from '../stores/user'

const router = useRouter()
const route = useRoute()
const store = useUserStore()
const loading = ref(false)
const form = reactive({ account: '', password: '' })
const loginRole = computed(() => route.query.role === 'admin' ? 'admin' : 'tourist')
const roleTitle = computed(() => loginRole.value === 'admin' ? '管理员登录' : '游客登录')
const roleTip = computed(() => loginRole.value === 'admin' ? '登录后台维护中山陵景点、路线和反馈数据' : '登录后使用中山陵景点收藏、反馈和文本问答服务')

const handleLogin = async () => {
  if (!form.account || !form.password) return ElMessage.warning('请输入账号和密码')
  loading.value = true
  try {
    const res = await login(form)
    if (res.code === 200) {
      store.setLogin(res.data.token, res.data.user)
      ElMessage.success('登录成功')
      router.push(res.data.user.role === 'admin' ? '/admin/dashboard' : '/tourist/home')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px;
}
.auth-card {
  width: 500px;
  max-width: 92vw;
  padding: 38px 32px 30px;
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 24px 70px rgba(30, 65, 90, 0.13);
}
.auth-logo {
  margin: 0 auto 16px;
}
h1 {
  text-align: center;
  margin: 0;
  font-size: 28px;
}
p {
  text-align: center;
  color: var(--muted);
  margin: 10px 0 28px;
}
.full-btn {
  width: 100%;
  height: 54px;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 700;
}
.auth-links {
  margin-top: 28px;
  display: flex;
  gap: 10px;
  justify-content: center;
  color: var(--muted);
}
.auth-links a {
  color: var(--primary-dark);
  font-weight: 800;
}
.mode-links {
  margin-top: 16px;
  display: flex;
  justify-content: center;
  color: var(--muted);
}
.mode-links a {
  color: var(--primary-dark);
  font-weight: 700;
}
</style>
