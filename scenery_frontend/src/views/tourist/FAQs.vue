<template>
  <section>
    <h1 class="page-title">常见问题</h1>
    <p class="page-subtitle">优先从本地 FAQ 中查询南京中山陵常见问题。</p>
    <div class="toolbar">
      <el-input v-model="keyword" placeholder="搜索门票、开放时间、路线等" clearable @keyup.enter="load" />
      <el-button type="primary" @click="load">搜索</el-button>
    </div>
    <el-collapse v-model="active">
      <el-collapse-item v-for="item in items" :key="item.id" :name="item.id">
        <template #title>
          <strong>{{ item.question }}</strong>
          <el-tag v-if="item.category" size="small" type="success" style="margin-left: 10px">{{ item.category }}</el-tag>
        </template>
        <p class="answer">{{ item.answer }}</p>
      </el-collapse-item>
    </el-collapse>
    <div v-if="!items.length" class="empty-hint">暂无 FAQ 数据</div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getFaqs } from '../../api/tourist'
const keyword = ref('')
const items = ref([])
const active = ref([])
const load = async () => {
  const res = await getFaqs({ keyword: keyword.value })
  if (res.code === 200) items.value = res.data.items
}
onMounted(load)
</script>

<style scoped>
.answer {
  color: var(--muted);
  line-height: 1.8;
}
:deep(.el-collapse) {
  border: 0;
  background: transparent;
}
:deep(.el-collapse-item) {
  background: #fff;
  border-radius: 16px;
  margin-bottom: 12px;
  overflow: hidden;
  border: 1px solid #e2eef2;
}
:deep(.el-collapse-item__header) {
  padding: 0 18px;
  border: 0;
}
:deep(.el-collapse-item__content) {
  padding: 0 18px 16px;
}
</style>
