<template>
  <section>
    <h1 class="page-title">景点管理</h1>
    <p class="page-subtitle">维护景区景点基础信息。</p>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="景点名称/分类/位置" clearable />
      <el-button type="primary" @click="load">查询</el-button>
      <el-button type="primary" plain @click="open()">新增景点</el-button>
    </div>
    <el-table :data="items" class="soft-card" v-loading="loading">
      <el-table-column label="序号" width="70">
        <template #default="{ $index }">{{ $index + 1 }}</template>
      </el-table-column>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="category" label="分类" />
      <el-table-column prop="location" label="位置" />
      <el-table-column prop="ticket_price" label="票价" width="90" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="open(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" title="景点信息" width="620px">
      <el-form label-position="top">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="分类"><el-input v-model="form.category" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="开放时间"><el-input v-model="form.open_time" /></el-form-item>
        <el-form-item label="位置"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="票价"><el-input-number v-model="form.ticket_price" :min="0" /></el-form-item>
        <el-form-item label="推荐游览时长"><el-input v-model="form.recommended_duration" /></el-form-item>
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
import { ElMessageBox } from 'element-plus'
import { adminSpots, createSpot, deleteSpot, updateSpot } from '../../api/admin'

const loading = ref(false)
const visible = ref(false)
const editingId = ref(null)
const items = ref([])
const query = reactive({ keyword: '' })
const empty = () => ({ name: '', category: '', description: '', open_time: '', location: '', ticket_price: 0, recommended_duration: '', image_url: '' })
const form = reactive(empty())
const load = async () => {
  loading.value = true
  try {
    const res = await adminSpots(query)
    if (res.code === 200) items.value = [...res.data.items].sort((a, b) => a.id - b.id)
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
  if (editingId.value) await updateSpot(editingId.value, form)
  else await createSpot(form)
  visible.value = false
  load()
}
const remove = async (row) => {
  await ElMessageBox.confirm(`确定删除景点“${row.name}”吗？`, '删除确认', { type: 'warning' })
  await deleteSpot(row.id)
  load()
}
onMounted(load)
</script>
