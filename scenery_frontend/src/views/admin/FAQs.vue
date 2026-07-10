<template>
  <section>
    <h1 class="page-title">FAQ 管理</h1>
    <p class="page-subtitle">维护常见问题库，供游客文本问答优先匹配。</p>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="问题/答案/关键词" clearable />
      <el-button type="primary" @click="load">查询</el-button>
      <el-button type="primary" plain @click="open()">新增 FAQ</el-button>
    </div>
    <el-table :data="items" class="soft-card" v-loading="loading">
      <el-table-column type="index" label="序号" width="80" />
      <el-table-column prop="question" label="问题" />
      <el-table-column prop="category" label="分类" width="120" />
      <el-table-column prop="keywords" label="关键词" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="open(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" title="FAQ 信息" width="680px">
      <el-form label-position="top">
        <el-form-item label="问题"><el-input v-model="form.question" /></el-form-item>
        <el-form-item label="答案"><el-input v-model="form.answer" type="textarea" :rows="4" /></el-form-item>
        <el-form-item label="分类"><el-input v-model="form.category" /></el-form-item>
        <el-form-item label="关键词"><el-input v-model="form.keywords" placeholder="逗号分隔，如 门票,价格" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort_order" /></el-form-item>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminFaqs, createFaq, deleteFaq, updateFaq } from '../../api/admin'
const loading = ref(false)
const visible = ref(false)
const editingId = ref(null)
const items = ref([])
const query = reactive({ keyword: '' })
const empty = () => ({ question: '', answer: '', category: '', keywords: '', sort_order: 0, status: 'active' })
const form = reactive(empty())
const load = async () => {
  loading.value = true
  try {
    const res = await adminFaqs(query)
    if (res.code === 200) items.value = res.data.items
  } finally {
    loading.value = false
  }
}
const open = (row) => {
  Object.assign(form, empty(), row || {})
  editingId.value = row?.id || null
  visible.value = true
}
const save = async () => {
  if (editingId.value) await updateFaq(editingId.value, form)
  else await createFaq(form)
  visible.value = false
  load()
}
const remove = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条 FAQ 吗？删除后会从数据库中移除，不能恢复。', '删除确认', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await deleteFaq(id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      load()
    }
  } catch {
    // 用户取消删除时不做处理
  }
}
onMounted(load)
</script>
