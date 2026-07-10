<template>
  <section>
    <h1 class="page-title">游客反馈</h1>
    <p class="page-subtitle">提交游览意见，并查看自己的反馈处理状态。</p>
    <div class="soft-card form-card">
      <el-form label-position="top">
        <el-form-item label="反馈类型">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="景点介绍" value="景点介绍" />
            <el-option label="路线推荐" value="路线推荐" />
            <el-option label="服务建议" value="服务建议" />
            <el-option label="系统问题" value="系统问题" />
          </el-select>
        </el-form-item>
        <el-form-item label="评分">
          <el-rate v-model="form.rating" />
        </el-form-item>
        <el-form-item label="反馈内容">
          <el-input v-model="form.content" type="textarea" :rows="4" placeholder="请输入反馈内容" />
        </el-form-item>
        <el-button type="primary" @click="submit">提交反馈</el-button>
      </el-form>
    </div>

    <h3>我的反馈</h3>
    <div v-for="item in items" :key="item.id" class="feedback-card">
      <div>
        <strong>{{ item.type }}</strong>
        <el-tag size="small">{{ statusText(item.status) }}</el-tag>
      </div>
      <p>{{ item.content }}</p>
      <div class="muted">评分：{{ item.rating }}　提交：{{ item.created_at }}</div>
      <div v-if="item.reply" class="reply">管理员回复：{{ item.reply }}</div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getMyFeedback, submitFeedback } from '../../api/tourist'

const form = reactive({ type: '景点介绍', rating: 5, content: '' })
const items = ref([])
const statusText = (v) => ({ pending: '待处理', processed: '已处理', ignored: '已忽略' }[v] || v)
const load = async () => {
  const res = await getMyFeedback()
  if (res.code === 200) items.value = res.data.items
}
const submit = async () => {
  if (!form.content) return ElMessage.warning('请输入反馈内容')
  const res = await submitFeedback(form)
  if (res.code === 200) {
    ElMessage.success('反馈提交成功')
    form.content = ''
    load()
  }
}
onMounted(load)
</script>

<style scoped>
.form-card {
  padding: 20px;
  margin-bottom: 22px;
}
.feedback-card {
  background: #fff;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
}
.feedback-card > div:first-child {
  display: flex;
  justify-content: space-between;
}
p {
  color: var(--text);
}
.muted,
.reply {
  color: var(--muted);
  font-size: 14px;
}
.reply {
  margin-top: 8px;
  color: var(--primary-dark);
}
</style>
