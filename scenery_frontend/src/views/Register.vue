<template>
  <div class="auth-page">
    <div class="auth-card register-card">
      <h1>欢迎注册</h1>
      <p>创建账号，开启景区导览服务</p>
      <el-form label-position="top" @submit.prevent>
        <el-form-item label="用户名">
          <el-input v-model="form.username" size="large" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" size="large" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" size="large" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.confirm_password" size="large" placeholder="请再次输入密码" show-password />
        </el-form-item>
        <el-button class="full-btn" type="primary" size="large" :loading="loading" @click="handleRegister">注册</el-button>
      </el-form>
      <div class="auth-links">
        <span>已有账号？</span>
        <router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '../api/auth'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', phone: '', password: '', confirm_password: '' })

const handleRegister = async () => {
  if (!form.username || !form.phone || !form.password) return ElMessage.warning('请完整填写注册信息')
  if (form.password !== form.confirm_password) return ElMessage.warning('两次密码不一致')
  loading.value = true
  try {
    const res = await register(form)
    if (res.code === 200) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
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
  width: 520px;
  max-width: 92vw;
  padding: 34px 32px 30px;
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 24px 70px rgba(30, 65, 90, 0.13);
}
h1 {
  text-align: center;
  margin: 0;
  font-size: 28px;
}
p {
  text-align: center;
  color: var(--muted);
  margin: 10px 0 24px;
}
.full-btn {
  width: 100%;
  height: 54px;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 700;
}
.auth-links {
  margin-top: 24px;
  display: flex;
  gap: 10px;
  justify-content: center;
  color: var(--muted);
}
.auth-links a {
  color: var(--primary-dark);
  font-weight: 800;
}
</style>
