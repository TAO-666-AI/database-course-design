<template>
  <section>
    <h1 class="page-title">路线管理</h1>
    <p class="page-subtitle">维护游览路线，并绑定路线包含的景点。</p>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="路线名称" clearable />
      <el-button type="primary" @click="load">查询</el-button>
      <el-button type="primary" plain @click="open()">新增路线</el-button>
    </div>
    <el-table :data="items" class="soft-card" v-loading="loading">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="difficulty" label="难度" width="100" />
      <el-table-column prop="duration_hours" label="时长" width="100" />
      <el-table-column label="包含景点">
        <template #default="{ row }">
          <el-tag v-for="s in row.spots" :key="s.id" style="margin: 2px">{{ s.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="open(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" title="路线信息" width="620px">
      <el-form label-position="top">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="难度">
          <el-select v-model="form.difficulty">
            <el-option label="轻松" value="easy" />
            <el-option label="适中" value="medium" />
            <el-option label="较难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="预计时长"><el-input-number v-model="form.duration_hours" :min="0" /></el-form-item>
        <el-form-item label="包含景点">
          <el-select v-model="form.spot_ids" multiple filterable style="width: 100%">
            <el-option v-for="s in spots" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
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
import { adminRoutes, adminSpots, createRoute, deleteRoute, updateRoute } from '../../api/admin'

const loading = ref(false)
const visible = ref(false)
const editingId = ref(null)
const items = ref([])
const spots = ref([])
const query = reactive({ keyword: '' })
const empty = () => ({ name: '', description: '', difficulty: 'easy', duration_hours: 1, spot_ids: [] })
const form = reactive(empty())
const load = async () => {
  loading.value = true
  try {
    const res = await adminRoutes(query)
    if (res.code === 200) items.value = [...res.data.items].sort((a, b) => a.id - b.id)
  } finally {
    loading.value = false
  }
}
const loadSpots = async () => {
  const res = await adminSpots()
  if (res.code === 200) spots.value = res.data.items
}
const open = (row) => {
  Object.assign(form, empty(), row || {})
  form.spot_ids = row?.spots?.map((s) => s.id) || []
  editingId.value = row?.id || null
  visible.value = true
}
const save = async () => {
  if (editingId.value) await updateRoute(editingId.value, form)
  else await createRoute(form)
  visible.value = false
  load()
}
const remove = async (row) => {
  await ElMessageBox.confirm(`确定删除路线“${row.name}”吗？`, '删除确认', { type: 'warning' })
  await deleteRoute(row.id)
  load()
}
onMounted(() => {
  load()
  loadSpots()
})
</script>
