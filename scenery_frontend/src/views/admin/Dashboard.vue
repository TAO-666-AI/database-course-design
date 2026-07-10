<template>
  <section>
    <h1 class="page-title">首页概览</h1>
    <p class="page-subtitle">南京中山陵景区导览管理系统数据概览。</p>
    <div class="stats-grid">
      <div class="stat-card">
        <strong>{{ counts.users }}</strong>
        <span>用户数量</span>
      </div>
      <div class="stat-card">
        <strong>{{ counts.spots }}</strong>
        <span>景点数量</span>
      </div>
      <div class="stat-card">
        <strong>{{ counts.routes }}</strong>
        <span>路线数量</span>
      </div>
      <div class="stat-card">
        <strong>{{ stats.total || 0 }}</strong>
        <span>反馈数量</span>
      </div>
    </div>
    <div class="soft-card panel">
      <h3>系统说明</h3>
      <p>本后台面向景区日常运营管理，支持工作人员统一维护景点资料、游览路线、常见问题、游客反馈和问答记录，帮助景区及时更新导览信息、跟进游客诉求，并为游客提供更加清晰、稳定的导览服务。</p>
    </div>
    <div class="dashboard-grid">
      <div class="soft-card panel">
        <h3>运营待办</h3>
        <div class="todo-list">
          <div class="todo-item">
            <strong>{{ pendingFeedbacks }}</strong>
            <span>待处理游客反馈</span>
            <router-link to="/admin/feedbacks">去处理</router-link>
          </div>
          <div class="todo-item">
            <strong>{{ counts.spots }}</strong>
            <span>在库景点资料</span>
            <router-link to="/admin/spots">维护景点</router-link>
          </div>
          <div class="todo-item">
            <strong>{{ counts.routes }}</strong>
            <span>已配置游览路线</span>
            <router-link to="/admin/routes">维护路线</router-link>
          </div>
        </div>
      </div>
      <div class="soft-card panel">
        <h3>快捷入口</h3>
        <div class="quick-grid">
          <router-link to="/admin/spots">新增或编辑景点</router-link>
          <router-link to="/admin/routes">调整路线节点</router-link>
          <router-link to="/admin/faqs">维护常见问题</router-link>
          <router-link to="/admin/chats">查看问答记录</router-link>
        </div>
      </div>
    </div>
    <div class="dashboard-grid">
      <div class="soft-card panel">
        <h3>反馈概况</h3>
        <div class="feedback-summary">
          <div>
            <strong>{{ stats.total || 0 }}</strong>
            <span>累计反馈</span>
          </div>
          <div>
            <strong>{{ stats.avg_rating || '-' }}</strong>
            <span>平均评分</span>
          </div>
        </div>
        <div class="tag-row">
          <span v-for="item in feedbackStatus" :key="item.status">{{ statusText(item.status) }}：{{ item.count }}</span>
        </div>
      </div>
      <div class="soft-card panel">
        <h3>导览维护建议</h3>
        <ul class="tips">
          <li>优先处理游客反馈中涉及开放时间、门票和路线的问题。</li>
          <li>路线调整后同步检查相关景点顺序，保持游客端展示清晰。</li>
          <li>定期查看聊天记录，将高频问题补充到 FAQ 知识库。</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { adminRoutes, adminSpots, adminUsers, feedbackStats } from '../../api/admin'

const counts = reactive({ users: 0, spots: 0, routes: 0 })
const stats = ref({})
const feedbackStatus = ref([])
const pendingFeedbacks = computed(() => feedbackStatus.value.find((item) => item.status === 'pending')?.count || 0)
const statusText = (value) => ({ pending: '待处理', processed: '已处理', ignored: '已忽略' }[value] || value)
onMounted(async () => {
  const [u, s, r, f] = await Promise.all([adminUsers(), adminSpots(), adminRoutes(), feedbackStats()])
  counts.users = u.data?.total || 0
  counts.spots = s.data?.total || 0
  counts.routes = r.data?.total || 0
  stats.value = f.data?.summary || {}
  feedbackStatus.value = f.data?.by_status || []
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(160px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}
.stat-card {
  background: #fff;
  border-radius: 20px;
  padding: 28px;
  text-align: center;
  box-shadow: 0 12px 28px rgba(25, 68, 91, 0.06);
}
.stat-card strong {
  display: block;
  font-size: 38px;
  color: var(--primary);
  margin-bottom: 10px;
}
.stat-card span {
  color: var(--muted);
}
.panel {
  padding: 24px;
  margin-bottom: 24px;
}
.panel p {
  color: var(--muted);
  line-height: 1.9;
}
.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 24px;
}
.todo-list {
  display: grid;
  gap: 12px;
}
.todo-item {
  display: grid;
  grid-template-columns: 64px 1fr auto;
  align-items: center;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid #edf2f5;
}
.todo-item:last-child {
  border-bottom: 0;
}
.todo-item strong,
.feedback-summary strong {
  color: var(--primary);
  font-size: 28px;
}
.todo-item span {
  color: var(--muted);
}
.todo-item a,
.quick-grid a {
  color: var(--primary-dark);
  font-weight: 700;
}
.quick-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.quick-grid a {
  padding: 16px;
  border-radius: 14px;
  background: var(--primary-soft);
  border: 1px solid #cce9ea;
}
.feedback-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin-bottom: 14px;
}
.feedback-summary div {
  padding: 16px;
  border-radius: 14px;
  background: #f7fdfc;
}
.feedback-summary span {
  display: block;
  color: var(--muted);
  margin-top: 4px;
}
.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.tag-row span {
  padding: 8px 12px;
  border-radius: 999px;
  background: #edf5ff;
  color: #60718a;
}
.tips {
  margin: 0;
  padding-left: 20px;
  color: var(--muted);
  line-height: 2;
}
@media (max-width: 960px) {
  .stats-grid,
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
