<template>
  <section>
    <h1 class="page-title">聊天记录</h1>
    <p class="page-subtitle">查看游客文本问答记录，用于完善 FAQ 知识库。</p>
    <div class="toolbar">
      <el-input v-model="keyword" placeholder="搜索用户或聊天内容" clearable />
      <el-button type="primary" @click="load">查询</el-button>
    </div>
    <el-table :data="items" class="soft-card" v-loading="loading">
      <el-table-column prop="username" label="用户" width="120" />
      <el-table-column prop="role" label="角色" width="100" />
      <el-table-column prop="source" label="来源" width="110" />
      <el-table-column prop="content" label="内容" />
      <el-table-column prop="created_at" label="时间" width="180" />
    </el-table>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { adminChats } from '../../api/admin'
const keyword = ref('')
const loading = ref(false)
const items = ref([])
const load = async () => {
  loading.value = true
  try {
    const res = await adminChats({ keyword: keyword.value })
    if (res.code === 200) items.value = res.data.items
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>
