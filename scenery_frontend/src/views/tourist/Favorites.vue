<template>
  <section>
    <h1 class="page-title">我的收藏</h1>
    <p class="page-subtitle">管理自己收藏的景区景点。</p>
    <div v-loading="loading" class="spot-list">
      <article v-for="item in items" :key="item.favorite_id" class="spot-card">
        <h3>{{ item.name }}</h3>
        <p>{{ item.description }}</p>
        <div class="meta">📍 {{ item.location }}　收藏时间：{{ item.favorited_at }}</div>
        <el-button type="danger" plain @click="remove(item.id)">取消收藏</el-button>
      </article>
      <div v-if="!items.length" class="empty-hint">你还没有收藏景点</div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getFavorites, removeFavorite } from '../../api/tourist'

const loading = ref(false)
const items = ref([])
const load = async () => {
  loading.value = true
  try {
    const res = await getFavorites()
    if (res.code === 200) items.value = res.data.items
  } finally {
    loading.value = false
  }
}
const remove = async (id) => {
  const res = await removeFavorite(id)
  if (res.code === 200) {
    ElMessage.success('已取消收藏')
    load()
  }
}
onMounted(load)
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
}
h3 {
  margin: 0 0 10px;
}
p,
.meta {
  color: var(--muted);
}
</style>
