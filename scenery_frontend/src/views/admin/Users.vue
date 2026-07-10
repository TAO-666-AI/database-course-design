<template>
  <section>
    <h1 class="page-title">用户管理</h1>
    <p class="page-subtitle">查询游客和管理员账号，维护用户状态与角色。</p>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="用户名/手机号" clearable />
      <el-select v-model="query.role" placeholder="角色" clearable style="width: 140px">
        <el-option label="游客" value="tourist" />
        <el-option label="管理员" value="admin" />
      </el-select>
      <el-button type="primary" @click="load">查询</el-button>
    </div>
    <el-table :data="items" class="soft-card" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="role" label="角色" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="created_at" label="注册时间" />
      <el-table-column label="操作" width="260">
        <template #default="{ row }">
          <el-button size="small" @click="changeRole(row)">{{ row.role === 'admin' ? '设为游客' : '设为管理员' }}</el-button>
          <el-button size="small" type="warning" @click="changeStatus(row)">{{ row.status === 'active' ? '禁用' : '启用' }}</el-button>
        </template>
      </el-table-column>
    </el-table>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { adminUsers, updateUserRole, updateUserStatus } from '../../api/admin'

const loading = ref(false)
const items = ref([])
const query = reactive({ keyword: '', role: '' })
const load = async () => {
  loading.value = true
  try {
    const res = await adminUsers(query)
    if (res.code === 200) items.value = [...res.data.items].sort((a, b) => a.id - b.id)
  } finally {
    loading.value = false
  }
}
const changeRole = async (row) => {
  await updateUserRole(row.id, { role: row.role === 'admin' ? 'tourist' : 'admin' })
  load()
}
const changeStatus = async (row) => {
  await updateUserStatus(row.id, { status: row.status === 'active' ? 'disabled' : 'active' })
  load()
}
onMounted(load)
</script>
