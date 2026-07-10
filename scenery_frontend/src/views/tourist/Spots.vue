<template>
  <section>
    <h1 class="page-title">景点介绍</h1>
    <p class="page-subtitle">浏览南京中山陵景点信息，支持名称、位置和分类查询。</p>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="搜索景点名称/位置" clearable @keyup.enter="load" />
      <el-select v-model="query.category" placeholder="选择景点分类" clearable>
        <el-option v-for="item in categories" :key="item" :label="item" :value="item" />
      </el-select>
      <el-button type="primary" @click="load">查询</el-button>
    </div>
    <div v-loading="loading" class="spot-list">
      <article v-for="item in items" :key="item.id" class="spot-card">
        <div>
          <h3>{{ item.name }}</h3>
          <el-tag type="success">{{ item.category || '未分类' }}</el-tag>
        </div>
        <p>{{ item.description }}</p>
        <div class="meta">
          <span>📍 {{ item.location || '暂无位置' }}</span>
          <span>🕘 {{ item.open_time || '暂无开放时间' }}</span>
          <span>￥{{ item.ticket_price }}</span>
        </div>
        <el-button type="primary" plain @click="favorite(item.id)">收藏景点</el-button>
      </article>
      <div v-if="!items.length" class="empty-hint">暂无景点数据</div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { addFavorite, getSpotCategories, getSpots } from '../../api/tourist'

const loading = ref(false)
const items = ref([])
const categories = ref([])
const query = reactive({ keyword: '', category: '' })

const loadCategories = async () => {
  const res = await getSpotCategories()
  if (res.code === 200) categories.value = res.data.items
}
const load = async () => {
  loading.value = true
  try {
    const res = await getSpots(query)
    if (res.code === 200) items.value = res.data.items
  } finally {
    loading.value = false
  }
}
const favorite = async (id) => {
  const res = await addFavorite(id)
  if (res.code === 200) ElMessage.success('收藏成功')
}
onMounted(() => {
  loadCategories()
  load()
})
</script>

<style scoped>
.spot-list {
  display: grid;
  gap: 16px;
}
.spot-card {
  background: #fff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 12px 28px rgba(25, 68, 91, 0.06);
}
.spot-card h3 {
  display: inline-block;
  margin: 0 12px 10px 0;
  font-size: 21px;
}
.spot-card p {
  color: var(--muted);
  line-height: 1.7;
}
.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #60718a;
  margin-bottom: 14px;
}
</style>
