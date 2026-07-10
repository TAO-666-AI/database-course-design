<template>
  <section>
    <h1 class="page-title">反馈管理</h1>
    <p class="page-subtitle">查看游客评价、反馈内容与满意度统计。</p>
    <div class="stats-grid">
      <div class="stat-card"><strong>{{ summary.total || 0 }}</strong><span>反馈总数</span></div>
      <div class="stat-card"><strong>{{ summary.avg_rating || 0 }}</strong><span>平均评分</span></div>
    </div>
    <div class="toolbar">
      <el-select v-model="query.status" placeholder="状态" clearable style="width: 160px">
        <el-option label="待处理" value="pending" />
        <el-option label="已处理" value="processed" />
        <el-option label="已忽略" value="ignored" />
      </el-select>
      <el-button type="primary" @click="load">查询</el-button>
    </div>
    <el-table :data="items" class="soft-card">
      <el-table-column prop="username" label="用户" width="120" />
      <el-table-column prop="type" label="类型" width="120" />
      <el-table-column prop="rating" label="评分" width="100" />
      <el-table-column prop="content" label="内容" />
      <el-table-column prop="status" label="状态" width="100" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" @click="open(row)">处理</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" title="处理反馈" width="520px">
      <el-form label-position="top">
        <el-form-item label="处理状态">
          <el-select v-model="form.status">
            <el-option label="待处理" value="pending" />
            <el-option label="已处理" value="processed" />
            <el-option label="已忽略" value="ignored" />
          </el-select>
        </el-form-item>
        <el-form-item label="回复内容"><el-input v-model="form.reply" type="textarea" :rows="4" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { adminFeedbacks, feedbackStats, updateFeedback } from '../../api/admin'
const items = ref([])
const summary = ref({})
const visible = ref(false)
const editingId = ref(null)
const query = reactive({ status: '' })
const form = reactive({ status: 'processed', reply: '' })
const load = async () => {
  const res = await adminFeedbacks(query)
  if (res.code === 200) items.value = res.data.items
  const stat = await feedbackStats()
  if (stat.code === 200) summary.value = stat.data.summary
}
const open = (row) => {
  editingId.value = row.id
  form.status = row.status
  form.reply = row.reply || ''
  visible.value = true
}
const save = async () => {
  await updateFeedback(editingId.value, form)
  visible.value = false
  load()
}
onMounted(load)
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
  margin-bottom: 18px;
}
.stat-card {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  text-align: center;
}
.stat-card strong {
  display: block;
  font-size: 34px;
  color: var(--primary);
}
.stat-card span {
  color: var(--muted);
}
</style>
