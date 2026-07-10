import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 15000
})

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

request.interceptors.response.use(
  (response) => {
    const body = response.data
    if (body && typeof body.code !== 'undefined' && body.code !== 200) {
      ElMessage.warning(body.msg || '请求失败')
    }
    return body
  },
  (error) => {
    const status = error.response?.status
    if (status === 401) {
      const store = useUserStore()
      store.logout()
      ElMessage.error('登录已失效，请重新登录')
      window.location.href = '/login'
    } else {
      ElMessage.error(error.response?.data?.detail || error.message || '网络错误')
    }
    return Promise.reject(error)
  }
)

export default request
